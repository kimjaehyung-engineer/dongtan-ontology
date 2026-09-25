import sqlite3
import json
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

db_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\geotech_data.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
doc_name = "입찰안내서(동탄트램).pdf"

# 1. Bidding Guide Knowledge Nodes
nodes = [
    {
        "id": "spec_tender_general",
        "label": "동탄트램 입찰안내서 총괄",
        "type": "SPEC",
        "desc": "동탄 도시철도 건설공사(1단계) 기본설계 기술제안입찰 유의사항 및 최상위 적용기준",
        "group_name": "spec",
        "facility": "공통",
        "page": 3
    },
    {
        "id": "contract_special_terms",
        "label": "공사계약특수조건 (제3장)",
        "type": "CONTRACT",
        "desc": "기술제안입찰 리스크 분담원칙, 설계변경 제한요건 및 특수조건 준수 의무",
        "group_name": "spec",
        "facility": "공통",
        "page": 142
    },
    {
        "id": "contract_unforeseen_ground",
        "label": "지반조건 및 지장물 상이 조항",
        "type": "CONTRACT",
        "desc": "기본설계 조건과 현장 지반·지장물 상이 시 책임소재 및 설계변경 허용 기준",
        "group_name": "spec",
        "facility": "공통",
        "page": 150
    },
    {
        "id": "spec_design_geotech",
        "label": "지반조사 및 기초 실시설계지침",
        "type": "SPEC",
        "desc": "시추 간격/심도 규정, 지반정수 산정 및 구조물/비탈면 기초 허용지지력·침하량 기준",
        "group_name": "spec",
        "facility": "공통",
        "page": 241
    },
    {
        "id": "spec_design_excavation",
        "label": "흙막이 가시설 및 지하수위 설계지침",
        "type": "SPEC",
        "desc": "도심지 굴착 가시설 변위기준, 배면 침하 방지, 차수 및 지하수위 관리기준",
        "group_name": "spec",
        "facility": "1공구/2공구 본선",
        "page": 260
    },
    {
        "id": "spec_design_slope",
        "label": "절·성토 비탈면 설계지침",
        "type": "SPEC",
        "desc": "비탈면 최소 기준안전율(건기 1.5, 우기 1.3, 지진 1.1) 및 표준기울기 지침",
        "group_name": "spec",
        "facility": "차량기지",
        "page": 280
    },
    {
        "id": "spec_design_track",
        "label": "트램 궤도 및 노반 설계지침",
        "type": "SPEC",
        "desc": "무매설/매설 궤도 구조, 최소 곡선반경, 허용 구배 및 노반 지지력 기준",
        "group_name": "spec",
        "facility": "1공구/2공구 본선",
        "page": 310
    },
    {
        "id": "spec_const_quality_safety",
        "label": "시공품질 및 안전·환경관리지침",
        "type": "SPEC",
        "desc": "현장 시공 중 계측관리(경보단계별 조치), 비산먼지/소음진동 민원관리",
        "group_name": "spec",
        "facility": "공통",
        "page": 356
    },
    {
        "id": "interface_section_boundary",
        "label": "공구간(1공구-2공구) 경계 인터페이스",
        "type": "INTERFACE",
        "desc": "1·2공구 경계부 시공 연계, 궤도·시스템 접속 및 공정 간섭 조정조건",
        "group_name": "spec",
        "facility": "1공구-2공구 경계",
        "page": 497
    },
    {
        "id": "interface_tram_system",
        "label": "트램차량-인프라 인터페이스 조건",
        "type": "INTERFACE",
        "desc": "차량 한계, 급전방식, 신호·통신 및 차량기지 검수설비 접속 요건",
        "group_name": "spec",
        "facility": "차량기지 및 본선",
        "page": 502
    },
    {
        "id": "spec_tech_proposal_sub",
        "label": "기술제안서 작성지침",
        "type": "SPEC",
        "desc": "공사비 절감, 공기단축, 안전성 향상을 위한 기술제안서 작성 서식 및 필수 검토항목",
        "group_name": "spec",
        "facility": "공통",
        "page": 536
    },
    {
        "id": "eval_award_criteria",
        "label": "낙찰자 결정 및 기술제안 평가지침",
        "type": "EVAL",
        "desc": "기술제안서 차등배점, 가시설/지반 안전성 평가항목 및 부적격/감점 기준",
        "group_name": "spec",
        "facility": "공통",
        "page": 586
    }
]

