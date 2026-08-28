from importlib import import_module
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

runtime = import_module("dongtan_runtime")

def reconnect_graph():
    config = runtime.load_cloud_database_config()
    paths = runtime.load_project_paths()
    pd = import_module("pandas")
    GraphDatabase = import_module("neo4j").GraphDatabase
    print("--- [Cloud] Starting Knowledge Graph Reconnection ---")
    driver = GraphDatabase.driver(config.uri, **config.driver_kwargs())
    
    try:
        with driver.session() as session:
            # 1. 기존 데이터 초기화 (깨끗한 재시작을 위해)
            print("Cleaning up current cloud data...")
            session.run("MATCH (n) DETACH DELETE n")

            # 2. 데이터 로드 및 정규화
            nodes_df = pd.read_csv(paths.nodes_csv)
            rels_df = pd.read_csv(paths.relationships_csv)
            
            # ID 대문자화 및 공백 제거로 매칭률 극대화
            nodes_df['id'] = nodes_df['id'].str.strip().str.upper()
            rels_df['source'] = rels_df['source'].str.strip().str.upper()
            rels_df['target'] = rels_df['target'].str.strip().str.upper()

            # 3. 노드 생성 (속성 보강)
            print(f"Re-creating {len(nodes_df)} nodes...")
            for _, row in nodes_df.iterrows():
                q = """
                CREATE (n:Entity {
                    id: $id, 
                    name: $name, 
                    section: $section, 
                    risk_level: $risk_level,
                    label: $label
                })
                SET n:%s
                """ % row['label'] # 동적 라벨 부여
                session.run(q, id=row['id'], name=row['keywords'], 
                            section=row['section'], risk_level=row['risk_level'], label=row['label'])

            # 4. 인덱스 생성
            session.run("CREATE INDEX FOR (n:Entity) ON (n.id)")

            # 5. 기존 관계 복구
            print(f"Restoring {len(rels_df)} explicit relationships...")
            rel_count = 0
            for _, row in rels_df.iterrows():
                q = f"""
                MATCH (a {{id: $source}}), (b {{id: $target}})
                MERGE (a)-[r:{row['type']}]->(b)
                """
                res = session.run(q, source=row['source'], target=row['target'])
                if res.consume().counters.relationships_created > 0:
                    rel_count += 1
            print(f"Successfully connected {rel_count} explicit links.")

            # 6. [지능형 재연결] 같은 Section 내의 고립 노드들 연결
            print("Heuristic: Connecting isolated nodes in the same section...")
            session.run("""
                MATCH (a:Entity), (b:Entity)
                WHERE a.section = b.section AND a.id <> b.id
                AND NOT (a)-[]-(b)
                WITH a, b LIMIT 500
                MERGE (a)-[:RELATED_IN_SECTION]->(b)
            """)

            # 7. [지능형 재연결] 키워드 기반 교차 연결 (예: 전기 <-> 차량)
            print("Heuristic: Connecting cross-domain keywords...")
            keywords = [
                ('전기', '차량', 'POWER_FOR_VEHICLE'),
                ('토목', '정거장', 'INFRA_FOR_STATION'),
                ('신호', '안전', 'SIGNAL_FOR_SAFETY')
            ]
            for k1, k2, rel_name in keywords:
                q = f"""
                MATCH (a:Entity), (b:Entity)
                WHERE (toString(a.name) CONTAINS $k1 OR toString(a.section) CONTAINS $k1)
                  AND (toString(b.name) CONTAINS $k2 OR toString(b.section) CONTAINS $k2)
                MERGE (a)-[:{rel_name}]->(b)
                """
                session.run(q, k1=k1, k2=k2)

        print("--- [Cloud] Reconnection Completed! ---")
    except Exception as e:
        print(f"Error during reconnection: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    reconnect_graph()
