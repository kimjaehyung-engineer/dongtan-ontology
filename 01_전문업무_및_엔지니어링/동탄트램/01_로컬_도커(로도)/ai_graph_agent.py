import json
import sys
import os
from neo4j import GraphDatabase

# 1. 로컬 Memgraph 서버 접속 정보 (Docker)
URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

# 2. 결과 저장 경로
OUTPUT_PATH = r"c:\Users\sskjh\antigravity\04_자기계발_및_창작\mindmap-app\public\ontology.json"

def run_agent(cypher_query=None):
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            # (A) 쿼리가 있으면 실행 (쓰기 트랜잭션 사용)
            if cypher_query:
                print(f"Executing Query...")
                def execute_tx(tx):
                    result = tx.run(cypher_query)
                    records = list(result)
                    if records:
                        print(f"Query Results ({len(records)} records):")
                        for record in records[:10]: # 결과가 많을 경우 상위 10개만 출력
                            print(f"  {record}")
                    summary = result.consume()
                    return summary.counters

                counters = session.execute_write(execute_tx)
                print(f"Update Summary: Nodes created: {counters.nodes_created}, Relationships created: {counters.relationships_created}, Properties set: {counters.properties_set}")

            # (B) 최신 그래프 데이터 추출
            print("Fetching latest graph data...")
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

            # (C) JSON 파일로 저장
            os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
            with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
                json.dump(ontology_data, f, ensure_ascii=False, indent=2)
            
            print(f"Successfully updated {OUTPUT_PATH} with {len(ontology_data)} relationships.")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    # 모든 인자를 하나로 합쳐서 쿼리로 사용 (공백 문제 해결)
    query_arg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    run_agent(query_arg)
