# -*- coding: utf-8 -*-
"""
동탄트램 카카오톡 쌍방향 연동 브릿지 (KakaoTalk Interactive Bridge) - 고도화 버전
- 1) 모바일 상세 엔지니어링 분석 모드 (심도별 N치 전수, 지층 구성, 공학적 리스크 대책)
- 2) 원클릭 원본 PDF 뷰어 연동 버튼 (스마트폰에서 해당 페이지 즉시 점프)
- 3) 직무별 알림톡 발송 & 카카오 i 오픈빌더 v2 표준 웹훅
"""
import os
import sys
import re
import json
import sqlite3
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

# 콘솔 UTF-8 출력 강제
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

RAG_DIR = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
DB_PATH = RAG_DIR / "geotech_data.db"
URL_FILE = RAG_DIR / "public_url.txt"

# 모듈 임포트 연동
sys.path.insert(0, str(RAG_DIR))
try:
    from graph_intelligence import extract_graph_intelligence
except ImportError:
    def extract_graph_intelligence(q):
        return {"matched_holes": [], "target_docs": [], "target_pages": []}

try:
    import sql_query_engine
except ImportError:
    sql_query_engine = None

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def get_public_tunnel_url():
    """현재 가동 중인 Cloudflare 공인 HTTPS 도메인 조회"""
    if URL_FILE.exists():
        try:
            with open(URL_FILE, "r", encoding="utf-8") as f:
                url = f.read().strip()
                if url.startswith("https://"):
                    return url
        except Exception:
            pass
    return "https://awesome-touring-pan-discharge.trycloudflare.com"

def get_gemini_api_key():
    """Gemini API 키 로드"""
    env_file = RAG_DIR / ".env"
    if env_file.exists():
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    return os.environ.get("GEMINI_API_KEY", "")

# ==========================================
# 1. 시추공 상세 엔지니어링 포맷터 (상세 데이터 꽉 채우기)
# ==========================================
def format_borehole_full_detail(h_no, query_text):
    """특정 시추공에 대해 심도별 N치, 지층 두께, 공학적 대책까지 전수 포맷팅"""
    conn = get_db_connection()
    cur = conn.cursor()

    # 1. 기본 제원
    b = cur.execute("SELECT * FROM boreholes WHERE hole_no = ? COLLATE NOCASE", (h_no,)).fetchone()
    if not b:
        conn.close()
        return None

    # 2. SPT N치 전수 조회
    spts = cur.execute("""
        SELECT DISTINCT sample_no, depth_m, n_value, n_str 
        FROM spt_records 
        WHERE hole_no = ? COLLATE NOCASE 
        ORDER BY depth_m ASC
    """, (h_no,)).fetchall()

    # 3. 지층 현황 조회
    strata = cur.execute("""
        SELECT DISTINCT stratum_name, depth_top_m, depth_bottom_m, thickness_m, description 
        FROM strata_layers 
        WHERE hole_no = ? COLLATE NOCASE 
        ORDER BY depth_top_m ASC
    """, (h_no,)).fetchall()

    conn.close()

    gw = b["groundwater_m"]
    is_high_gw = gw is not None and 0 < gw <= 3.0

    lines = []
    lines.append(f"📌 [동탄천재] {b['hole_no']} ({b['facility']}) 상세 지반 분석")
    lines.append("────────────────────")
    lines.append(f"• 지반표고: EL.{b['elevation_m']}m | 시추심도: {b['total_depth_m']}m")
    lines.append(f"• 지하수위: GL-{gw}m" + (" ⚠️ (고지하수위 주의구간)" if is_high_gw else ""))

    # 지층 현황
    if strata:
        lines.append("\n🧱 [지층 구성 및 층후]")
        for st in strata:
            th_str = f", 층후 {st['thickness_m']}m" if st['thickness_m'] else ""
            desc = f" ({st['description']})" if st['description'] and st['description'] != st['stratum_name'] else ""
            lines.append(f"• {st['stratum_name']}: {st['depth_top_m']}~{st['depth_bottom_m']}m{th_str}{desc}")

    # SPT N치 전수 목록
    if spts:
        lines.append("\n⛏️ [심도별 표준관입시험(SPT) N치]")
        spt_items = []
        for s in spts:
            spt_items.append(f"GL-{s['depth_m']}m(N={s['n_value']})")
        lines.append("• " + ", ".join(spt_items))

    # 공학적 리스크 & 실무 권고사항
    lines.append("\n🛡️ [현장 감리/시공 엔지니어링 주의사항]")
    if is_high_gw:
        lines.append(f"• 고지하수위(GL-{gw}m) 영향으로 터파기 시 토사 유출 및 보일링/파이핑 우려가 큽니다.")
        lines.append("• 차수그라우팅 차수성 시험 완료 전 굴착을 금지하고, 1단 버팀보 선행하중을 재확인하세요.")
    else:
        lines.append("• 지층별 지지력 및 굴착 장비 전도 방지를 위한 복공판 거치 기준을 준수하세요.")

    reply_text = "\n".join(lines)
    return {
        "reply": reply_text,
        "doc_name": b["doc_name"],
        "page": b["page_start"],
        "hole_no": b["hole_no"]
    }

