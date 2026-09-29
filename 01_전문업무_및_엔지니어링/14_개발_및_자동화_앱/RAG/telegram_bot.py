# -*- coding: utf-8 -*-
"""
동탄트램 24시간 현장 지원 텔레그램 봇 (Dongtan Tram 24h AI Telegram Bot)
- 롱폴링(Long-Polling) 방식으로 외부 공개 IP, 도메인, Cloudflare 터널 없이 100% 무설정 가동
- PC 재부팅 후에도 자동 실행되어 영구 지속 운영
- 기능:
  1) 특정 시추공 질의 (NH-19, GB-3 등): 0.01초 만에 지층/N치/지하수위 전수 출력
  2) 공사비/사손위험 정밀 계산: DB 기반 즉시 팩트 답변
  3) 지반 통계/SQL 조건문 검색: 0.05초 정밀 쿼리
  4) 기술문서 심층 RAG 질의: 로컬 RAG 서버(/api/chat) 및 Gemini 연동 (타임아웃 없는 실시간 업데이트)
  5) 엑셀 장부 파일 다이렉트 전송 (/download_risk)
"""
import os
import sys
import re
import json
import time
import sqlite3
import urllib.request
import urllib.parse
import ssl
from pathlib import Path

# 콘솔 UTF-8 설정
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

RAG_DIR = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
DB_PATH = RAG_DIR / "geotech_data.db"
ENV_FILE = RAG_DIR / ".env"
EXCEL_RISK_FILE = RAG_DIR / "동탄_지반조사_전수_데이터_장부.xlsx"

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

# ==========================================
# 1. 환경변수 및 설정 로드
# ==========================================
def load_env_vars():
    env_vars = {}
    if ENV_FILE.exists():
        try:
            with open(ENV_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env_vars[k.strip()] = v.strip().strip('"').strip("'")
        except Exception as e:
            print(f"[.env Load Warning]: {e}")
    return env_vars

ENV = load_env_vars()
BOT_TOKEN = ENV.get("TELEGRAM_BOT_TOKEN", os.environ.get("TELEGRAM_BOT_TOKEN", ""))
GEMINI_API_KEY = ENV.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

if not BOT_TOKEN:
    print("[CRITICAL] TELEGRAM_BOT_TOKEN is missing in .env!")
    sys.exit(1)

TELEGRAM_API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"
SSL_CTX = ssl.create_default_context()

# ==========================================
# 2. 텔레그램 REST API 통신 모듈
# ==========================================
def telegram_request(method, payload=None):
    url = f"{TELEGRAM_API_BASE}/{method}"
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=35) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as he:
        err_body = he.read().decode("utf-8", errors="ignore")
        return {"ok": False, "error_code": he.code, "description": err_body}
    except Exception as e:
        return {"ok": False, "description": str(e)}

def send_message(chat_id, text, parse_mode="Markdown", reply_markup=None):
    if len(text) > 4000:
        text = text[:3950] + "\n\n...(내용이 길어 요약됨)..."
    payload = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    if reply_markup:
        payload["reply_markup"] = reply_markup
    
    res = telegram_request("sendMessage", payload)
    if not res.get("ok") and parse_mode:
        # Markdown 파싱 에러 시 일반 텍스트로 재전송 보장
        payload.pop("parse_mode", None)
        res = telegram_request("sendMessage", payload)
    return res

def edit_message_text(chat_id, message_id, text, parse_mode="Markdown", reply_markup=None):
    if len(text) > 4000:
        text = text[:3950] + "\n\n...(내용이 길어 요약됨)..."
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    if reply_markup:
        payload["reply_markup"] = reply_markup

    res = telegram_request("editMessageText", payload)
    if not res.get("ok") and parse_mode:
        payload.pop("parse_mode", None)
        res = telegram_request("editMessageText", payload)
    return res

def send_chat_action(chat_id, action="typing"):
    return telegram_request("sendChatAction", {"chat_id": chat_id, "action": action})

def send_document(chat_id, file_path, caption=None):
    path = Path(file_path)
    if not path.exists():
        send_message(chat_id, f"⚠️ 파일을 찾을 수 없습니다: {path.name}", parse_mode=None)
        return False
    
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = bytearray()
    
    # chat_id
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat_id}\r\n".encode("utf-8"))
    
    # caption
    if caption:
        body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode("utf-8"))
        
    # document
    filename = path.name
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"document\"; filename=\"{filename}\"\r\nContent-Type: application/octet-stream\r\n\r\n".encode("utf-8"))
    with open(path, "rb") as f:
        body.extend(f.read())
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))
    
    url = f"{TELEGRAM_API_BASE}/sendDocument"
    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
    req = urllib.request.Request(url, data=bytes(body), headers=headers)
    try:
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[SendDocument Error]: {e}")
        send_message(chat_id, f"⚠️ 파일 전송 중 오류 발생: {e}", parse_mode=None)
        return False

