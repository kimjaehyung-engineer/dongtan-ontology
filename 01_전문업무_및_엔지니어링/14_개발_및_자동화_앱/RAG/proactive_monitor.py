# -*- coding: utf-8 -*-
"""
동탄트램 24시간 자율 지식망 감시 엔진 (Proactive Knowledge Monitor)
- 지식 그래프 및 정형 지반 DB를 상시 감시하여:
  1) 지반-구조 충돌 (고지하수위, 표층 연약지반)
  2) 온톨로지 경고 (is_warning=1, 대책 미수립 리스크)
  3) 향후 공문 회신기한 및 품질/시험 일정 임박 건
- 리스크 감지 시 직무별 담당자(공사, 공무, 품질, 안전, 소장)에게 선별 카카오 알림 큐 적재
"""
import os
import sys
import json
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

# 콘솔 UTF-8 출력 강제 (이모지 및 특수문자 깨짐 방지)
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

RAG_DIR = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
DB_PATH = RAG_DIR / "geotech_data.db"

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_monitor_tables(conn=None):
    """감시 로그 및 직원 연락망 테이블 초기화"""
    should_close = False
    if conn is None:
        conn = get_db_connection()
        should_close = True

    cur = conn.cursor()

    # 1. 알림 로그 테이블 (중복 알림 방지 해시 키 포함)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS monitor_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_hash TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,         -- GEOTECH, ONTOLOGY, DEADLINE, SAFETY, CONTRACT
        severity TEXT NOT NULL,         -- CRITICAL, WARNING, INFO
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        facility TEXT,                  -- 1공구, 2공구, 차량기지 등
        target_role TEXT NOT NULL,      -- CIVIL_GEO, STRUCT, CONTRACT, QUALITY, SAFETY, CHIEF
        doc_name TEXT,
        page INTEGER,
        status TEXT DEFAULT 'PENDING',  -- PENDING, SENT, ACKNOWLEDGED
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        notified_at TIMESTAMP
    );
    """)

    # 2. 직원 연락망 테이블 (직무 매핑)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS staff_directory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        role TEXT NOT NULL,             -- CIVIL_GEO, STRUCT, CONTRACT, QUALITY, SAFETY, CHIEF
        role_label TEXT NOT NULL,       -- 토목/지반, 구조/가시설, 공무/계약, 품질, 안전, 현장소장
        facility TEXT DEFAULT 'ALL',    -- 담당 공구 (1공구, 2공구, 차량기지, ALL)
        kakao_id TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 기본 샘플 직원 등록 (없는 경우에만)
    cur.execute("SELECT COUNT(*) FROM staff_directory")
    if cur.fetchone()[0] == 0:
        default_staff = [
            ("김재형", "010-0000-0001", "CIVIL_GEO", "토목/지반 엔지니어", "ALL", "staff_geo_01"),
            ("이구조", "010-0000-0002", "STRUCT", "구조/가시설 엔지니어", "ALL", "staff_struct_01"),
            ("박공무", "010-0000-0003", "CONTRACT", "공무/계약/공문 관리자", "ALL", "staff_contract_01"),
            ("정품질", "010-0000-0004", "QUALITY", "품질시험/검측 관리자", "ALL", "staff_quality_01"),
            ("최안전", "010-0000-0005", "SAFETY", "안전/보건 관리책임자", "ALL", "staff_safety_01"),
            ("현장소장", "010-0000-0000", "CHIEF", "현장 총괄 기술소장", "ALL", "chief_dongtan"),
        ]
        cur.executemany("""
            INSERT INTO staff_directory (name, phone, role, role_label, facility, kakao_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, default_staff)

    conn.commit()
    if should_close:
        conn.close()

def make_alert_hash(category, facility, title, identifier):
    """중복 알림 방지를 위한 고유 해시 생성"""
    raw = f"{category}|{facility}|{title}|{identifier}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()[:16]

