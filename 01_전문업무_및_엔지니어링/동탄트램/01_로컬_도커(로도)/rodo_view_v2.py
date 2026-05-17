import sys
import os
import urllib.parse
from neo4j import GraphDatabase
import subprocess

# UTF-8 출력 강제 (윈도우 콘솔 한글 깨짐 방지)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

# 검색을 위한 기본 매핑 딕셔너리
BASE_PATHS = {
    "01. 설계보고서(건축).pdf": r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\04_설계서\1공구\건축",
    "01. 설계보고서_궤도.pdf": r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\04_설계서\1공구\궤도",
    "01. 종합요약보고서.pdf": r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\04_설계서\1공구\토목"
}

def view_risks(search_type, search_keyword):
    print("=" * 75)
    print(" 📂 [RODO] 다차원 리스크(Risk) & 근거 문서 통합 조회 엔진")
    print("=" * 75)
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    with driver.session() as session:
        if search_type == "위치":
            query = """
            MATCH (r:Risk)-[:OCCURS_AT]->(loc:Location)
            WHERE loc.name CONTAINS $keyword
            MATCH (r)-[:BELONGS_TO]->(disc:Discipline)
            MATCH (r)-[:VIOLATES]->(s:Standard)
            MATCH (r)-[ev:EVIDENCE_IN]->(doc:Document)
            RETURN r.name AS risk_name, loc.name AS location, disc.name AS discipline,
                   s.name AS std_name, s.limit_value AS limit, s.unit AS unit,
                   r.actual_value AS actual, r.issue_description AS issue,
                   doc.name AS doc_name, doc.absolute_path AS doc_path, ev.page AS page
            """
        elif search_type == "공종":
            query = """
            MATCH (r:Risk)-[:BELONGS_TO]->(disc:Discipline)
            WHERE disc.name CONTAINS $keyword
            MATCH (r)-[:OCCURS_AT]->(loc:Location)
            MATCH (r)-[:VIOLATES]->(s:Standard)
            MATCH (r)-[ev:EVIDENCE_IN]->(doc:Document)
            RETURN r.name AS risk_name, loc.name AS location, disc.name AS discipline,
                   s.name AS std_name, s.limit_value AS limit, s.unit AS unit,
                   r.actual_value AS actual, r.issue_description AS issue,
                   doc.name AS doc_name, doc.absolute_path AS doc_path, ev.page AS page
            """
        else:
            print("검색 타입은 '위치' 또는 '공종' 이어야 합니다.")
            return

        result = session.run(query, keyword=search_keyword)
        records = list(result)
        
        if not records:
            print(f"❌ [알림] '{search_keyword}'에 해당하는 {search_type} 리스크가 등록되어 있지 않습니다.")
            print("=" * 75)
            return
            
        print(f"🎉 총 {len(records)}개의 위배 사항 및 근거 문서를 지식망(Graph)에서 찾았습니다!\n")
        
        for idx, r in enumerate(records, 1):
            print(f"[{idx}] 분야: {r['discipline']} | 위치: {r['location']}")
            print(f"  🚨 리스크 항목: {r['std_name'].replace('표준: ', '')}")
            print(f"  📝 위배 내용  : {r['issue']}")
            print(f"  📊 기준값 비교 : 한계 기준 {r['limit']}{r['unit']} | 실제 기본설계 값 {r['actual']}{r['unit']}")
            print(f"  -------------------------------------------------------------")
            print(f"  📜 [출처 및 근거 자료 (지식망 연계)]")
            print(f"   - 파 일 명 : {r['doc_name']}")
            print(f"   - 근거페이지: Page {r['page']}")
            print(f"   - 로컬 경로 : {r['doc_path']}")
            print("-" * 75)
            
    driver.close()
    print("\n" + "=" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("사용법: python rodo_view_v2.py [위치/공종] [검색어]")
        print("예시: python rodo_view_v2.py 공종 궤도")
        print("예시: python rodo_view_v2.py 위치 304")
        sys.exit(1)
        
    search_type = sys.argv[1]
    keyword = sys.argv[2]
    view_risks(search_type, keyword)
