# -*- coding: utf-8 -*-
"""
동탄트램 9대 전문 기술제안서 RAG 정밀 색인 & 지식망 온톨로지 전수 동기화 파이프라인
- 대상: 건축, 기계·소방, 신호, 전기, 토목구조, 토목시공, 토질및기초, 철도·궤도, 통신 9대 전문 제안서
- 동기화 대상 1: _metadata_index.json (페이지 단위 정밀 슬라이싱 및 키워드 색인)
- 동기화 대상 2: geotech_data.db (knowledge_nodes & knowledge_edges 온톨로지 지식망 결합)
- 동기화 대상 3: server.py 라우팅 가중치 (전문 분야별 쿼리 즉각 탐색 보너스)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import re
import json
import sqlite3
from pathlib import Path
from extract_all_proposals import extract_proposals

RAG_DIR = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
META_INDEX_FILE = RAG_DIR / "documents" / "_metadata_index.json"
DB_PATH = RAG_DIR / "geotech_data.db"
SERVER_PATH = RAG_DIR / "server.py"

def run_sync():
    print("=== Step 1: 9대 기술제안서 세부 과제 및 페이지 추출 ===")
    extracted = extract_proposals()
    print(f"추출 완료: 총 {len(extracted)}개 기술제안서 문서 메타데이터")

    # 1. Update _metadata_index.json
    print("\n=== Step 2: RAG 정밀 메타데이터 인덱스(_metadata_index.json) 병합 ===")
    meta_map = {}
    if META_INDEX_FILE.exists():
        with open(META_INDEX_FILE, "r", encoding="utf-8") as f:
            meta_map = json.load(f)

    for doc_name, data in extracted.items():
        meta_map[doc_name] = data
        print(f" - [색인 병합] {doc_name} (총 {data['total_pages']}p, {len(data['sections'])}개 섹션)")

    with open(META_INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(meta_map, f, ensure_ascii=False, indent=2)
    print(f"✅ _metadata_index.json 저장 성공! (기존 문서 포함 총 {len(meta_map)}개 문서 완벽 색인)")

    # 2. Insert into geotech_data.db (knowledge_nodes & knowledge_edges)
    print("\n=== Step 3: 지식망 온톨로지 DB (geotech_data.db) 노드 및 엣지 동기화 ===")
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    # Ensure tables exist
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
        properties TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 1) Root Hub Node for Proposals
    cur.execute("""
    INSERT INTO knowledge_nodes (id, label, type, description, group_name, facility, doc_name, page, properties)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        label=excluded.label,
        description=excluded.description,
        group_name=excluded.group_name,
        facility=excluded.facility
    """, (
        "hub_proposals",
        "9대 기본설계 기술제안",
        "PROPOSAL_HUB",
        "건축, 신호, 전기, 토목구조, 토목시공, 토질및기초, 철도궤도, 통신, 기계소방 9대 분야 기본설계 기술제안 총괄",
        "proposal",
        "공통, 전구간",
        "02_기본설계_기술제안",
        1,
        json.dumps({"total_fields": 9}, ensure_ascii=False)
    ))

    # Group mapping
    group_map = {
        "건축": "건축",
        "기계": "기계·소방",
        "신호": "신호·시스템",
        "전기": "전기·급전",
        "토목구조": "토목·구조",
        "토목시공": "토목·시공",
        "토질": "토질·기초",
        "철도": "철도·궤도",
        "통신": "통신·시스템"
    }

    nodes_inserted = 0
    edges_inserted = 0

    for doc_name, data in extracted.items():
        matched_group = "기타"
        for k, v in group_map.items():
            if k in doc_name:
                matched_group = v
                break

        for s in data["sections"]:
            task_id = s.get("task_id", "")
            if not task_id: continue
            
            clean_id = re.sub(r'[\s,\-_()]+', '_', task_id).lower()
            node_id = f"prop_{clean_id}"
            label = s["title"].split("]")[0] + "]" if "]" in s["title"] else s["title"][:25]
            desc = s["title"]
            fac_list = s.get("facility", [])
            # Always ensure "공통" is present in facility string for universal visibility in filtered views
            fac_str = ", ".join(fac_list + ["공통"])
            
            # Upsert node
            cur.execute("""
            INSERT INTO knowledge_nodes (id, label, type, description, group_name, facility, doc_name, page, properties)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                label=excluded.label,
                description=excluded.description,
                group_name=excluded.group_name,
                facility=excluded.facility,
                doc_name=excluded.doc_name,
                page=excluded.page,
                properties=excluded.properties
            """, (
                node_id,
                label,
                "TechnicalProposal",
                desc,
                matched_group,
                fac_str,
                doc_name,
                s["start_page"],
                json.dumps(s, ensure_ascii=False)
            ))
            nodes_inserted += 1

            # Remove previous proposal edges for this node to avoid duplicate accumulation
            cur.execute("DELETE FROM knowledge_edges WHERE src_id = ?", (node_id,))

            # Connect 1: Hub Proposals
            cur.execute("""
            INSERT INTO knowledge_edges (src_id, tgt_id, relation, label, is_warning, doc_name, page)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (node_id, "hub_proposals", "INCLUDED_IN", "기술제안 포함", 0, doc_name, s["start_page"]))
            edges_inserted += 1

            # Connect 2: Physical Facility Hubs
            targets = []
            if "차량기지" in fac_str:
                targets.append(("hub_depot", "APPLIED_TO", "차량기지 적용"))
                targets.append(("hub_prop_depot", "APPLIED_TO", "제안차량기지 적용"))
            if "정거장" in fac_str or "본선" in fac_str or "전구간" in fac_str:
                targets.append(("hub_sec1", "APPLIED_TO", "1공구 본선 연계"))
                targets.append(("hub_sec2", "APPLIED_TO", "2공구 본선 연계"))

            # Connect 3: Standard & Spec Nodes
            if matched_group == "철도·궤도":
                targets.append(("spec_design_track", "GOVERNED_BY", "궤도설계기준 준수"))
                targets.append(("interface_tram_system", "INTERFACE_WITH", "트램차량 인터페이스"))
            elif matched_group in ("신호·시스템", "전기·급전", "통신·시스템"):
                targets.append(("interface_tram_system", "INTERFACE_WITH", "시스템 통합 인터페이스"))
            elif matched_group in ("토질·기초", "토목·구조", "토목·시공"):
                targets.append(("spec_design_geotech", "GOVERNED_BY", "지반설계기준 준수"))
                targets.append(("spec_design_excavation", "GOVERNED_BY", "가시설설계기준 준수"))

            # Connect 4: General Tender Spec
            targets.append(("spec_tender_general", "COMPLIES_WITH", "입찰안내서 요구조건 준수"))

            for tgt, rel, lbl in targets:
                cur.execute("""
                INSERT INTO knowledge_edges (src_id, tgt_id, relation, label, is_warning, doc_name, page)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (node_id, tgt, rel, lbl, 0, doc_name, s["start_page"]))
                edges_inserted += 1

    conn.commit()
    conn.close()
    print(f"✅ 지식망 온톨로지 동기화 완료! (노드 {nodes_inserted}개, 엣지 {edges_inserted}개 신규 등록/갱신)")

    # 3. Update server.py routing bonuses
    print("\n=== Step 4: RAG 서버(server.py) 질문 라우팅 가중치 최적화 ===")
    with open(SERVER_PATH, "r", encoding="utf-8", errors="ignore") as f:
        srv_code = f.read()

    new_routing_rules = '''                        # [신규 9대 전문 기술제안서 맞춤형 라우팅 가중치]
                        if any(k in query_lower for k in ["신호", "cbtc", "atp", "ato", "차상", "지상신호"]) and "신호" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["전기", "급전", "충전", "수변전", "변전소", "전차선"]) and "전기" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["철도", "궤도", "레일", "분기기", "선형", "무도상"]) and "철도" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["건축", "캐노피", "디자인", "체험시설", "정거장배치"]) and "건축" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["토목구조", "u타입", "지하차도", "기존구조물"]) and "토목구조" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["토목시공", "공기단축", "품질관리", "스마트건설"]) and "토목시공" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["통신", "lte-r", "영상감시", "cctv", "afc", "mis"]) and "통신" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["기계", "소방", "검수설비", "공조", "소화"]) and "기계" in dn: doc_bonus += 50
                        if any(k in query_lower for k in ["토질", "기초", "지반조사", "비탈면", "가시설"]) and "토질" in dn: doc_bonus += 40
'''

    if "# [신규 9대 전문 기술제안서 맞춤형 라우팅 가중치]" not in srv_code:
        anchor = 'if "입찰안내서" in query_lower and "입찰안내서" in dn: doc_bonus += 60'
        if anchor in srv_code:
            srv_code = srv_code.replace(anchor, new_routing_rules + "                        " + anchor, 1)
            with open(SERVER_PATH, "w", encoding="utf-8") as f:
                f.write(srv_code)
            print("✅ server.py 라우팅 가중치 주입 완료!")
        else:
            print("⚠️ server.py 앵커를 찾을 수 없어 라우팅 규칙 주입을 건너뜁니다.")
    else:
        print("ℹ️ server.py 라우팅 가중치 규칙이 이미 존재합니다.")

    print("\n🎉 === 9대 기술제안서 완전 동기화(Full Synchronization) 성공적으로 완료되었습니다! ===")

if __name__ == "__main__":
    run_sync()