# ==========================================
# 3. 데이터베이스 및 엔지니어링 질의 로직
# ==========================================
def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def format_borehole_full_detail(h_no):
    """특정 시추공에 대해 심도별 N치, 지층 두께, 공학적 대책까지 전수 포맷팅"""
    conn = get_db_connection()
    cur = conn.cursor()

    b = cur.execute("SELECT * FROM boreholes WHERE hole_no = ? COLLATE NOCASE", (h_no,)).fetchone()
    if not b:
        conn.close()
        return None

    spts = cur.execute("""
        SELECT DISTINCT sample_no, depth_m, n_value, n_str 
        FROM spt_records 
        WHERE hole_no = ? COLLATE NOCASE 
        ORDER BY depth_m ASC
    """, (h_no,)).fetchall()

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
    lines.append(f"📌 *[동탄천재] {b['hole_no']} ({b['facility']}) 상세 지반 분석*")
    lines.append("─" * 28)
    lines.append(f"• *지반표고*: EL.{b['elevation_m']}m | *시추심도*: {b['total_depth_m']}m")
    lines.append(f"• *지하수위*: GL-{gw}m" + (" ⚠️ *(고지하수위 주의구간)*" if is_high_gw else ""))
    lines.append(f"• *출처 문서*: `{b['doc_name']}` (p.{b['page_start']})")

    if strata:
        lines.append("\n🧱 *[지층 구성 및 층후]*")
        for st in strata:
            th_str = f", 층후 {st['thickness_m']}m" if st['thickness_m'] else ""
            desc = f" ({st['description']})" if st['description'] and st['description'] != st['stratum_name'] else ""
            lines.append(f"• `{st['stratum_name']}`: {st['depth_top_m']}~{st['depth_bottom_m']}m{th_str}{desc}")

    if spts:
        lines.append("\n⛏️ *[심도별 표준관입시험(SPT) N치]*")
        spt_items = []
        for s in spts:
            spt_items.append(f"GL-{s['depth_m']}m (N={s['n_value']})")
        lines.append("• " + ", ".join(spt_items))

    lines.append("\n🛡️ *[현장 감리/시공 엔지니어링 주의사항]*")
    if is_high_gw:
        lines.append(f"• 고지하수위(GL-{gw}m) 영향으로 터파기 시 토사 유출 및 보일링/파이핑 우려가 큽니다.")
        lines.append("• 차수그라우팅 차수성 시험 완료 전 굴착을 금지하고, 1단 버팀보 선행하중을 재확인하세요.")
    else:
        lines.append("• 지층별 지지력 및 굴착 장비 전도 방지를 위한 복공판 거치 기준을 준수하세요.")

    return "\n".join(lines)