def scan_geotechnical_risks(conn):
    """지반 정형 DB(시추공, SPT) 스캔: 고지하수위 & 표층 연약지반 위험군 탐지"""
    cur = conn.cursor()
    new_alerts = []

    # 1. 고지하수위 (GL - 3.0m 이내)
    gw_query = """
        SELECT hole_no, facility, doc_name, page_start, groundwater_m, elevation_m
        FROM boreholes
        WHERE groundwater_m IS NOT NULL AND groundwater_m > 0 AND groundwater_m <= 3.0
        ORDER BY groundwater_m ASC
    """
    for r in cur.execute(gw_query).fetchall():
        h = r["hole_no"]
        fac = r["facility"] or "공통"
        gw = r["groundwater_m"]
        doc = r["doc_name"]
        page = r["page_start"]

        title = f"고지하수위 취약 구간 감지 ({h})"
        msg = (
            f"[{fac}] 시추공 {h} 지하수위가 GL-{gw:.2f}m로 고수위 상태입니다.\n"
            f"• 굴착 시 수압 증가 및 보일링/파이핑 우려가 높습니다.\n"
            f"• 가시설 차수그라우팅 및 버팀보 선행하중(Preload) 확인이 필요합니다.\n"
            f"• 출처: {doc} (p.{page})"
        )
        h_key = make_alert_hash("GEOTECH", fac, "HIGH_GW", h)

        new_alerts.append({
            "alert_hash": h_key,
            "category": "GEOTECH",
            "severity": "WARNING",
            "title": title,
            "message": msg,
            "facility": fac,
            "target_role": "CIVIL_GEO",
            "doc_name": doc,
            "page": page
        })

    # 2. 표층 연약지반 (depth <= 3.0m & N < 6)
    soft_query = """
        SELECT DISTINCT s.hole_no, b.facility, b.doc_name, b.page_start, s.depth_m, s.n_value
        FROM spt_records s
        JOIN boreholes b ON s.hole_no = b.hole_no
        WHERE s.depth_m <= 3.0 AND s.n_value < 6
        ORDER BY s.depth_m ASC
    """
    for r in cur.execute(soft_query).fetchall():
        h = r["hole_no"]
        fac = r["facility"] or "공통"
        depth = r["depth_m"]
        n_val = r["n_value"]
        doc = r["doc_name"]
        page = r["page_start"]

        title = f"표층 연약지반(N<6) 침하 위험 구간 ({h})"
        msg = (
            f"[{fac}] 시추공 {h} 심도 {depth:.1f}m에서 N치={n_val}의 연약점토/실트층이 확인되었습니다.\n"
            f"• 중장비(크레인, 천공기) 전도 방지를 위한 복공판 및 치환 대책이 필수입니다.\n"
            f"• 출처: {doc} (p.{page})"
        )
        h_key = make_alert_hash("GEOTECH", fac, "SOFT_GROUND", f"{h}_{depth}")

        new_alerts.append({
            "alert_hash": h_key,
            "category": "GEOTECH",
            "severity": "WARNING",
            "title": title,
            "message": msg,
            "facility": fac,
            "target_role": "CIVIL_GEO",
            "doc_name": doc,
            "page": page
        })

    return new_alerts

def scan_ontology_warnings(conn):
    """지식 그래프(knowledge_edges) 스캔: is_warning=1 관계선 탐지"""
    cur = conn.cursor()
    new_alerts = []

    sql = """
        SELECT e.src_id, e.tgt_id, e.relation, e.label as edge_label, e.doc_name, e.page,
               src.label as src_label, src.type as src_type, src.facility,
               tgt.label as tgt_label, tgt.type as tgt_type, tgt.description as tgt_desc
        FROM knowledge_edges e
        JOIN knowledge_nodes src ON e.src_id = src.id
        JOIN knowledge_nodes tgt ON e.tgt_id = tgt.id
        WHERE e.is_warning = 1
    """
    for r in cur.execute(sql).fetchall():
        src_lbl = r["src_label"]
        tgt_lbl = r["tgt_label"]
        fac = r["facility"] or "차량기지"
        doc = r["doc_name"]
        page = r["page"]
        edge_lbl = r["edge_label"] or "위험 관계"

        title = f"지식망 설계 경고: {tgt_lbl}"
        msg = (
            f"[{fac}] 구조물/구간 '{src_lbl}'에 공학적 리스크 '{tgt_lbl}'가 연결되어 있습니다.\n"
            f"• 관계 속성: {edge_lbl}\n"
            f"• 검토 문서: {doc} (p.{page})\n"
            f"• 조치 권고: 관련 설계 보강 대책(MITIGATION) 및 안전율 기준(SPEC) 준수 여부 긴급 확인 요망."
        )
        h_key = make_alert_hash("ONTOLOGY", fac, "EDGE_WARN", f"{r['src_id']}_{r['tgt_id']}")

        new_alerts.append({
            "alert_hash": h_key,
            "category": "ONTOLOGY",
            "severity": "CRITICAL",
            "title": title,
            "message": msg,
            "facility": fac,
            "target_role": "STRUCT",
            "doc_name": doc,
            "page": page
        })

    return new_alerts

