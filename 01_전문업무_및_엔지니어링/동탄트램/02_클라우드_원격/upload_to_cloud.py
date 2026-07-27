from importlib import import_module
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

runtime = import_module("dongtan_runtime")

def upload_data():
    config = runtime.load_cloud_database_config()
    paths = runtime.load_project_paths()
    pd = import_module("pandas")
    GraphDatabase = import_module("neo4j").GraphDatabase
    try:
        # 1. 데이터 로드
        nodes_df = pd.read_csv(paths.nodes_csv)
        rels_df = pd.read_csv(paths.relationships_csv)
        print(f"Loaded {len(nodes_df)} nodes and {len(rels_df)} relationships.")

        # 2. 드라이버 설정 (URI에서 SSL 설정 처리)
        driver = GraphDatabase.driver(config.uri, **config.driver_kwargs())
        
        with driver.session() as session:
            # 기존 데이터 정리 (선택 사항 - 여기서는 유지하거나 새로고침)
            print("Cleaning up old data...")
            session.run("MATCH (n) DETACH DELETE n")

            # 3. 노드 생성
            print("Creating nodes...")
            for _, row in nodes_df.iterrows():
                query = f"""
                CREATE (n:{row['label']} {{
                    id: $id,
                    name: $name,
                    section: $section,
                    risk_level: $risk_level
                }})
                """
                session.run(query, id=row['id'], name=row['keywords'],
                            section=row['section'], risk_level=row['risk_level'])

            # 4. 인덱스 생성 (성능 최적화)
            session.run("CREATE INDEX FOR (n:Constraint) ON (n.id)")
            session.run("CREATE INDEX FOR (n:Tech_Spec) ON (n.id)")
            session.run("CREATE INDEX FOR (n:Regulation) ON (n.id)")

            # 5. 관계 생성
            print("Creating relationships...")
            for _, row in rels_df.iterrows():
                query = f"""
                MATCH (a {{id: $source}}), (b {{id: $target}})
                CREATE (a)-[r:{row['type']}]->(b)
                """
                session.run(query, source=row['source'], target=row['target'])

        print("Successfully uploaded all data to Memgraph Cloud!")
        driver.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    upload_data()