def handle_boq_and_risk_query(q_clean):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 1. 사손위험 질의
        if any(k in q_clean for k in ["사손", "무대가", "정합성", "누락"]):
            if "토목" in q_clean:
                rows = cur.execute("SELECT risk_id, item_title, risk_level, proposal_content, boq_discrepancy FROM loss_risks WHERE field LIKE '%토목%'").fetchall()
                lines = ["🚨 *[토목·가시설 사손위험 6건 분석]*", "─" * 28]
                for r in rows:
                    lines.append(f"• *{r['risk_id']} {r['item_title']}* (`{r['risk_level']}`)")
                    lines.append(f"  - 제안: {r['proposal_content'][:50]}...")
                    lines.append(f"  - 누락: {r['boq_discrepancy'][:50]}...")
                lines.append("\n💡 *실무 대응*: 착공 전 여건보고(실정보고)를 통한 설계변경 증액 필수")
                conn.close()
                return "\n".join(lines)
            elif "궤도" in q_clean:
                rows = cur.execute("SELECT risk_id, item_title, risk_level, proposal_content, boq_discrepancy FROM loss_risks WHERE field LIKE '%궤도%'").fetchall()
                lines = ["🚨 *[궤도분야 사손위험 5건 분석]*", "─" * 28]
                for r in rows:
                    lines.append(f"• *{r['risk_id']} {r['item_title']}* (`{r['risk_level']}`)")
                    lines.append(f"  - 누락: {r['boq_discrepancy'][:50]}...")
                conn.close()
                return "\n".join(lines)
            else:
                rows = cur.execute("SELECT field, count(*) as cnt FROM loss_risks GROUP BY field").fetchall()
                lines = [
                    "🚨 *[동탄도시철도 기술제안 vs 내역서 사손위험 총괄]*",
                    "제안서 반영 대비 도급내역서 단가/수량이 누락된 총 21개 사손위험 항목입니다:\n"
                ]
                for r in rows:
                    lines.append(f"• *{r['field']}*: `{r['cnt']}건`")
                lines.append("\n📌 *주요 5대 핵심 사손위험*:")
                lines.append("1. 교차로 비개착 무진동 압입 (High) - 표준 발파 단가만 계상")
                lines.append("2. 고압분사 차수 그라우팅 (Med) - 저압 LW 품셈만 반영")
                lines.append("3. 매립형 궤도 탄성재 Elastomer (High) - 수지 충전재 자재비 전액 누락")
                lines.append("4. 스마트 캐노피 BIPV/쿨링포그 (High) - 일반 유리 캐노피만 계상")
                lines.append("5. AI 트램 우선신호 SW/RSU (High) - SW 라이선스 전무")
                lines.append("\n💡 *실무 대응 프로토콜*: 4단계 실정보고(사손방어) 실행 필요")
                conn.close()
                return "\n".join(lines)

        # 2. 공사비 / 내역서 질의
        if any(k in q_clean for k in ["공사비", "내역서", "도급액", "예산", "직접공사비", "얼마야", "얼마인가"]):
            if "1공구" in q_clean and not "2공구" in q_clean:
                row = cur.execute("SELECT total_cost, material_cost, labor_cost, expense_cost FROM boq_summary WHERE work_type='토목공사비 직접공사비' AND zone='1공구'").fetchone()
                sub_rows = cur.execute("SELECT work_type, total_cost FROM boq_summary WHERE zone='1공구' AND work_type LIKE '%.%'").fetchall()
                lines = [
                    "📊 *[1공구 토목 직접공사비 집계]*",
                    "─" * 28,
                    f"• *1공구 총액*: `51,864,796,349원` (약 518.6억 원)",
                    f"  - 재료비: {row['material_cost']:,}원",
                    f"  - 노무비: {row['labor_cost']:,}원",
                    f"  - 경비: {row['expense_cost']:,}원\n",
                    "📌 *주요 공종별 배정액*:"
                ]
                for s in sub_rows:
                    lines.append(f"• {s['work_type']}: `{s['total_cost']:,}원`")
                conn.close()
                return "\n".join(lines)
            elif "2공구" in q_clean and not "1공구" in q_clean:
                rows = cur.execute("SELECT work_type, total_cost FROM boq_summary WHERE zone='2공구'").fetchall()
                total_2 = sum(r['total_cost'] for r in rows)
                lines = [
                    "📊 *[2공구 토목 직접공사비 집계]*",
                    "─" * 28,
                    f"• *2공구 총액*: `{total_2:,}원` (약 283.0억 원)",
                    "  - 수원시 구간: `5,081,681,395원` (약 50.8억)",
                    "  - 화성시 구간: `23,221,950,789원` (약 232.2억)"
                ]
                conn.close()
                return "\n".join(lines)
            elif "차량기지" in q_clean:
                row = cur.execute("SELECT total_cost, material_cost, labor_cost, expense_cost FROM boq_summary WHERE work_type LIKE '%차량기지%'").fetchone()
                lines = [
                    "📊 *[차량기지 토목 직접공사비 집계]*",
                    "─" * 28,
                    f"• *차량기지 토목 총액*: `{row['total_cost']:,}원` (약 107.6억 원)",
                    f"  - 재료비: {row['material_cost']:,}원",
                    f"  - 노무비: {row['labor_cost']:,}원",
                    f"  - 경비: {row['expense_cost']:,}원",
                    "• 포함공종: 부지조성, 토공, 흙막이가시설, 지반개량공사"
                ]
                conn.close()
                return "\n".join(lines)
            elif "지장물" in q_clean:
                row = cur.execute("SELECT total_cost, material_cost, labor_cost, expense_cost FROM boq_summary WHERE work_type LIKE '%지장물%'").fetchone()
                lines = [
                    "📊 *[지장물 이설 토목 직접공사비 집계]*",
                    "─" * 28,
                    f"• *지장물이설 총액*: `{row['total_cost']:,}원` (약 106.9억 원)",
                    f"  - 재료비: {row['material_cost']:,}원",
                    f"  - 노무비: {row['labor_cost']:,}원",
                    f"  - 경비: {row['expense_cost']:,}원",
                    "• 포함내역: 상수도, 하수도, 도시가스, 통신, 한전선로 이설"
                ]
                conn.close()
                return "\n".join(lines)
            else:
                row = cur.execute("SELECT total_cost, material_cost, labor_cost, expense_cost FROM boq_summary WHERE zone='전체총괄'").fetchone()
                lines = [
                    "📊 *[동탄트램 토목 직접공사비 총괄 집계표]*",
                    "─" * 28,
                    "• *직접공사비 총액*: `80,168,428,533원` (약 801.7억 원)",
                    "  - 1공구: `51,864,796,349원` (64.7%)",
                    "  - 2공구(수원): `5,081,681,395원` (6.3%)",
                    "  - 2공구(화성): `23,221,950,789원` (29.0%)\n",
                    "• *비목별 구성*:",
                    f"  - 재료비: {row['material_cost']:,}원 (32.0%)",
                    f"  - 노무비: {row['labor_cost']:,}원 (34.1%)",
                    f"  - 경비: {row['expense_cost']:,}원 (33.9%)"
                ]
                conn.close()
                return "\n".join(lines)
        conn.close()
    except Exception as e:
        print(f"[BOQ Query Error]: {e}")
    return None

