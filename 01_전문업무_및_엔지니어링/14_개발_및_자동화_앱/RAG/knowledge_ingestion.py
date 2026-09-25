# -*- coding: utf-8 -*-
"""
동탄트램 지식 문서 자동 추출 & 지식망 확장 파이프라인 (Knowledge Ingestion Pipeline)
- 새 PDF/엑셀/문서 투입 시:
  1) 텍스트 및 페이지 색인 (_metadata_index.json) 자동 생성/갱신
  2) 시추주상도/정형 데이터 발견 시 SQLite DB (boreholes, spt_records, strata_layers) 자동 적재
  3) 비정형 기술보고서/시방서/검토서 발견 시 LLM(Gemini) 스키마 제약 기반 온톨로지 추출
  4) knowledge_nodes, knowledge_edges 테이블에 MERGE하여 지식 그래프 실시간 확장
"""
import os
import re
import json
import sqlite3
import urllib.request
from pathlib import Path
from pypdf import PdfReader

RAG_DIR = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
DOCS_DIR = RAG_DIR / "documents"
DB_PATH = RAG_DIR / "geotech_data.db"
META_FILE = DOCS_DIR / "_metadata_index.json"

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_knowledge_tables(conn=None):
    """지식망 확장용 동적 노드/엣지 테이블 초기화"""
    should_close = False
    if conn is None:
        conn = get_db_connection()
        should_close = True

    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_nodes (
        id TEXT PRIMARY KEY,
        label TEXT NOT NULL,
        type TEXT NOT NULL,
        description TEXT,
        group_name TEXT,
        facility TEXT,
        doc_name TEXT,
        page INTEGER,
        properties TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_edges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        src_id TEXT NOT NULL,
        tgt_id TEXT NOT NULL,
        relation TEXT NOT NULL,
        label TEXT,
        is_warning INTEGER DEFAULT 0,
        doc_name TEXT,
        page INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(src_id, tgt_id, relation)
    );
    """)
    conn.commit()
    if should_close:
        conn.close()

def load_metadata_index():
    if META_FILE.exists():
        try:
            with open(META_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_metadata_index(data):
    try:
        with open(META_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[KnowledgeIngestion] 메타데이터 저장 실패: {e}")

def parse_drill_log_page(page_text, p_num, doc_name):
    """시추주상도 텍스트 레이어 파싱 (정형 데이터 파서)"""
    if not page_text or not page_text.strip():
        return None, [], []

    m_hole = re.search(r'HOLE\s*No\.?\s*([A-Z0-9_-]+)', page_text, re.I)
    if not m_hole:
        m_hole = re.search(r'\b(NH-\d+|GB-\d+|DT-\d+|NGB-\d+)\b', page_text)
    if not m_hole:
        return None, [], []

    hole_no = m_hole.group(1).strip()
    facility = "기타"
    if hole_no.startswith("GB"):
        facility = "차량기지"
    elif hole_no.startswith("NGB"):
        facility = "차량기지 (제안설계)"
    elif hole_no.startswith("NH"):
        facility = "1공구 본선"
    elif hole_no.startswith("DT"):
        facility = "2공구 본선"

    elevation_m = None
    m_elev = re.search(r'ELEVATION\s*([0-9.]+)\s*M', page_text, re.I)
    if m_elev:
        try: elevation_m = float(m_elev.group(1))
        except ValueError: pass

    groundwater_m = None
    m_gw = re.search(r'GROUND\s*WATER.*?([0-9.]+)\s*M', page_text, re.I)
    if m_gw:
        try: groundwater_m = float(m_gw.group(1))
        except ValueError: pass

    total_depth_m = None
    m_end = re.search(r'(?:굴착심도|심도|TOTAL\s*DEPTH)\s*([0-9.]+)\s*M', page_text, re.I)
    if m_end:
        try: total_depth_m = float(m_end.group(1))
        except ValueError: pass

    driller = None
    m_driller = re.search(r'DRILLER\s*([^\n\r]+)', page_text, re.I)
    if m_driller: driller = m_driller.group(1).strip()

    date_str = None
    m_date = re.search(r'DATE\s*([0-9.~ \t/–-]+)', page_text, re.I)
    if m_date: date_str = m_date.group(1).strip()

    borehole_info = {
        "doc_name": doc_name,
        "hole_no": hole_no,
        "facility": facility,
        "page": p_num,
        "elevation_m": elevation_m,
        "groundwater_m": groundwater_m,
        "total_depth_m": total_depth_m,
        "driller": driller,
        "date": date_str
    }

    # SPT 레코드 파싱
    lines = [l.strip() for l in page_text.split('\n') if l.strip()]
    n_values = []
    for l in lines:
        m_nv = re.match(r'^(\d+)/(\d+)$', l)
        if m_nv:
            n_values.append(int(m_nv.group(1)))
        elif re.match(r'^\d+$', l) and 0 <= int(l) <= 100:
            n_values.append(int(l))

    depths = [float(l) for l in lines if re.match(r'^\d+\.\d+$', l) and 0.5 <= float(l) <= 70.0]

    spt_records = []
    if depths and n_values:
        count = min(len(depths), len(n_values))
        for i in range(count):
            spt_records.append({
                "doc_name": doc_name,
                "hole_no": hole_no,
                "page": p_num,
                "sample_no": f"S-{i+1}",
                "depth_m": depths[i],
                "n_value": n_values[i],
                "n_str": str(n_values[i]),
                "blows": n_values[i],
                "penetration_cm": 30
            })

    # 지층(Strata) 파싱
    strata_records = []
    stratum_keywords = ["매립층", "퇴적층", "풍화토", "풍화암", "연암", "보통암", "경암", "자갈", "모래", "실트", "점토"]
    for l in lines:
        for kw in stratum_keywords:
            if kw in l:
                strata_records.append({
                    "doc_name": doc_name,
                    "hole_no": hole_no,
                    "page": p_num,
                    "stratum_name": kw,
                    "depth_top_m": 0.0,
                    "depth_bottom_m": total_depth_m or 10.0,
                    "thickness_m": None,
                    "uscs": "",
                    "description": l
                })
                break

    return borehole_info, spt_records, strata_records

def call_gemini_extract(prompt, api_key):
    """Gemini REST API를 호출하여 온톨로지 JSON 추출"""
    models = ["gemini-3.6-flash", "gemini-flash-latest", "gemini-3.5-flash-lite"]
    for m in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
        body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.1,
                "responseMimeType": "application/json"
            }
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(body).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                if text.startswith("```json"): text = text[7:]
                if text.startswith("```"): text = text[3:]
                if text.endswith("```"): text = text[:-3]
                return json.loads(text.strip())
        except Exception as e:
            print(f"[KnowledgeIngestion] Gemini API ({m}) 실패: {e}")
            continue
    return None

def extract_engineering_entities_llm(doc_name, sampled_text, api_key):
    """비정형 기술문서에서 엄격한 온톨로지 스키마에 따라 노드와 엣지 추출"""
    prompt = f"""당신은 동탄트램 철도·토목 지반/구조물 전문 온톨로지 엔지니어입니다.
