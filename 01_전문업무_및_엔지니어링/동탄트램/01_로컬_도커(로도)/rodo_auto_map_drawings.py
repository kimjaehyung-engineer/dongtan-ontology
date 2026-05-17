import os
import glob
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

# 실제 설계서가 위치한 루트 경로
BASE_DIR = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\04_설계서"

def auto_map_drawings():
    """폴더 구조를 스캔하여 지식망 허브 노드와 매핑"""
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    # 1. 실제 파일 스캔
    # 공구 및 분야별로 PDF 파일을 찾습니다.
    search_pattern = os.path.join(BASE_DIR, "**", "*.pdf")
    pdf_files = glob.glob(search_pattern, recursive=True)
    
    print(f"RODO: 총 {len(pdf_files)}개의 실제 설계서(PDF)를 발견했습니다.")
    if not pdf_files:
        print("RODO: 연결할 PDF 파일이 없습니다. 폴더에 도면을 추가한 후 다시 실행하세요.")
        driver.close()
        return

    # 2. 분류 및 매핑 로직
    # 분야별 키워드 확장 (동의어)
    keyword_map = {
        "건축": ['건축', '정거장', 'PSD'],
        "궤도": ['궤도', '분기기', '레일'],
        "전기": ['전기', '전압', 'DC', '급전'],
        "차량": ['차량', '동력', '대차'],
        "통신": ['통신', '네트워크', '광케이블', 'CCTV'],
        "신호": ['신호', '관제', '우선신호', 'ATO'],
        "소방": ['소방', '소화', '방재'],
        "기반시설": ['기반시설', '토목', '구조물', '지하차도']
    }

    with driver.session() as session:
        for file_path in pdf_files:
            # 윈도우 경로 구분자를 표준화
            normalized_path = file_path.replace("\\", "/")
            filename = os.path.basename(normalized_path)
            
            # 폴더 구조에서 공구 및 분야 추출 (예: 1공구/통신)
            rel_path = os.path.relpath(file_path, BASE_DIR).replace("\\", "/")
            parts = rel_path.split("/")
            sector = parts[1] if len(parts) >= 2 else "공통"
            
            # 분야별 동의어 키워드 가져오기 (없으면 폴더명 자체를 키워드로 사용)
            keywords = keyword_map.get(sector, [sector])
            
            # Cypher 쿼리 동적 생성 (모든 PDF는 Document 노드로 무조건 생성)
            where_clause = " OR ".join([f"n.name CONTAINS '{kw}'" for kw in keywords])
            
            query = f"""
            MERGE (d:Document {{file_path: $path}})
            ON CREATE SET d.name = $filename, d.mapped_from = '자동매핑(' + $sector + ')'
            WITH d
            OPTIONAL MATCH (n) WHERE NOT 'Document' IN labels(n) AND ({where_clause})
            FOREACH (_ IN CASE WHEN n IS NOT NULL THEN [1] ELSE [] END |
                MERGE (n)-[:HAS_DOCUMENT]->(d)
            )
            RETURN count(n) as cnt
            """
            
            res = session.run(query, path=normalized_path, filename=filename, sector=sector)
            updated_count = res.single()['cnt']
            
            if updated_count > 0:
                print(f"Success [{sector}]: {filename} -> {updated_count} nodes connected.")
            else:
                print(f"Success [{sector}]: {filename} -> Document created (0 connections).")

    driver.close()
    print("\nRODO: 설계서 폴더 스캔 및 지식망 오토매핑(Auto-Mapping)이 완료되었습니다!")

if __name__ == "__main__":
    auto_map_drawings()
