# -*- coding: utf-8 -*-
"""
9대 기술제안서 도메인 계층화(Clustering) 및 지식망 정돈 스크립트
- 59개 개별 세부과제 잎사귀(Leaf) 노드 난립으로 인한 '거미줄 및 흔들림' 현상 제거
- 9대 전문분야 대표 도메인 클러스터(PROPOSAL_DOMAIN) 9개 노드로 압축 결합
- 세부 59개 과제 리스트는 각 도메인 노드의 properties(JSON)로 내재화하여 클릭 시 우측 패널에 상세 표출
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
import sqlite3
from pathlib import Path

# Add scratch to sys.path
sys.path.insert(0, str(Path(__file__).parent))
from extract_all_proposals import extract_proposals

RAG_DIR = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
DB_PATH = RAG_DIR / "geotech_data.db"

def apply_domain_clustering():
    print("=== Step 1: 9대 기술제안서 데이터 추출 ===")
    extracted = extract_proposals()

    domain_configs = {
        "기본설계 기술제안_ 건축.pdf": {
            "id": "prop_domain_arch",
            "name": "건축",
            "emoji": "🏢",
            "label": "🏢 [건축] 기술제안",
            "group": "건축",
            "facilities": ["정거장", "본선", "차량기지", "공통"],
            "specs": [("spec_tender_general", "입찰안내서 준수"), ("interface_tram_system", "정거장-차량 인터페이스")]
        },
        "기본설계 기술제안_ 기계,소방,검수.pdf": {
            "id": "prop_domain_mech",
            "name": "기계·소방·검수",
            "emoji": "🚒",
            "label": "🚒 [기계·소방] 기술제안",
            "group": "기계·소방",
            "facilities": ["차량기지", "정거장", "공통"],
            "specs": [("spec_tender_general", "입찰안내서 준수"), ("hub_depot", "검수고 설비 연계")]
        },
        "기본설계 기술제안_ 신호.pdf": {
            "id": "prop_domain_signal",
            "name": "신호·열차제어",
            "emoji": "🚦",
            "label": "🚦 [신호] 기술제안",
            "group": "신호·시스템",
            "facilities": ["전구간", "본선", "차량기지", "공통"],
            "specs": [("spec_tender_general", "입찰안내서 준수"), ("interface_tram_system", "차상-지상 신호 인터페이스")]
        },
        "기본설계 기술제안_ 전기.pdf": {
            "id": "prop_domain_elec",
            "name": "전기·급전",
            "emoji": "⚡",
            "label": "⚡ [전기] 기술제안",
            "group": "전기·급전",
            "facilities": ["전구간", "본선", "차량기지", "공통"],
            "specs": [("spec_tender_general", "입찰안내서 준수"), ("interface_tram_system", "급전/충전 인터페이스")]
        },
        "기본설계 기술제안_ 토목구조.pdf": {
            "id": "prop_domain_struct",
            "name": "토목·구조",
            "emoji": "🌉",
            "label": "🌉 [토목구조] 기술제안",
            "group": "토목·구조",
            "facilities": ["1공구", "2공구", "본선", "공통"],
            "specs": [("spec_tender_general", "입찰안내서 준수"), ("spec_design_geotech", "구조물 지반설계기준"), ("spec_design_excavation", "가시설 안정기준")]
        },
        "기본설계 기술제안_ 토목시공.pdf": {
            "id": "prop_domain_civil",
            "name": "토목·시공",
            "emoji": "🏗️",
            "label": "🏗️ [토목시공] 기술제안",
            "group": "토목·시공",
            "facilities": ["1공구", "2공구", "본선", "공통"],
            "specs": [("spec_tender_general", "입찰안내서 준수"), ("spec_const_quality_safety", "시공품질 및 안전기준")]
        },
        "기본설계 기술제안_ 토질 및 기초.pdf": {
            "id": "prop_domain_geotech",
            "name": "토질·기초",
            "emoji": "⛰️",
            "label": "⛰️ [토질기초] 기술제안",
            "group": "토질·기초",
            "facilities": ["1공구", "2공구", "차량기지", "공통"],
            "specs": [("spec_design_geotech", "지반조사 및 기초설계기준"), ("spec_design_excavation", "흙막이 가시설 설계지침"), ("spec_design_slope", "비탈면 설계지침")]
        },
        "기본설계 기술제안_철도, 궤도.pdf": {
            "id": "prop_domain_track",
            "name": "철도·궤도",
            "emoji": "🛤️",
            "label": "🛤️ [철도궤도] 기술제안",
            "group": "철도·궤도",
            "facilities": ["1공구", "2공구", "차량기지", "공통"],
            "specs": [("spec_design_track", "트램 궤도 및 노반 설계지침"), ("interface_tram_system", "트램차량-궤도 인터페이스"), ("spec_tender_general", "입찰안내서 준수")]
        },
        "기본설계 기술제안_통신.pdf": {
            "id": "prop_domain_telecom",
            "name": "통신·LTE-R",
            "emoji": "📡",
            "label": "📡 [통신] 기술제안",
            "group": "통신·시스템",
            "facilities": ["전구간", "본선", "차량기지", "공통"],
            "specs": [("spec_tender_general", "입찰안내서 준수"), ("interface_tram_system", "LTE-R 및 영상감시 연계")]
        }
    }

    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    # 1. Clean up old 59 individual leaf proposal nodes and edges
    print("\n=== Step 2: 기존 59개 난립 잎사귀 노드 및 엣지 정돈 ===")
    cur.execute("DELETE FROM knowledge_nodes WHERE type = 'TechnicalProposal'")
    cur.execute("DELETE FROM knowledge_edges WHERE src_id LIKE 'prop_%'")
    print(" - 기존 59개 개별 잎사귀 노드 제거 완료 (노드 59개 ➔ 도메인 클러스터 9개로 압축)")

    # 2. Insert/Update Root Hub
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
        "📋 9대 기본설계 기술제안 (종합)",
        "PROPOSAL_HUB",
        "건축, 신호, 전기, 궤도, 통신, 기계, 토목구조, 토목시공, 토질기초 9대 전문분야 기술제안 총괄 허브",
        "proposal",
        "공통, 전구간",
        "02_기본설계_기술제안",
        1,
        json.dumps({"total_domains": 9, "total_proposals": 59}, ensure_ascii=False)
    ))

    # 3. Insert 9 Domain Clusters
    print("\n=== Step 3: 9대 도메인 클러스터 노드 및 엄선된 엣지 등록 ===")
    domain_count = 0
    edge_count = 0

    for doc_name, conf in domain_configs.items():
        doc_data = extracted.get(doc_name, {"total_pages": 1, "sections": []})
        sections = doc_data["sections"]
        sub_tasks = [s["title"] for s in sections if s.get("task_id")]
        
        # Build readable summary description
        desc_lines = [
            f"분야: {conf['emoji']} {conf['name']} 기술제안",
            f"문서: {doc_name} (총 {doc_data['total_pages']}p / 제안과제 {len(sections)}건)",
            f"주요 제안과제:"
        ]
        for s in sections[:6]:
            desc_lines.append(f" • {s['title']} (p.{s['start_page']}~{s['end_page']})")
        if len(sections) > 6:
            desc_lines.append(f" • 외 {len(sections)-6}건 추가 과제 포함")

        props = {
            "doc_name": doc_name,
            "total_pages": doc_data["total_pages"],
            "total_items": len(sections),
            "items": sections
        }

        node_id = conf["id"]
        node_label = f"{conf['label']} ({len(sections)}건)"
        fac_str = ", ".join(conf["facilities"])

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
            node_label,
            "PROPOSAL_DOMAIN",
            "\n".join(desc_lines),
            conf["group"],
            fac_str,
            doc_name,
            1,
            json.dumps(props, ensure_ascii=False)
        ))
        domain_count += 1

        # 4. Clean Edges
        # 1) Connect to Root Hub
        cur.execute("""
        INSERT INTO knowledge_edges (src_id, tgt_id, relation, label, is_warning, doc_name, page)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (node_id, "hub_proposals", "INCLUDED_IN", "기술제안 포함", 0, doc_name, 1))
        edge_count += 1

        # 2) Connect to core facilities
        if "차량기지" in fac_str:
            cur.execute("""
            INSERT INTO knowledge_edges (src_id, tgt_id, relation, label, is_warning, doc_name, page)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (node_id, "hub_depot", "APPLIED_TO", "차량기지 적용", 0, doc_name, 1))
            edge_count += 1

        if "본선" in fac_str or "1공구" in fac_str:
            cur.execute("""
            INSERT INTO knowledge_edges (src_id, tgt_id, relation, label, is_warning, doc_name, page)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (node_id, "hub_sec1", "APPLIED_TO", "1공구 본선 적용", 0, doc_name, 1))
            edge_count += 1

        if "본선" in fac_str or "2공구" in fac_str:
            cur.execute("""
            INSERT INTO knowledge_edges (src_id, tgt_id, relation, label, is_warning, doc_name, page)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (node_id, "hub_sec2", "APPLIED_TO", "2공구 본선 적용", 0, doc_name, 1))
            edge_count += 1

        # 3) Connect to core standards & specs
        for spec_tgt, spec_lbl in conf["specs"]:
            cur.execute("""
            INSERT INTO knowledge_edges (src_id, tgt_id, relation, label, is_warning, doc_name, page)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (node_id, spec_tgt, "GOVERNED_BY", spec_lbl, 0, doc_name, 1))
            edge_count += 1

    conn.commit()
    conn.close()
    print(f"✅ 도메인 클러스터링 완료! (도메인 허브 {domain_count}개, 핵심 연결 엣지 {edge_count}개 등록)")

if __name__ == "__main__":
    apply_domain_clustering()