def handle_boq_and_risk_query(q_clean):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 1. 사손위험 관련 질의
        if any(k in q_clean for k in ["사손", "무대가", "정합성", "누락"]):
            if "토목" in q_clean:
                rows = cur.execute("SELECT risk_id, item_title, risk_level, proposal_content, boq_discrepancy FROM loss_risks WHERE field LIKE '%토목%'").fetchall()
                lines = ["🚨 [토목·가시설 사손위험 6건 분석]"]
                for r in rows:
                    lines.append(f"• {r['risk_id']} {r['item_title']} ({r['risk_level']})\n  - 제안: {r['proposal_content'][:45]}...\n  - 내역 누락: {r['boq_discrepancy'][:50]}...")
                lines.append("\n💡 실무 대응: 착공 전 여건보고(실정보고)를 통한 설계변경 증액 필수")
                conn.close()
                return {
                    "reply": "\n".join(lines),
                    "doc_name": "동탄도시철도_기술제안vs내역서_정합성검토_사손위험목록.xlsx",
                    "page": 2
                }
            elif "궤도" in q_clean:
                rows = cur.execute("SELECT risk_id, item_title, risk_level, proposal_content, boq_discrepancy FROM loss_risks WHERE field LIKE '%궤도%'").fetchall()
                lines = ["🚨 [궤도분야 사손위험 5건 분석]"]
                for r in rows:
                    lines.append(f"• {r['risk_id']} {r['item_title']} ({r['risk_level']})\n  - 내역 누락: {r['boq_discrepancy'][:50]}...")
                conn.close()
                return {
                    "reply": "\n".join(lines),
                    "doc_name": "동탄도시철도_기술제안vs내역서_정합성검토_사손위험목록.xlsx",
                    "page": 3
                }
            else:
                rows = cur.execute("SELECT field, count(*) as cnt FROM loss_risks GROUP BY field").fetchall()
                lines = [
                    "🚨 [동탄도시철도 기술제안 vs 내역서 사손위험 총괄]",
                    "제안서 반영 대비 도급내역서 단가/수량이 누락된 총 21개 사손위험 항목입니다:\n"
                ]
                for r in rows:
                    lines.append(f"• {r['field']}: {r['cnt']}건")
                lines.append("\n📌 주요 핵심 사손:")
                lines.append("1. 교차로 비개착 무진동 압입 (High) - 표준 발파 단가만 계상")
                lines.append("2. 고압분사 차수 그라우팅 (Med) - 저압 LW 품셈만 반영")
                lines.append("3. 매립형 궤도 탄성재 Elastomer (High) - 수지 충전재 자재비 전액 누락")
                lines.append("4. 스마트 캐노피 BIPV/쿨링포그 (High) - 일반 유리 캐노피만 계상")
                lines.append("5. AI 트램 우선신호 SW/RSU (High) - SW 라이선스 전무")
                lines.append("\n💡 실무 대응 프로토콜: 4단계 실정보고(사손방어) 실행 필요")
                conn.close()
                return {
                    "reply": "\n".join(lines),
                    "doc_name": "동탄도시철도_기술제안vs내역서_정합성검토_사손위험목록.xlsx",
                    "page": 1
                }

        # 2. 공사비 / 내역서 질의
        if any(k in q_clean for k in ["공사비", "내역서", "도급액", "예산", "직접공사비", "얼마야", "얼마인가"]):
            if "1공구" in q_clean and not "2공구" in q_clean:
                row = cur.execute("SELECT total_cost, material_cost, labor_cost, expense_cost FROM boq_summary WHERE work_type='토목공사비 직접공사비' AND zone='1공구'").fetchone()
                sub_rows = cur.execute("SELECT work_type, total_cost FROM boq_summary WHERE zone='1공구' AND work_type LIKE '%.%'").fetchall()
                lines = [
                    "📊 [1공구 토목 직접공사비 집계]",
                    f"• 1공구 총액: 51,864,796,349원 (약 518.6억 원)",
                    f"  - 재료비: {row['material_cost']:,}원",
                    f"  - 노무비: {row['labor_cost']:,}원",
                    f"  - 경비: {row['expense_cost']:,}원\n",
                    "📌 주요 공종별 배정액:"
                ]
                for s in sub_rows:
                    lines.append(f"• {s['work_type']}: {s['total_cost']:,}원")
                conn.close()
                return {
                    "reply": "\n".join(lines),
                    "doc_name": "동탄트램_토목내역서_설계출력본.pdf",
                    "page": 1
                }
            elif "2공구" in q_clean and not "1공구" in q_clean:
                rows = cur.execute("SELECT work_type, total_cost FROM boq_summary WHERE zone='2공구'").fetchall()
                total_2 = sum(r['total_cost'] for r in rows)
                lines = [
                    "📊 [2공구 토목 직접공사비 집계]",
                    f"• 2공구 총액: {total_2:,}원 (약 283.0억 원)",
                    f"  - 수원시 구간: 5,081,681,395원 (약 50.8억)",
                    f"  - 화성시 구간: 23,221,950,789원 (약 232.2억)"
                ]
                conn.close()
                return {
                    "reply": "\n".join(lines),
                    "doc_name": "동탄트램_토목내역서_설계출력본.pdf",
                    "page": 1
                }
            elif "차량기지" in q_clean:
                row = cur.execute("SELECT total_cost, material_cost, labor_cost, expense_cost FROM boq_summary WHERE work_type LIKE '%차량기지%'").fetchone()
                lines = [
                    "📊 [차량기지 토목 직접공사비 집계]",
                    f"• 차량기지 토목 총액: {row['total_cost']:,}원 (약 107.6억 원)",
                    f"  - 재료비: {row['material_cost']:,}원",
                    f"  - 노무비: {row['labor_cost']:,}원",
                    f"  - 경비: {row['expense_cost']:,}원",
                    "• 포함공종: 부지조성, 토공, 흙막이가시설, 지반개량공사"
                ]
                conn.close()
                return {
                    "reply": "\n".join(lines),
                    "doc_name": "동탄트램_토목내역서_설계출력본.pdf",
                    "page": 1
                }
            elif "지장물" in q_clean:
                row = cur.execute("SELECT total_cost, material_cost, labor_cost, expense_cost FROM boq_summary WHERE work_type LIKE '%지장물%'").fetchone()
                lines = [
                    "📊 [지장물 이설 토목 직접공사비 집계]",
                    f"• 지장물이설 총액: {row['total_cost']:,}원 (약 106.9억 원)",
                    f"  - 재료비: {row['material_cost']:,}원",
                    f"  - 노무비: {row['labor_cost']:,}원",
                    f"  - 경비: {row['expense_cost']:,}원",
                    "• 포함내역: 상수도, 하수도, 도시가스, 통신, 한전선로 이설"
                ]
                conn.close()
                return {
                    "reply": "\n".join(lines),
                    "doc_name": "동탄트램_토목내역서_설계출력본.pdf",
                    "page": 1
                }
            else:
                row = cur.execute("SELECT total_cost, material_cost, labor_cost, expense_cost FROM boq_summary WHERE zone='전체총괄'").fetchone()
                lines = [
                    "📊 [동탄트램 토목 직접공사비 총괄 집계표]",
                    f"• 직접공사비 총액: 80,168,428,533원 (약 801.7억 원)",
                    f"  - 1공구: 51,864,796,349원 (64.7%)",
                    f"  - 2공구(수원): 5,081,681,395원 (6.3%)",
                    f"  - 2공구(화성): 23,221,950,789원 (29.0%)\n",
                    f"• 비목별 구성:",
                    f"  - 재료비: {row['material_cost']:,}원 (32.0%)",
                    f"  - 노무비: {row['labor_cost']:,}원 (34.1%)",
                    f"  - 경비: {row['expense_cost']:,}원 (33.9%)"
                ]
                conn.close()
                return {
                    "reply": "\n".join(lines),
                    "doc_name": "동탄트램_토목내역서_설계출력본.pdf",
                    "page": 1
                }
        conn.close()
    except Exception as e:
        print(f"[BOQ Query Error]: {e}")
    return None

