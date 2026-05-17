from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

def final_anchor():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        print("RODO: Setting the Final Project Anchor...")
        
        # 1. 뿌리 노드 생성
        session.run("MERGE (root:Project {name: '동탄트램 사업'})")
        
        # 2. 허브 노드들을 뿌리 노드에 결합
        keywords = ['차량', '전기', '전력', '인프라', '시설', '도로', '기동', '지하차도', '유지관리']
        for kw in keywords:
            print(f"RODO: Anchoring hubs related to '{kw}' to Project Root...")
            q = """
            MATCH (root:Project {name: '동탄트램 사업'})
            MATCH (hub)
            WHERE hub <> root AND hub.name CONTAINS $kw
            MERGE (hub)-[:PART_OF_PROJECT]->(root)
            """
            session.run(q, kw=kw)
            
        print("RODO: All hubs are now anchored to the Project Root!")
    driver.close()

if __name__ == "__main__":
    final_anchor()
