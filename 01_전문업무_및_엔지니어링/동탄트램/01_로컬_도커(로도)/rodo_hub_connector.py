from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

def hub_connector():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        print("RODO: Starting Precision Hub Connection...")
        
        # 허브 키워드 및 매칭 규칙
        hub_rules = [
            ('차량 및 전동차 관련 제약', ['차량', '전동차', '트램', '제약', '운행', 'TCMS', '시험기']),
            ('주요 설비/전기', ['전기', '설비', '전력', '기계', '이중계', 'Standby']),
            ('전력 계통 및 변전 시설', ['전력', '변전', '급전', '계통', '전기']),
            ('도로의 및 가로등', ['도로', '가로등', '등주', '교통', '보도', '유도블록', '안내']),
            ('동탄 지하차도', ['지하차도', '터널', '하부', '신도시', '복공판', '방음벽']),
            ('도시기반시설 유지관리 및 보수공사', ['유지관리', '보수', '관리', '시설', '공사']),
            ('기동지구', ['기동', '부대시설', '변기', '화장실', '설비', '건축']),
            ('인프라/관제', ['인프라', '시설', '구조', '토목', '기존', '비디오 월', '지령실', '관제'])
        ]
        
        for hub_kw, target_kws in hub_rules:
            print(f"RODO: Linking hub nodes containing '{hub_kw}'...")
            for t_kw in target_kws:
                q = """
                MATCH (hub)
                WHERE hub.name CONTAINS $hub_kw
                MATCH (target)
                WHERE target <> hub AND target.name CONTAINS $t_kw
                MERGE (target)-[:HUB_LINK {source: 'RODO_HEURISTIC'}]->(hub)
                """
                session.run(q, hub_kw=hub_kw, t_kw=t_kw)
                
        print("RODO: Precision Hub Connection Completed!")
    driver.close()

if __name__ == "__main__":
    hub_connector()