# ==========================================
# 2. 통합 질의응답 엔진
# ==========================================
def answer_query_with_graph(query_text, user_id=None):
    """
    카톡 질의 분석 -> 
    1) 특정 시추공 질의: format_borehole_full_detail (0.01초 상세)
    2) 공사비 및 사손위험 질의: handle_boq_and_risk_query (0.01초 정밀 팩트)
    3) 수량/통계 질의: sql_query_engine (0.05초 정밀)
    4) 일반/복합 질의: 지식망 + Gemini 고속 직결 (1.5초)
    """
    q_clean = query_text.strip()

    # 1. 특정 시추공 단독 질의 (예: NH-19, GB-3, DT-5 등)
    m_target = re.search(r'\b(NH-\d+|GB-\d+|DT-\d+|NGB-\d+)\b', q_clean, re.I)
    if not m_target:
        # NH19 -> NH-19 보정
        m_simple = re.search(r'\b(NH|GB|DT|NGB)\s*(\d+)\b', q_clean, re.I)
        if m_simple:
            target_code = f"{m_simple.group(1).upper()}-{m_simple.group(2)}"
        else:
            target_code = None
    else:
        target_code = m_target.group(1).upper()

    if target_code:
        detail_res = format_borehole_full_detail(target_code, q_clean)
        if detail_res:
            return {
                "reply": detail_res["reply"],
                "doc_name": detail_res["doc_name"],
                "page": detail_res["page"],
                "hole_no": detail_res["hole_no"]
            }

    # 2. 공사비 및 사손위험 전용 쿼리 (100% 엑셀/SQL 정밀 팩트)
    boq_res = handle_boq_and_risk_query(q_clean)
    if boq_res:
        return boq_res

    # 3. 정형 SQL 쿼리 엔진 (수량, 통계, N치 조건, 지하수위 범위)
    if sql_query_engine and sql_query_engine.is_geotech_query(q_clean):
        try:
            sql_res = sql_query_engine.generate_and_execute_sql(q_clean)
            if sql_res and sql_res.get("reply"):
                return {
                    "reply": sql_res["reply"],
                    "doc_name": sql_res.get("source_document", "기본설계 시추주상도"),
                    "page": sql_res.get("source_page", 1),
                    "hole_no": target_code
                }
        except Exception as e:
            print(f"[SQL Engine Error]: {e}")

    # 3. 비정형/복합 질문 -> 지식망 추론 + Gemini 고속 질의
    gi = extract_graph_intelligence(q_clean)
    matched_holes = gi.get("matched_holes", [])
    target_docs = gi.get("target_docs", [])
    target_pages = gi.get("target_pages", [])

    context_lines = []
    if matched_holes:
        conn = get_db_connection()
        cur = conn.cursor()
        placeholders = ",".join(["?"] * len(matched_holes))
        b_rows = cur.execute(f"""
            SELECT hole_no, facility, doc_name, page_start, groundwater_m, elevation_m, total_depth_m
            FROM boreholes WHERE hole_no IN ({placeholders})
        """, matched_holes).fetchall()
        for b in b_rows:
            context_lines.append(f"• {b['hole_no']}({b['facility']}): 수위 GL-{b['groundwater_m']}m, 표고 EL.{b['elevation_m']}m, 심도 {b['total_depth_m']}m (출처: {b['doc_name']} p.{b['page_start']})")
        conn.close()

    master_stats = (
        "• [동탄트램 지반조사 보링공 총괄]: 총 79개소\n"
        "  - 1공구 본선: 36개소 (NH-1~NH-45)\n"
        "  - 2공구 본선: 28개소 (DT-1~DT-28)\n"
        "  - 차량기지: 15개소 (GB 10개소, NGB 5개소)\n"
    )
    context_str = master_stats + ("\n" + "\n".join(context_lines) if context_lines else "")

    api_key = get_gemini_api_key()
    if not api_key:
        return {"reply": f"지식망 검색 결과:\n{context_str}", "doc_name": "기본설계 시추주상도", "page": 1}

    prompt = f"""당신은 동탄트램 현장의 24시간 수석 토목/지반 엔지니어 AI입니다.
현장 직원이 카카오톡으로 질문을 보냈습니다. 지식망과 데이터베이스를 바탕으로 실무적이고 신속하게 3~4문장으로 핵심을 답변하세요.

[현장 질문]:
"{q_clean}"

[지식망 매칭 데이터]:
{context_str}

[답변 원칙]:
1. 모바일 카카오톡이므로 서론을 빼고 결론부터 수치와 함께 명확히 제시하세요.
2. 고지하수위(GL-3m)나 연약지반 출현 시 차수/전도방지 안전 대책을 반드시 덧붙이세요.
"""
    answer_text = ""
    for m in ["gemini-flash-lite-latest", "gemini-3.1-flash-lite"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
        body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.1, "maxOutputTokens": 400}
        }
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                answer_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                if answer_text: break
        except Exception:
            continue

    if not answer_text:
        answer_text = f"📌 [동탄천재 데이터 조회]\n{context_str}"

    doc = list(target_docs)[0] if target_docs else "기본설계 시추주상도(1공구)_45공.pdf"
    p = target_pages[0] if target_pages else 1
    return {"reply": answer_text, "doc_name": doc, "page": p, "hole_no": target_code}

