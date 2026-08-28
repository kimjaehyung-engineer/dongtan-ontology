import json
from importlib import import_module
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

runtime = import_module("dongtan_runtime")

# ==========================================
# 🌌 [DONGTAN TRAM] CLOUD GRAPH AGENT
# ==========================================
# 특징: 
# 1. Memgraph Cloud(원격)와 직접 통신
# 2. 로컬 데이터를 클라우드로 업로드 (--upload)
# 3. 클라우드 데이터를 재사용 가능한 JSON 파일로 내보내기
# 4. 클라우드 서버에 Cypher 쿼리 직접 실행
# ==========================================

def run_cloud_agent(command=None, query=None):
    config = runtime.load_cloud_database_config()
    paths = runtime.load_project_paths()
    pd = import_module("pandas")
    GraphDatabase = import_module("neo4j").GraphDatabase

    print(f"--- [Cloud] Connecting to Memgraph Cloud ({config.uri}) ---")
    driver = GraphDatabase.driver(config.uri, **config.driver_kwargs())
    
    try:
        with driver.session() as session:
            # [기능 1] 로컬 데이터를 클라우드로 강제 업로드
            if command == "upload":
                print(f"Action: Uploading local CSVs to Cloud...")
                if not paths.nodes_csv.exists() or not paths.relationships_csv.exists():
                    print(f"Error: CSV files not found at {paths.nodes_csv}")
                    return

                nodes_df = pd.read_csv(paths.nodes_csv)
                rels_df = pd.read_csv(paths.relationships_csv)
                
                print("Cleaning existing data in Cloud...")
                session.run("MATCH (n) DETACH DELETE n")
                
                print(f"Creating {len(nodes_df)} nodes...")
                for _, row in nodes_df.iterrows():
                    q = f"CREATE (n:{row['label']} {{id: $id, name: $name, section: $section, risk_level: $risk_level}})"
                    session.run(q, id=row['id'], name=row['keywords'], section=row['section'], risk_level=row['risk_level'])
                
                print(f"Creating {len(rels_df)} relationships...")
                for _, row in rels_df.iterrows():
                    q = f"MATCH (a {{id: $source}}), (b {{id: $target}}) CREATE (a)-[r:{row['type']}]->(b)"
                    session.run(q, source=row['source'], target=row['target'])
                
                print("Cloud Data Upload Completed Successfully!")

            # [기능 2] Cypher 쿼리 실행
            elif query:
                print(f"Action: Executing Cloud Cypher Query: {query}")
                result = session.run(query)
                records = list(result)
                if records:
                    print(f"Results ({len(records)}):")
                    for record in records[:5]:
                        print(f"  > {record}")
                    if len(records) > 5: print("  ... (truncated)")
                else:
                    print("Query executed (no records returned).")

            # [기능 3] 클라우드 데이터를 JSON으로 내보내기 (기본 동작)
            print(f"Action: Exporting Cloud Graph to {paths.ontology_output}...")
            result = session.run("""
                MATCH (s)-[p]->(o)
                RETURN 
                    COALESCE(s.name, toString(id(s))) AS subject,
                    type(p) AS predicate,
                    COALESCE(o.name, toString(id(o))) AS object
            """)
            
            ontology_data = []
            for record in result:
                ontology_data.append({
                    "subject": record["subject"],
                    "predicate": record["predicate"],
                    "object": record["object"]
                })

            paths.ontology_output.parent.mkdir(parents=True, exist_ok=True)
            with paths.ontology_output.open('w', encoding='utf-8') as f:
                json.dump(ontology_data, f, ensure_ascii=False, indent=2)
            
            print(f"Successfully updated '{paths.ontology_output.name}' with {len(ontology_data)} cloud relationships.")

    except Exception as e:
        print(f"Cloud Agent Error: {e}")
    finally:
        driver.close()
        print("--- [Cloud] Connection Closed ---")

def main():
    # 사용법 안내
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--upload":
            run_cloud_agent(command="upload")
        elif arg == "--help" or arg == "-h":
            print("Usage:")
            print("  python cloud_graph_agent.py           # Export Cloud Graph to JSON")
            print("  python cloud_graph_agent.py --upload  # Local CSV -> Cloud")
            print("  python cloud_graph_agent.py \"MATCH (n) RETURN count(n)\" # Run Query on Cloud")
        else:
            run_cloud_agent(query=" ".join(sys.argv[1:]))
    else:
        # 인자 없으면 기본적으로 클라우드 데이터를 JSON으로 내보냅니다.
        run_cloud_agent()


if __name__ == "__main__":
    try:
        main()
    except runtime.ConfigurationError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        raise SystemExit(2) from error