for n in nodes:
    props = json.dumps({
        "id": n["id"],
        "label": n["label"],
        "type": n["type"],
        "desc": n["desc"],
        "facility": n["facility"],
        "page": n["page"]
    }, ensure_ascii=False)
    
    c.execute("""
        INSERT OR REPLACE INTO knowledge_nodes 
        (id, label, type, description, group_name, facility, doc_name, page, properties, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (n["id"], n["label"], n["type"], n["desc"], n["group_name"], n["facility"], doc_name, n["page"], props, now_str))

print(f"Inserted/Updated {len(nodes)} knowledge nodes!")

# 2. Knowledge Edges connecting Bidding Guide to existing entities
edges = [
    # 1공구 본선 연결
    ("hub_sec1", "spec_design_geotech", "GOVERNED_BY", "1공구 지반설계 지침 준용", 0, 241),
    ("hub_sec1", "spec_design_excavation", "GOVERNED_BY", "1공구 도심지 굴착 가시설 지침", 0, 260),
    ("hub_sec1", "spec_design_track", "GOVERNED_BY", "1공구 궤도/노반 설계기준", 0, 310),
    ("hub_sec1", "interface_section_boundary", "INTERFACE_WITH", "1공구-2공구 경계 접속", 0, 497),

    # 2공구 본선 연결
    ("hub_sec2", "spec_design_geotech", "GOVERNED_BY", "2공구 지반설계 지침 준용", 0, 241),
    ("hub_sec2", "spec_design_excavation", "GOVERNED_BY", "2공구 도심지 굴착 가시설 지침", 0, 260),
    ("hub_sec2", "spec_design_track", "GOVERNED_BY", "2공구 궤도/노반 설계기준", 0, 310),
    ("hub_sec2", "interface_section_boundary", "INTERFACE_WITH", "2공구-1공구 경계 접속", 0, 497),

    # 차량기지 연결
    ("hub_depot", "spec_design_slope", "GOVERNED_BY", "차량기지 절토사면 기준", 0, 280),
    ("hub_depot", "interface_tram_system", "GOVERNED_BY", "차량기지 검수·주박 인터페이스", 0, 502),
    ("struct_slope_2566", "spec_design_slope", "COMPLIES_WITH", "사면안전율 해석 만족", 0, 280),

    # 안전율 기준 연결
    ("spec_fs_dry", "spec_design_slope", "DERIVED_FROM", "건기 안전율 1.5 기준 근거", 0, 280),
    ("spec_fs_rain", "spec_design_slope", "DERIVED_FROM", "우기 안전율 1.3 기준 근거", 0, 280),
    ("spec_fs_seismic", "spec_design_slope", "DERIVED_FROM", "지진 안전율 1.1 기준 근거", 0, 280),

    # 지반 취약군(리스크) 연결
    ("risk_cluster_soft", "spec_design_geotech", "REGULATED_BY", "연약지반 규정 지침", 1, 241),
    ("risk_cluster_gw", "spec_design_excavation", "REGULATED_BY", "고지하수위 차수 관리기준", 1, 260),

    # 입찰/계약/평가 체계 내부 연결
    ("spec_tender_general", "contract_special_terms", "INCLUDES", "계약특수조건 포함", 0, 142),
    ("spec_tender_general", "spec_design_geotech", "INCLUDES", "실시설계지침 포함", 0, 241),
    ("contract_special_terms", "contract_unforeseen_ground", "CONSTRAINS", "지반상이 조항 규정", 0, 150),
    ("eval_award_criteria", "spec_tech_proposal_sub", "EVALUATES", "기술제안서 평가기준", 0, 586),
    ("struct_roadbed", "spec_design_track", "GOVERNED_BY", "노반-궤도 지지력 기준", 0, 310),
    ("risk_settlement_or_interface", "interface_section_boundary", "MITIGATED_BY", "인터페이스 조정 대책", 0, 497)
]

for src, tgt, rel, lbl, warn, pg in edges:
    # Check if edge already exists
    c.execute("""
        SELECT id FROM knowledge_edges 
        WHERE src_id = ? AND tgt_id = ? AND relation = ?
    """, (src, tgt, rel))
    row = c.fetchone()
    if not row:
        c.execute("""
            INSERT INTO knowledge_edges 
            (src_id, tgt_id, relation, label, is_warning, doc_name, page, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (src, tgt, rel, lbl, warn, doc_name, pg, now_str))

conn.commit()

c.execute("SELECT COUNT(id) FROM knowledge_nodes")
total_nodes = c.fetchone()[0]
c.execute("SELECT COUNT(id) FROM knowledge_edges")
total_edges = c.fetchone()[0]

print(f"Total knowledge_nodes now: {total_nodes}")
print(f"Total knowledge_edges now: {total_edges}")

conn.close()
