import json
import sys
import os
import pandas as pd
from neo4j import GraphDatabase

# ==========================================
# 🌌 [DONGTAN TRAM] CLOUD GRAPH AGENT
# ==========================================
# 특징: 
# 1. Memgraph Cloud(원격)와 직접 통신
# 2. 로컬 데이터를 클라우드로 업로드 (--upload)
# 3. 클라우드 데이터를 웹 앱(Ontology App)으로 동기화
# 4. 클라우드 서버에 Cypher 쿼리 직접 실행
# ==========================================

# 1. Memgraph Cloud 접속 정보
URI = "bolt+ssc://3.70.13.61:7687"  # Memgraph Cloud (make_sheets_txt.py 기준)
USER = "skjh0717@gmail.com"
PASSWORD = "ssmg25rk$12#"

# 2. 결과 저장 경로 (웹 앱 시각화용)
# 이 경로를 업데이트하면 localhost:3000 에서 실행 중인 앱이 클라우드 데이터를 표시합니다.
OUTPUT_PATH = r"c:\Users\sskjh\antigravity\04_자기계발_및_창작\mindmap-app\public\ontology.json"

# 3. 로컬 데이터 소스 (업로드용)
NODES_CSV = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\00_원본_데이터\rfp_nodes.csv"
RELS_CSV = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\00_원본_데이터\rfp_relationships.csv"

def run_cloud_agent(command=None, query=None):
    print(f"--- [Cloud] Connecting to Memgraph Cloud ({URI}) ---")
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            # [기능 1] 로컬 데이터를 클라우드로 강제 업로드
            if command == "upload":
                print(f"Action: Uploading local CSVs to Cloud...")
                if not os.path.exists(NODES_CSV) or not os.path.exists(RELS_CSV):
                    print(f"Error: CSV files not found at {NODES_CSV}")
                    return

                nodes_df = pd.read_csv(NODES_CSV)
                rels_df = pd.read_csv(RELS_CSV)
                
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

            # [기능 3] 클라우드 데이터를 웹 앱용 JSON으로 동기화 (기본 동작)
            print("Action: Syncing Cloud Graph to Web Visualization App...")
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

            os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
            with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
                json.dump(ontology_data, f, ensure_ascii=False, indent=2)
            
            print(f"Successfully updated '{os.path.basename(OUTPUT_PATH)}' with {len(ontology_data)} cloud relationships.")

    except Exception as e:
        print(f"Cloud Agent Error: {e}")
    finally:
        driver.close()
        print("--- [Cloud] Connection Closed ---")

if __name__ == "__main__":
    # 사용법 안내
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--upload":
            run_cloud_agent(command="upload")
        elif arg == "--help" or arg == "-h":
            print("Usage:")
            print("  python cloud_graph_agent.py           # Sync Cloud -> Web App")
            print("  python cloud_graph_agent.py --upload  # Local CSV -> Cloud")
            print("  python cloud_graph_agent.py \"MATCH (n) RETURN count(n)\" # Run Query on Cloud")
        else:
            run_cloud_agent(query=" ".join(sys.argv[1:]))
    else:
        # 인자 없으면 기본적으로 클라우드 데이터를 가져와서 웹 앱 업데이트
        run_cloud_agent()
