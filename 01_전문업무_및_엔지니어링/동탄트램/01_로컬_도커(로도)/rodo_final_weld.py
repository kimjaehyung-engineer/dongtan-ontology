from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

def final_weld_monthly_inspection():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        print("RODO: Executing Forced Welding for 'Monthly Inspection'...")
        
        # 1. 중심축 및 허브 노드 확인/생성
        session.run("MERGE (root:Project {name: '동탄트램 사업'})")
        session.run("MERGE (hub:Hub {name: '도시기반시설 유지관리 및 보수공사'})")
        
        # 2. '월상'이 포함된 모든 노드를 강제로 연결
        q = """
        MATCH (root:Project {name: '동탄트램 사업'})
        MATCH (hub:Hub {name: '도시기반시설 유지관리 및 보수공사'})
        MATCH (o)
        WHERE o.name CONTAINS '월상'
        MERGE (o)-[r1:COMPOSITION]->(hub)
        MERGE (o)-[r2:NAVIGATION]->(root)
        RETURN count(o) as count
        """
        result = session.run(q)
        count = result.single()['count']
        
        if count > 0:
            print(f"RODO: Success! {count} node(s) containing '월상' are now welded to the network.")
        else:
            # 만약 CONTAINS로도 못 찾는다면, 모든 노드를 뒤져서 '월'로 시작하는 것까지 탐색
            print("RODO: Substring match failed, trying broader search...")
            q2 = """
            MATCH (root:Project {name: '동탄트램 사업'})
            MATCH (hub:Hub {name: '도시기반시설 유지관리 및 보수공사'})
            MATCH (o)
            WHERE o.name =~ '.*월상.*'
            MERGE (o)-[r1:COMPOSITION]->(hub)
            MERGE (o)-[r2:NAVIGATION]->(root)
            RETURN count(o) as count
            """
            result2 = session.run(q2)
            count2 = result2.single()['count']
            print(f"RODO: Final search connected {count2} nodes.")

    driver.close()

if __name__ == "__main__":
    final_weld_monthly_inspection()