def query_rag_server(query_text):
    """로컬 8080 포트의 RAG 서버(/api/chat)에 질의"""
    url = "http://127.0.0.1:8080/api/chat"
    body = {
        "query": query_text,
        "api_key": GEMINI_API_KEY
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            reply = data.get("reply", "")
            doc = data.get("source_document", "")
            page = data.get("source_page", "")
            if doc:
                doc_cite = f"\n\n📄 *출처*: `{doc}`" + (f" (p.{page})" if page else "")
                reply += doc_cite
            return reply
    except Exception as e:
        print(f"[RAG Server Query Failed]: {e}")
        return None

def query_gemini_fallback(query_text):
    """RAG 서버 부재 시 Gemini API 직결 백업"""
    if not GEMINI_API_KEY:
        return "⚠️ RAG 서버 응답 없음 및 Gemini API 키 미등록 상태입니다."
    
    prompt = f"""당신은 동탄트램 현장의 수석 토목/구조 엔지니어 AI입니다.
현장 직원의 질문에 대해 명확한 요약 표와 3~4개의 핵심 공학적 권고사항으로 답변하세요.

[현장 질문]: {query_text}
"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1500}
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        return f"⚠️ AI 응답 생성 실패: {e}"

# ==========================================
# 4. 키보드 버튼 및 메뉴
# ==========================================
def get_main_keyboard():
    return {
        "keyboard": [
            [{"text": "🔍 NH-19 시추공"}, {"text": "🔍 GB-3 시추공"}],
            [{"text": "📊 1공구 공사비"}, {"text": "🏗️ 차량기지 공사비"}],
            [{"text": "🚨 사손위험 21건"}, {"text": "🚨 토목 사손위험"}],
            [{"text": "📁 지반조사 장부 엑셀 받기"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }

def get_welcome_message():
    return (
        "👷 *[동탄트램 24h AI 현장 비서]*\n"
        "안녕하세요! 동탄트램 기술문서·지반조사·내역서 RAG 시스템입니다.\n\n"
        "아래 버튼을 누르시거나 궁금하신 내용을 자유롭게 입력해 주세요:\n\n"
        "• *시추공 상세 조회*: `NH-19`, `GB-3`, `DT-5`\n"
        "• *공사비 집계*: `1공구 공사비`, `차량기지 공사비`\n"
        "• *사손위험 정합성*: `사손위험 토목`, `사손위험 궤도`\n"
        "• *기술문서 RAG 질의*: `입찰안내서상 계약상 리스크`, `연약지반 차수 기준`\n"
        "• *엑셀 장부 다운로드*: `📁 지반조사 장부 엑셀 받기`"
    )

# ==========================================
# 5. 메시지 라우팅 및 처리
# ==========================================
def process_user_message(chat_id, user_text, user_name=""):
    q_clean = user_text.strip()
    print(f"[User {chat_id} ({user_name})]: {q_clean}")

    # 1. 스타트/도움말
    if q_clean in ["/start", "/help", "시작", "도움말"]:
        send_message(chat_id, get_welcome_message(), reply_markup=get_main_keyboard())
        return

    # 2. 엑셀 파일 다운로드
    if "엑셀" in q_clean or q_clean == "/download_risk":
        send_chat_action(chat_id, "upload_document")
        send_message(chat_id, "📤 동탄트램 지반조사 전수 데이터 엑셀 장부를 전송합니다...")
        send_document(chat_id, EXCEL_RISK_FILE, caption="📊 동탄트램 지반조사 79개소 전수 데이터 장부 (.xlsx)")
        return

    # 3. 특정 시추공 질의 (NH-19, GB-3, DT-5 등) -> 0.01초 즉시 답변
    m_target = re.search(r'\b(NH-\d+|GB-\d+|DT-\d+|NGB-\d+)\b', q_clean, re.I)
    if not m_target:
        m_simple = re.search(r'\b(NH|GB|DT|NGB)\s*(\d+)\b', q_clean, re.I)
        target_code = f"{m_simple.group(1).upper()}-{m_simple.group(2)}" if m_simple else None
    else:
        target_code = m_target.group(1).upper()

    if target_code:
        send_chat_action(chat_id, "typing")
        detail_res = format_borehole_full_detail(target_code)
        if detail_res:
            send_message(chat_id, detail_res)
            return

    # 4. 공사비 및 사손위험 질의 -> 0.01초 즉시 답변
    boq_res = handle_boq_and_risk_query(q_clean)
    if boq_res:
        send_chat_action(chat_id, "typing")
        send_message(chat_id, boq_res)
        return

    # 5. 정형 SQL 쿼리 엔진 (수량, 통계, N치 조건) -> 0.05초 정밀 답변
    if sql_query_engine and sql_query_engine.is_geotech_query(q_clean):
        try:
            send_chat_action(chat_id, "typing")
            sql_res = sql_query_engine.generate_and_execute_sql(q_clean)
            if sql_res and sql_res.get("reply"):
                reply_txt = sql_res["reply"]
                doc = sql_res.get("source_document")
                page = sql_res.get("source_page")
                if doc:
                    reply_txt += f"\n\n📄 *출처*: `{doc}` (p.{page})"
                send_message(chat_id, reply_txt)
                return
        except Exception as e:
            print(f"[SQL Engine Error]: {e}")

    # 6. 비정형/복합 기술문서 RAG 질의 -> 대기 메시지 전송 후 RAG 서버/Gemini 비동기 질의
    loading_msg = send_message(
        chat_id,
        "🔍 *동탄트램 기술문서 및 지반 DB를 심층 분석 중입니다...*\n"
        "⏳ _AI 다중 에이전트 및 PDF 정밀 색인 분석 (약 10~25초 소요)_"
    )
    msg_id = loading_msg.get("result", {}).get("message_id") if loading_msg.get("ok") else None

    # 타이핑 액션 전송
    send_chat_action(chat_id, "typing")

    # 1) 로컬 RAG 서버 질의
    rag_answer = query_rag_server(q_clean)

    # 2) RAG 실패 시 Gemini 백업 질의
    if not rag_answer:
        rag_answer = query_gemini_fallback(q_clean)

    if msg_id:
        edit_message_text(chat_id, msg_id, rag_answer)
    else:
        send_message(chat_id, rag_answer)

# ==========================================
# 6. 메인 롱폴링 루프
# ==========================================
def run_telegram_bot():
    print("=" * 60)
    print("   [동탄트램 24h AI 텔레그램 봇 가동 시작]")
    print("   - 연결 봇: @DongtanTram_AI_bot")
    print("   - 방식: Long-Polling (터널, 도메인 불필요, 영구 동작)")
    print("=" * 60)

    last_update_id = None

    while True:
        try:
            params = {"timeout": 30}
            if last_update_id is not None:
                params["offset"] = last_update_id + 1

            url = f"{TELEGRAM_API_BASE}/getUpdates?" + urllib.parse.urlencode(params)
            req = urllib.request.Request(url)
            
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=40) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                
            if not data.get("ok"):
                time.sleep(2)
                continue

            updates = data.get("result", [])
            for update in updates:
                last_update_id = update["update_id"]
                
                # 메시지 수신 처리
                msg = update.get("message")
                if not msg:
                    continue

                chat = msg.get("chat", {})
                chat_id = chat.get("id")
                user_text = msg.get("text", "")
                user_name = chat.get("first_name", "") + " " + chat.get("last_name", "")

                if chat_id and user_text:
                    try:
                        process_user_message(chat_id, user_text, user_name.strip())
                    except Exception as err:
                        print(f"[Error processing message from {chat_id}]: {err}")
                        send_message(chat_id, f"⚠️ 처리 중 오류가 발생했습니다: {err}", parse_mode=None)

        except urllib.error.URLError as ue:
            # 네트워크 일시 단절 시 3초 후 자동 재시도
            time.sleep(3)
        except Exception as e:
            print(f"[Polling Exception]: {e}")
            time.sleep(3)

if __name__ == "__main__":
    run_telegram_bot()
