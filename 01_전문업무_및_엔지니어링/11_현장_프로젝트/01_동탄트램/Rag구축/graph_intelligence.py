# -*- coding: utf-8 -*-
"""
지식망(Graph)과 메타 색인(Index)의 유기적 결합 강화 모듈
Graph-Guided Index Retrieval (지식망 기반 색인 가이드 파이프라인)
"""
import sqlite3
import re
from pathlib import Path

DB_PATH = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\geotech_data.db")

def extract_graph_intelligence(query: str):
    """
    질문 텍스트로부터 지식망(Graph DB)의 핵심 노드, 구간 허브, 위험 클러스터를 선제적으로 탐색하여
    색인(Index) 스코어링에 주입할 '지식망 인텔리전스(가중치 데이터)'를 반환합니다.
    """
    q_lower = query.lower()
    
    # 1. 대상 구간/허브 판별
    is_depot = any(k in q_lower for k in ["차량기지", "기지", "gb", "ngb"])
    is_prop = any(k in q_lower for k in ["제안설계", "입찰", "ngb", "대안"])
    is_sec1 = any(k in q_lower for k in ["1공구", "본선1", "오산천", "nh"])
    is_sec2 = any(k in q_lower for k in ["2공구", "동탄역", "환승", "dt"])
    
    # 2. 리스크 유형 판별
    is_soft_ground = any(k in q_lower for k in ["연약", "n치", "n<", "n=", "침하", "지지력", "spt", "토질", "점성토"])
    is_high_gw = any(k in q_lower for k in ["지하수", "수위", "차수", "보일링", "파이핑", "양압력", "유입", "배수"])
    
    matched_holes = set()
    target_docs = set()
    target_pages = []
    reasoning_summary = []
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # 특정 시추공 직접 언급 시
        holes_in_q = re.findall(r'(?:NH|DT|GB|NGB)-?\d+', query, re.IGNORECASE)
        for h in holes_in_q:
            clean_h = h.upper().replace(" ", "")
            if not clean_h.startswith(("NH-", "DT-", "GB-", "NGB-")):
                # NH1 -> NH-1
                clean_h = re.sub(r'([A-Z]+)(\d+)', r'\1-\2', clean_h)
            matched_holes.add(clean_h)
        
        # 연약지반 리스크 클러스터 쿼리
        if is_soft_ground:
            sql = """
                SELECT DISTINCT s.hole_no, b.doc_name, b.page_start, s.depth_m, s.n_value
                FROM spt_records s
                JOIN boreholes b ON s.hole_no = b.hole_no
                WHERE s.depth_m <= 3.0 AND s.n_value < 6
            """
            rows = cur.execute(sql).fetchall()
            for r in rows:
                h = r["hole_no"]
                # 구간 필터링
                if is_prop and not h.startswith("NGB"): continue
                if is_depot and not (h.startswith("GB") or h.startswith("NGB")): continue
                if is_sec1 and not h.startswith("NH"): continue
                if is_sec2 and not h.startswith("DT"): continue
                
                matched_holes.add(h)
                target_docs.add(r["doc_name"])
                target_pages.append(r["page_start"])
            
            reasoning_summary.append(f"연약지반 위험군(N<6) {len(matched_holes)}개 시추공 추출")

        # 고지하수위 리스크 클러스터 쿼리
        if is_high_gw:
            sql = """
                SELECT hole_no, doc_name, page_start, groundwater_m
                FROM boreholes
                WHERE groundwater_m IS NOT NULL AND groundwater_m > 0 AND groundwater_m <= 3.0
            """
            rows = cur.execute(sql).fetchall()
            for r in rows:
                h = r["hole_no"]
                if is_prop and not h.startswith("NGB"): continue
                if is_depot and not (h.startswith("GB") or h.startswith("NGB")): continue
                if is_sec1 and not h.startswith("NH"): continue
                if is_sec2 and not h.startswith("DT"): continue
                
                matched_holes.add(h)
                target_docs.add(r["doc_name"])
                target_pages.append(r["page_start"])
            
            reasoning_summary.append(f"고지하수위(GL-3m) 취약군 {len(matched_holes)}개소 추출")

        conn.close()
    except Exception as e:
        print(f"[Graph Intelligence Error]: {e}")

    return {
        "matched_holes": list(matched_holes),
        "target_docs": list(target_docs),
        "target_pages": target_pages,
        "is_depot": is_depot,
        "is_prop": is_prop,
        "is_sec1": is_sec1,
        "is_sec2": is_sec2,
        "is_soft_ground": is_soft_ground,
        "is_high_gw": is_high_gw,
        "summary": ", ".join(reasoning_summary) if reasoning_summary else "일반 엔지니어링 질의 탐색"
    }

if __name__ == "__main__":
    q1 = "차량기지 연약지반 시추공 N값 알려줘"
    res1 = extract_graph_intelligence(q1)
    print("Test 1 (차량기지 연약지반):")
    print(" - Matched holes:", res1["matched_holes"])
    print(" - Target docs:", res1["target_docs"])
    print(" - Target pages count:", len(res1["target_pages"]))
    print(" - Summary:", res1["summary"])

    q2 = "1공구 오산천 구간 고지하수위 시추공"
    res2 = extract_graph_intelligence(q2)
    print("\nTest 2 (1공구 고지하수위):")
    print(" - Matched holes:", res2["matched_holes"])
    print(" - Target docs:", res2["target_docs"])
    print(" - Summary:", res2["summary"])