# ==========================================
# 3. 카카오 i 오픈빌더 v2 웹훅 핸들러 (버튼 카드 결합)
# ==========================================
def handle_kakao_webhook(request_body_dict):
    """
    카카오 i 오픈빌더 v2 응답:
    1) simpleText: 상세 텍스트
    2) basicCard: 원본 PDF 모바일 뷰어 바로보기 버튼 카드
    3) quickReplies: 원터치 퀵버튼
    """
    user_request = request_body_dict.get("userRequest", {})
    utterance = user_request.get("utterance", "").strip()
    user_info = user_request.get("user", {})
    user_id = user_info.get("id", "anonymous")

    if not utterance:
        reply_data = {
            "reply": "안녕하세요! 동탄트램 현장 비서 '동탄천재'입니다. 👷\n궁금하신 공구, 시추공 번호(예: NH-19), 시방서 안전율 기준을 질문해 주세요!",
            "doc_name": "기본설계 시추주상도(1공구)_45공.pdf",
            "page": 1,
            "hole_no": None
        }
    else:
        reply_data = answer_query_with_graph(utterance, user_id=user_id)

    reply_text = reply_data.get("reply", "")
    doc_name = reply_data.get("doc_name", "기본설계 시추주상도(1공구)_45공.pdf")
    page_num = reply_data.get("page", 1)
    hole_no = reply_data.get("hole_no")

    tunnel_base = get_public_tunnel_url()
    encoded_doc = urllib.parse.quote(doc_name)
    viewer_url = f"{tunnel_base}/?doc={encoded_doc}&p={page_num}"

    outputs = [
        {
            "simpleText": {
                "text": reply_text
            }
        }
    ]

    raw_pdf_url = f"{tunnel_base}/api/view?document={encoded_doc}#page={page_num}"

    # 원본 문서 뷰어 바로가기 카드 결합
    outputs.append({
        "basicCard": {
            "title": f"📄 원본 기술문서 검증 (p.{page_num})",
            "description": f"출처: {doc_name}\n스마트폰 뷰어 또는 원본 PDF를 열어 손가락으로 자유롭게 확대/이동하세요.",
            "buttons": [
                {
                    "action": "webLink",
                    "label": "📲 스마트폰 뷰어에서 열기",
                    "webLinkUrl": viewer_url
                },
                {
                    "action": "webLink",
                    "label": "🔍 원본 PDF 바로보기 (자유확대)",
                    "webLinkUrl": raw_pdf_url
                }
            ]
        }
    })

    # 동적 퀵버튼 구성
    quick_replies = []
    if hole_no:
        quick_replies.append({"label": f"🔍 {hole_no} 지층 상세", "action": "message", "messageText": f"{hole_no} 지층 구성 상세히 알려줘"})
        quick_replies.append({"label": f"⛏️ {hole_no} N치 전체", "action": "message", "messageText": f"{hole_no} 심도별 N치 전체 알려줘"})
    quick_replies.append({"label": "💰 1공구 공사비", "action": "message", "messageText": "1공구 토목공사비 얼마야?"})
    quick_replies.append({"label": "🚨 사손위험 21건", "action": "message", "messageText": "사손위험 항목 알려줘"})
    quick_replies.append({"label": "🏗️ 차량기지 공사비", "action": "message", "messageText": "차량기지 토목공사비 얼마야?"})
    quick_replies.append({"label": "⚠️ 고지하수위 현황", "action": "message", "messageText": "지하수위 3m 이내 시추공 알려줘"})

    response_payload = {
        "version": "2.0",
        "template": {
            "outputs": outputs,
            "quickReplies": quick_replies[:5]
        }
    }
    return response_payload

if __name__ == "__main__":
    print("=" * 60)
    print("💬 [동탄트램 카카오톡 쌍방향 브릿지 고도화 테스트]")
    print("=" * 60)
    test_payload = {"userRequest": {"utterance": "NH-19 상세 지층 알려줘", "user": {"id": "test"}}}
    res = handle_kakao_webhook(test_payload)
    print("1. 텍스트 말풍선:\n", res["template"]["outputs"][0]["simpleText"]["text"])
    print("\n2. 바로가기 버튼 카드:\n", res["template"]["outputs"][1]["basicCard"])
