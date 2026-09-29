import sqlite3
import json
from pathlib import Path

DB_PATH = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\geotech_data.db")

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def build_master_graph(section=None, risk_only=False):
    """
    동탄 트램 지반-공종 지식 그래프 생성 엔진 (온톨로지 최적화 버전)
    - 슈퍼노드 병목(지층 5개 노드 150여 개 엣지) 제거 -> 시추공 속성(Property)으로 흡수
    - 1:1 파편화된 위험노드(32개) -> 2대 공통 리스크 마스터 클러스터로 통합
    - 노드 수: 118개 -> 83개 / 엣지 수: 236개 -> 109개 (복잡도 54% 경감)
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # 1. 시추공 로드
    query = """
        SELECT b.id, b.doc_name, b.hole_no, b.facility, b.page_start, b.page_end, 
               b.elevation_m, b.groundwater_m, b.total_depth_m
        FROM boreholes b
        ORDER BY b.id
    """
    boreholes = cur.execute(query).fetchall()

    # 2. 연약층(N<6 @ depth<=3m) 데이터 로드
    soft_records = cur.execute("""
        SELECT hole_no, depth_m, n_value, n_str
        FROM spt_records
        WHERE depth_m <= 3.0 AND n_value < 6
        ORDER BY depth_m ASC
    """).fetchall()

    soft_map = {}
    for r in soft_records:
        h = r["hole_no"]
        if h not in soft_map:
            soft_map[h] = []
        soft_map[h].append({"depth": r["depth_m"], "n": r["n_value"], "n_str": r["n_str"]})

    # 3. 고지하수위(GL - 3.0m 이내) 감지
    high_gw_map = {}
    for b in boreholes:
        if b["groundwater_m"] is not None and 0 < b["groundwater_m"] <= 3.0:
            high_gw_map[b["hole_no"]] = b["groundwater_m"]

    # 4. 시추공별 지층 정보 집계 (속성용)
    strata_records = cur.execute("""
        SELECT hole_no, stratum_name, depth_top_m, depth_bottom_m
        FROM strata_layers
        ORDER BY hole_no, depth_top_m
    """).fetchall()

    strata_map = {}
    for s in strata_records:
        h = s["hole_no"]
        if h not in strata_map:
            strata_map[h] = []
        if s["stratum_name"] not in strata_map[h]:
            strata_map[h].append(s["stratum_name"])

    # conn 유지

    # 노드 및 엣지 빌드
    nodes = []
    edges = []
    node_set = set()

    def add_node(n_id, label, n_type, desc="", group="", extra=None):
        if n_id not in node_set:
            node_set.add(n_id)
            node_data = {
                "id": n_id,
                "label": label,
                "type": n_type,
                "description": desc,
                "group": group
            }
            if extra:
                node_data.update(extra)
            nodes.append(node_data)

    def add_edge(src, tgt, relation, label="", is_warning=False):
        edges.append({
            "from": src,
            "to": tgt,
            "relation": relation,
            "label": label,
            "is_warning": is_warning
        })

    # 1) 공간/구간 마스터 허브 노드 (4개)
    structures = {
        "hub_depot": {"label": "동탄 차량기지 (기본 GB)", "type": "DESIGN_ELEMENT", "desc": "1공구 차량기지 기본설계 부지 (GB-1~9)"},
        "hub_prop_depot": {"label": "차량기지 제안설계 (NGB)", "type": "DESIGN_ELEMENT", "desc": "입찰 제안설계 당시 차량기지 사전조사 (NGB-1~5)"},
        "hub_sec1": {"label": "1공구 본선 (NH)", "type": "DESIGN_ELEMENT", "desc": "1공구 본선 및 오산천 횡단구간 (NH-1~36)"},
        "hub_sec2": {"label": "2공구 본선 (DT)", "type": "DESIGN_ELEMENT", "desc": "2공구 동탄역 환승 및 정거장 구간 (DT-1~27)"}
    }
    for hid, hdata in structures.items():
        add_node(hid, hdata["label"], hdata["type"], hdata["desc"], group="structure")

    # 2) 2대 공통 리스크 마스터 클러스터 노드
    risk_clusters = {
        "risk_cluster_soft": {
            "label": "⚠️ 표층 연약지반 취약군 (N<6)",
            "type": "DISCREPANCY",
            "desc": "지표하 3.0m 이내 N<6인 시추공 군집. 본선 궤도/차량기지 기초 지지력 부족 및 침하·측방유동 검토 대상 (총 27개소 집중)",
            "group": "risk"
        },
        "risk_cluster_gw": {
            "label": "💧 고지하수위 취약군 (GL-3.0m)",
            "type": "DISCREPANCY",
            "desc": "지하수위 GL -3.0m 이내인 시추공 군집. 지하 굴착 시 지하수 유입, 양압력 및 보일링/파이핑 검토 대상 (총 5개소 집중)",
            "group": "risk"
        }
    }
    for rid, rdata in risk_clusters.items():
        add_node(rid, rdata["label"], rdata["type"], rdata["desc"], group="risk")

    discrepancy_list = []
    connected_risk_soft = 0
    connected_risk_gw = 0

    for b in boreholes:
        hole = b["hole_no"]
        is_prop_depot = hole.startswith("NGB")
        is_depot = hole.startswith("GB")
        is_sec1 = hole.startswith("NH")
        is_sec2 = hole.startswith("DT")

        # 필터링 조건
        if section == "proposals":
            continue
        if section == "1" and not (is_sec1 or is_depot):
            continue
        if section == "depot" and not (is_depot or is_prop_depot):
            continue
        if section == "prop" and not is_prop_depot:
            continue
        if section == "2" and not is_sec2:
            continue

        has_soft = hole in soft_map
        has_gw = hole in high_gw_map
        has_risk = has_soft or has_gw

        if risk_only and not has_risk:
            continue

        # 소속 허브 결정
        if is_prop_depot:
            hub_id = "hub_prop_depot"
        elif is_depot:
            hub_id = "hub_depot"
        elif is_sec1:
            hub_id = "hub_sec1"
        else:
            hub_id = "hub_sec2"

        # 지층 정보 (노드가 아닌 속성으로 결합)
        layers = strata_map.get(hole, [])
        strata_text = " → ".join(layers) if layers else "지층 정보 미등록"

        # 시추공 노드 설명 구성
        desc_lines = [
            f"공번: {hole} ({b['facility']})",
            f"심도: {b['total_depth_m']}m" + (f" / 표고: {b['elevation_m']}m" if b['elevation_m'] else ""),
            f"지하수위: GL -{b['groundwater_m']}m" if b['groundwater_m'] else "지하수위: 미확인",
            f"관통지층: {strata_text}",
            f"원본: {b['doc_name']} (p.{b['page_start']})"
        ]
        if has_soft:
            min_s = soft_map[hole][0]
            desc_lines.append(f"⚠️ 표층 연약층: 심도 {min_s['depth']}m (N={min_s['n']})")
        if has_gw:
            desc_lines.append(f"💧 고지하수위: GL -{high_gw_map[hole]}m")

        add_node(
            f"bh_{hole}",
            hole,
            "BORING",
            desc="\n".join(desc_lines),
            group="borehole",
            extra={
                "hole_no": hole,
                "doc_name": b["doc_name"],
                "page": b["page_start"],
                "elevation": b["elevation_m"],
                "groundwater": b["groundwater_m"],
                "depth": b["total_depth_m"],
                "strata": layers,
                "has_risk": has_risk,
                "facility": b["facility"]
            }
        )

        # 구간 허브와 연결
        add_edge(hub_id, f"bh_{hole}", "LOCATED_IN", label="위치")

        # 공통 리스크 클러스터와 연결 (과설계 제거 및 클러스터링)
        if has_soft:
            s_info = soft_map[hole][0]
            phase_tag = "[제안설계]" if is_prop_depot else "[기본설계]"
            add_edge(f"bh_{hole}", "risk_cluster_soft", "HAS_RISK", label=f"N={s_info['n']}", is_warning=True)
            discrepancy_list.append(f"{phase_tag} [{hole}] 지하 {s_info['depth']}m에서 N={s_info['n']} 초연약층 확인 (p.{b['page_start']})")
            connected_risk_soft += 1

        if has_gw:
            gw_val = high_gw_map[hole]
            add_edge(f"bh_{hole}", "risk_cluster_gw", "HIGH_GROUNDWATER", label=f"GL-{gw_val}m", is_warning=True)
            discrepancy_list.append(f"[{hole}] 고지하수위 GL-{gw_val}m 감지 (p.{b['page_start']})")
            connected_risk_gw += 1


    # 5) 동적으로 확장된 문서 지식망 노드 및 엣지 결합
    try:
        cur_k = conn.cursor()
        # 테이블 존재 여부 확인
        tbl_check = cur_k.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='knowledge_nodes'").fetchone()
        if tbl_check:
            k_nodes = cur_k.execute("SELECT id, label, type, description, group_name, facility, doc_name, page, properties FROM knowledge_nodes").fetchall()
            for kn in k_nodes:
                k_fac = kn["facility"] or ""
                k_type = kn["type"] or ""
                if section == "geotech" and "PROPOSAL" in k_type:
                    continue
                if section == "1" and "1공구" not in k_fac and "공통" not in k_fac:
                    continue
                if section == "2" and "2공구" not in k_fac and "공통" not in k_fac:
                    continue
                if section in ("depot", "prop") and "차량기지" not in k_fac and "공통" not in k_fac:
                    continue

                extra_props = {}
                if kn["properties"]:
                    try: extra_props = json.loads(kn["properties"])
                    except Exception: pass
                extra_props["doc_name"] = kn["doc_name"]
                extra_props["page"] = kn["page"]
                extra_props["facility"] = kn["facility"]

                add_node(
                    kn["id"],
                    kn["label"],
                    kn["type"],
                    desc=kn["description"] or "",
                    group=kn["group_name"] or kn["type"].lower(),
                    extra=extra_props
                )

            k_edges = cur_k.execute("SELECT src_id, tgt_id, relation, label, is_warning, doc_name, page FROM knowledge_edges").fetchall()
            for ke in k_edges:
                # 연결될 노드가 존재하는지 확인 후 엣지 추가
                if ke["src_id"] in node_set and ke["tgt_id"] in node_set:
                    add_edge(
                        ke["src_id"],
                        ke["tgt_id"],
                        ke["relation"],
                        label=ke["label"] or "",
                        is_warning=bool(ke["is_warning"])
                    )
    except Exception as e:
        print(f"[graph_engine] 동적 지식 노드 로딩 실패: {e}")
    finally:
        try: conn.close()
        except Exception: pass

    summary_text = (
        f"동탄 트램 지식 그래프 (온톨로지 최적화): 4대 구간 허브 + 시추공 {len([n for n in nodes if n['type']=='BORING'])}개 + 2대 리스크 클러스터 구성 완료. "
        f"지층 데이터는 시추공 속성(Property)으로 내재화하여 거미줄 엣지를 제거하였으며, "
        f"연약층(N<6) {connected_risk_soft}개소 및 고지하수위 {connected_risk_gw}개소가 공통 위험 클러스터로 정돈되었습니다."
    )

    return {
        "nodes": nodes,
        "edges": edges,
        "summary": summary_text,
        "discrepancies": discrepancy_list,
        "stats": {
            "total_boreholes": len([n for n in nodes if n['type'] == 'BORING']),
            "risk_boreholes": len([n for n in nodes if n['type'] == 'BORING' and n.get('has_risk')]),
            "soft_ground_count": len(soft_map),
            "high_gw_count": len(high_gw_map)
        }
    }

if __name__ == "__main__":
    res = build_master_graph()
    print("=== Optimized Ontology Master Graph ===")
    print("Total Nodes:", len(res["nodes"]))
    print("Total Edges:", len(res["edges"]))
    print("Stats:", res["stats"])
    print("Discrepancies count:", len(res["discrepancies"]))