아래 제공된 문서 내용('{doc_name}')을 정밀 분석하여, 지식 그래프(Knowledge Graph)에 추가할 **핵심 구조물, 리스크, 설계/시방 대책, 검측 기준 노드와 관계선(Edges)**을 JSON으로 추출하세요.

[온톨로지 제약 규칙 - 노드가 난잡해지지 않도록 엄격히 준수]:
1. 노드 타입(type)은 오직 다음 5가지만 허용:
   - "FACILITY": 구간/공구/허브 (예: 1공구 본선, 2공구 본선, 차량기지, 환승센터)
   - "STRUCTURE": 구조물/공종/부재 (예: 흙막이 가시설, 정거장 구조물, 비탈면, 옹벽)
   - "RISK": 공학적 위험/파괴/취약요인 (예: 배면 토압증대, 사면활동 붕괴, 지하수 용출, 부등침하)
   - "MITIGATION": 설계 대책/보강 공법 (예: 소일네일링 보강, CIP 차수벽, 약액 그라우팅, 락볼트)
   - "SPEC": 시방/안전율 기준 (예: 건기 안전율 1.5, 허용 침하량 25mm, KCS 기준)
2. 엣지 관계(relation)는 오직 다음만 허용:
   - "LOCATED_IN": 구조물 -> 시설물 (예: 가시설 -> 1공구 본선)
   - "HAS_RISK": 구조물/시추공 -> 리스크 (예: 비탈면 -> 사면활동)
   - "MITIGATED_BY": 리스크 -> 설계대책 (예: 사면활동 -> 소일네일링 보강)
   - "GOVERNED_BY": 대책/구조물 -> 시방기준 (예: 소일네일링 -> 안전율 1.5)
   - "CONNECTED_TO": 부재 간 연결

[문서 텍스트 발췌]:
{sampled_text[:8000]}