def commit_alerts(conn, alert_list):
    """중복되지 않은 신규 알림만 DB에 적재"""
    cur = conn.cursor()
    inserted_count = 0
    for a in alert_list:
        try:
            cur.execute("""
                INSERT INTO monitor_alerts (
                    alert_hash, category, severity, title, message, 
                    facility, target_role, doc_name, page
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                a["alert_hash"], a["category"], a["severity"], a["title"], a["message"],
                a["facility"], a["target_role"], a["doc_name"], a["page"]
            ))
            inserted_count += 1
        except sqlite3.IntegrityError:
            # 이미 존재하는 알림 (중복 방지)
            pass
    conn.commit()
    return inserted_count

def get_pending_alerts(conn):
    """아직 담당자에게 발송되지 않은 대기 중인 알림 조회"""
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id, a.category, a.severity, a.title, a.message, a.facility, 
               a.target_role, a.doc_name, a.page, a.created_at
        FROM monitor_alerts a
        WHERE a.status = 'PENDING'
        ORDER BY a.severity DESC, a.id ASC
    """)
    return [dict(r) for r in cur.fetchall()]

def match_staff_for_alert(conn, target_role, facility):
    """알림 대상 직무 및 공구에 매칭되는 담당 직원 및 소장님 조회"""
    cur = conn.cursor()
    query = """
        SELECT id, name, phone, role, role_label, facility, kakao_id
        FROM staff_directory
        WHERE is_active = 1 
          AND (role = ? OR role = 'CHIEF')
          AND (facility = 'ALL' OR facility = ? OR ? = 'ALL')
    """
    rows = cur.execute(query, (target_role, facility, facility)).fetchall()
    return [dict(r) for r in rows]

def run_full_scan():
    """전체 지식망 상시 감시 스캔 실행"""
    conn = get_db_connection()
    init_monitor_tables(conn)

    print("=" * 60)
    print("🔍 [동탄트램 24h 자율 감시 에이전트] 지식망 정밀 스캔 시작...")
    print(f"• 실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. 지반 정형 DB 스캔
    geo_alerts = scan_geotechnical_risks(conn)
    print(f"• [지반 분석봇] 고지하수위 및 연약지반 취약 노드 {len(geo_alerts)}건 탐지")

    # 2. 온톨로지 경고 엣지 스캔
    onto_alerts = scan_ontology_warnings(conn)
    print(f"• [온톨로지 감시봇] 지식망 설계 경고(is_warning=1) {len(onto_alerts)}건 탐지")

    all_alerts = geo_alerts + onto_alerts
    inserted = commit_alerts(conn, all_alerts)
    print(f"• [DB 적재] 신규 발생 알림: {inserted}건 (기존 누적 건은 중복 제외 처리)")

    # 3. 대기 중인 알림 및 담당자 매핑 시뮬레이션
    pending = get_pending_alerts(conn)
    print(f"\n📋 [발송 대기 알림 대장] 총 {len(pending)}건 대기 중")
    print("-" * 60)

    for p in pending[:5]:  # 상위 5건만 미리보기 출력
        targets = match_staff_for_alert(conn, p["target_role"], p["facility"])
        target_names = [f"{t['name']}({t['role_label']})" for t in targets]
        print(f"🚨 [{p['severity']}] {p['title']}")
        print(f"   - 위치: {p['facility']} | 분야: {p['target_role']}")
        print(f"   - 카카오톡 선별 수신자: {', '.join(target_names)}")
        print(f"   - 메시지 요약: {p['message'].splitlines()[0]}")
        print("-" * 60)

    conn.close()
    return len(pending)

if __name__ == "__main__":
    run_full_scan()
