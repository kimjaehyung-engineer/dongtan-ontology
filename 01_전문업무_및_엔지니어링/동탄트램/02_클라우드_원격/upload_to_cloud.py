import pandas as pd
from neo4j import GraphDatabase
import logging

# 클라우드 접속 정보
URI = "bolt+s://18.192.99.27:7687"
USER = "skjh0717@gmail.com"
PASSWORD = "ssmg25rk$12#"

# 로컬 파일 경로
NODES_CSV = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\rfp_nodes.csv"
RELS_CSV = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\rfp_relationships.csv"

def upload_data():
    try:
        # 1. 데이터 로드
        nodes_df = pd.read_csv(NODES_CSV)
        rels_df = pd.read_csv(RELS_CSV)
        print(f"Loaded {len(nodes_df)} nodes and {len(rels_df)} relationships.")

        # 2. 드라이버 설정 (URI에서 SSL 설정 처리)
        driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
        
        with driver.session() as session:
            # 기존 데이터 정리 (선택 사항 - 여기서는 유지하거나 새로고침)
            print("Cleaning up old data...")
            session.run("MATCH (n) DETACH DELETE n")

            # 3. 노드 생성
            print("Creating nodes...")
            for _, row in nodes_df.iterrows():
                query = f"""
                CREATE (n:{row['Label']} {{
                    id: $id,
                    name: $name,
                    section: $section,
                    risk_level: $risk_level
                }})
                """
                session.run(query, id=row['ID'], name=row['Name'], 
                            section=row['Section'], risk_level=row['Risk_Level'])

            # 4. 인덱스 생성 (성능 최적화)
            session.run("CREATE INDEX FOR (n:Constraint) ON (n.id)")
            session.run("CREATE INDEX FOR (n:Tech_Spec) ON (n.id)")
            session.run("CREATE INDEX FOR (n:Regulation) ON (n.id)")

            # 5. 관계 생성
            print("Creating relationships...")
            for _, row in rels_df.iterrows():
                query = f"""
                MATCH (a {{id: $source}}), (b {{id: $target}})
                CREATE (a)-[r:{row['Type']}]->(b)
                """
                session.run(query, source=row['Source'], target=row['Target'])

        print("Successfully uploaded all data to Memgraph Cloud!")
        driver.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    upload_data()