[출력 JSON 스키마]:
{{
  "sections": [
    {{"title": "주요 장/절 제목", "start_page": 1, "end_page": 10, "facility": ["1공구 본선"], "summary": "내용 요약"}}
  ],
  "nodes": [
    {{
      "id": "node_영문_유니크_id",
      "label": "명확하고 정제된 한글 명칭",
      "type": "FACILITY|STRUCTURE|RISK|MITIGATION|SPEC",
      "desc": "구체적인 공학적 수치 및 설계 제원 요약 (1~2문장)",
      "facility": "1공구 본선|2공구 본선|차량기지|공통",
      "page": 1
    }}
  ],
  "edges": [
    {{
      "src": "출발 노드 id (기존 hub_sec1, hub_sec2, hub_depot 또는 위 nodes의 id)",
      "tgt": "도착 노드 id",
      "relation": "LOCATED_IN|HAS_RISK|MITIGATED_BY|GOVERNED_BY|CONNECTED_TO",
      "label": "엣지 한글 설명 (예: 위험요인, 보강대책, 위치, 기준)",
      "is_warning": true,
      "page": 1
    }}
  ]
}}
"""
    return call_gemini_extract(prompt, api_key)

def rule_based_fallback_extraction(doc_name, sampled_text):
    """API 키가 없거나 실패 시 동작하는 엔지니어링 룰 기반 백업 추출기"""
    nodes = []
    edges = []
    clean_name = Path(doc_name).stem

    fac = "공통"
    hub_src = "hub_sec1"
    if "차량기지" in doc_name:
        fac = "차량기지"
        hub_src = "hub_depot"
    elif "2공구" in doc_name:
        fac = "2공구 본선"
        hub_src = "hub_sec2"
    elif "1공구" in doc_name:
        fac = "1공구 본선"
        hub_src = "hub_sec1"

    if "비탈면" in clean_name or "사면" in clean_name:
        s_id = f"struct_slope_{abs(hash(clean_name)) % 10000}"
        r_id = f"risk_slope_failure_{abs(hash(clean_name)) % 10000}"
        m_id = f"mit_slope_reinforce_{abs(hash(clean_name)) % 10000}"

        nodes.append({
            "id": s_id, "label": f"{clean_name} 검토 구간",
            "type": "STRUCTURE", "desc": f"{doc_name}에 기술된 비탈면/사면 안정성 검토 대상 단면",
            "facility": fac, "page": 1
        })
        nodes.append({
            "id": r_id, "label": "⚠️ 우기 사면활동 위험 (안전율 저하)",
            "type": "RISK", "desc": "강우 침투 및 지하수위 상승에 따른 활동 안전율 기준 미달 리스크",
            "facility": fac, "page": 1
        })
        nodes.append({
            "id": m_id, "label": "🛡️ 사면 보강 대책 (네일링/배수공)",
            "type": "MITIGATION", "desc": "소일네일링, 격자블록 및 배수공을 통한 사면 활동 방지 보강",
            "facility": fac, "page": 1
        })

        edges.append({"src": hub_src, "tgt": s_id, "relation": "LOCATED_IN", "label": "위치", "is_warning": False, "page": 1})
        edges.append({"src": s_id, "tgt": r_id, "relation": "HAS_RISK", "label": "사면위험", "is_warning": True, "page": 1})
        edges.append({"src": r_id, "tgt": m_id, "relation": "MITIGATED_BY", "label": "보강공법", "is_warning": False, "page": 1})

    return {
        "sections": [
            {"title": f"{clean_name} 총괄", "start_page": 1, "end_page": 10, "facility": [fac], "summary": f"{doc_name} 기술 검토"}
        ],
        "nodes": nodes,
        "edges": edges
    }

def ingest_file(file_path, api_key=None):
    """통합 파일 수신 및 지식망 자동 확장 파이프라인"""
    file_path = Path(file_path)
    if not file_path.exists():
        return {"status": "error", "message": f"파일을 찾을 수 없습니다: {file_path}"}

    init_knowledge_tables()
    conn = get_db_connection()
    doc_name = file_path.name
    total_pages = 0
    borehole_count = 0
    nodes_added = 0
    edges_added = 0

    try:
        if file_path.suffix.lower() == ".pdf":
            reader = PdfReader(str(file_path))
            total_pages = len(reader.pages)

            all_text_samples = []
            cur = conn.cursor()
            for idx, page in enumerate(reader.pages):
                p_text = page.extract_text() or ""
                if idx < 15 or idx % 5 == 0:
                    all_text_samples.append(f"--- Page {idx+1} ---\n" + p_text[:1000])

                b_info, spt_list, strata_list = parse_drill_log_page(p_text, idx + 1, doc_name)
                if b_info and b_info.get("hole_no"):
                    borehole_count += 1
                    cur.execute("""
                    INSERT OR REPLACE INTO boreholes 
                    (doc_name, hole_no, facility, page_start, page_end, elevation_m, groundwater_m, total_depth_m, driller, date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        b_info["doc_name"], b_info["hole_no"], b_info["facility"],
                        b_info["page"], b_info["page"], b_info["elevation_m"],
                        b_info["groundwater_m"], b_info["total_depth_m"],
                        b_info["driller"], b_info["date"]
                    ))

                    for s in spt_list:
                        cur.execute("""
                        INSERT INTO spt_records (doc_name, hole_no, page, sample_no, depth_m, n_value, n_str, blows, penetration_cm)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (s["doc_name"], s["hole_no"], s["page"], s["sample_no"], s["depth_m"], s["n_value"], s["n_str"], s["blows"], s["penetration_cm"]))

                    for st in strata_list:
                        cur.execute("""
                        INSERT INTO strata_layers (doc_name, hole_no, page, stratum_name, depth_top_m, depth_bottom_m, thickness_m, uscs, description)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (st["doc_name"], st["hole_no"], st["page"], st["stratum_name"], st["depth_top_m"], st["depth_bottom_m"], st["thickness_m"], st["uscs"], st["description"]))

            conn.commit()

            sampled_text = "\n".join(all_text_samples)
            extracted = None
            if api_key:
                extracted = extract_engineering_entities_llm(doc_name, sampled_text, api_key)
            if not extracted or not extracted.get("nodes"):
                extracted = rule_based_fallback_extraction(doc_name, sampled_text)

            if extracted and extracted.get("nodes"):
                for n in extracted["nodes"]:
                    nid = n.get("id") or f"node_{abs(hash(n.get('label', '')))}"
                    lbl = n.get("label", nid)
                    ntype = n.get("type", "STRUCTURE")
                    desc = n.get("desc", "")
                    fac = n.get("facility", "공통")
                    p_num = n.get("page", 1)

                    cur.execute("""
                    INSERT OR REPLACE INTO knowledge_nodes 
                    (id, label, type, description, group_name, facility, doc_name, page, properties)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (nid, lbl, ntype, desc, ntype.lower(), fac, doc_name, p_num, json.dumps(n, ensure_ascii=False)))
                    nodes_added += 1

                for e in extracted.get("edges", []):
                    src = e.get("src")
                    tgt = e.get("tgt")
                    rel = e.get("relation", "CONNECTED_TO")
                    elbl = e.get("label", "")
                    warn = 1 if e.get("is_warning") else 0
                    p_num = e.get("page", 1)
                    if src and tgt:
                        cur.execute("""
                        INSERT OR IGNORE INTO knowledge_edges
                        (src_id, tgt_id, relation, label, is_warning, doc_name, page)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (src, tgt, rel, elbl, warn, doc_name, p_num))
                        edges_added += 1

                conn.commit()

            meta_index = load_metadata_index()
            sections = extracted.get("sections", []) if extracted else []
            if not sections:
                sections = [{"title": Path(doc_name).stem, "start_page": 1, "end_page": total_pages, "facility": ["공통"], "summary": f"{doc_name} 전체"}]

            meta_index[doc_name] = {
                "total_pages": total_pages,
                "sections": sections
            }
            save_metadata_index(meta_index)

        conn.close()

        summary_msg = (
            f"✅ [{doc_name}] 지식망 자동 연동 완료! (총 {total_pages}페이지)\n"
            f"- 시추공 정형 데이터: +{borehole_count}공 적재\n"
            f"- 지식 그래프 노드: +{nodes_added}개, 관계선: +{edges_added}개 신규 연동"
        )

        return {
            "status": "success",
            "filename": doc_name,
            "total_pages": total_pages,
            "boreholes_added": borehole_count,
            "nodes_added": nodes_added,
            "edges_added": edges_added,
            "summary": summary_msg
        }

    except Exception as e:
        if conn: conn.close()
        return {"status": "error", "message": f"파이프라인 실행 중 오류 발생: {str(e)}"}

if __name__ == "__main__":
    print("Testing knowledge_ingestion initialization...")
    init_knowledge_tables()
    print("Knowledge tables verified successfully!")
