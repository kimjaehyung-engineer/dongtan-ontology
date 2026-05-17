from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

def force_connect_isolated():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        print("RODO: Starting Forced Compression Connection (UTF-8)...")
        
        # 연결 대상 정의 (스크린샷 기반)
        targets = [
            {'kw': '일상검사', 'hub': '도시기반시설 유지관리 및 보수공사'},
            {'kw': '복공판', 'hub': '동탄 지하차도'},
            {'kw': 'TCMS', 'hub': '차량 및 전동차 관련 제약'},
            {'kw': '비디오 월', 'hub': '인프라/관제'},
            {'kw': 'Hot Standby', 'hub': '주요 설비/전기'},
            {'kw': '유도블록', 'hub': '도로의 및 가로등'}
        ]
        
        # 프로젝트 루트 (DONGTAN_TRAM_PROJECT)
        session.run("MERGE (root:Project {name: '동탄트램 사업'})")
        
        for item in targets:
            kw = item['kw']
            hub = item['hub']
            print(f"RODO: Force linking items containing '{kw}' using REGEX...")
            
            # 정규표현식 패턴 생성 (일상검사/감사 모두 대응)
            regex_pattern = f".*{kw}.*"
            if kw == '일상검사':
                regex_pattern = ".*일상.*[검|감]사.*"

            # 1. 허브에 연결
            q_hub = """
            MATCH (h {name: $hub_name}), (o)
            WHERE o.name =~ $pattern
            MERGE (o)-[:HUB_LINK]->(h)
            """
            session.run(q_hub, hub_name=hub, pattern=regex_pattern)
            
            # 2. 프로젝트 루트에 연결
            q_root = """
            MATCH (root:Project {name: '동탄트램 사업'}), (o)
            WHERE o.name =~ $pattern
            MERGE (o)-[:PART_OF_PROJECT]->(root)
            """
            session.run(q_root, pattern=regex_pattern)
            
        print("RODO: Forced Compression Connection Completed!")
    driver.close()

if __name__ == "__main__":
    force_connect_isolated()
