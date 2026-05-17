from neo4j import GraphDatabase
import os

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

def add_drawing_metadata():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        print("RODO: Injecting Drawing Metadata into Knowledge Graph...")
        
        # 1. 정거장 관련 노드에 건축 도면 메타데이터 추가
        q1 = """
        MATCH (n) WHERE n.name CONTAINS '정거장' OR n.name CONTAINS 'PSD'
        SET n.drawing_id = 'DT-ARC-001'
        SET n.file_path = 'C:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/동탄트램/도면/DT-ARC-001_정거장평면도.pdf'
        RETURN count(n) as count
        """
        res1 = session.run(q1)
        print(f"RODO: Added Architectural drawing to {res1.single()['count']} Station/PSD nodes.")

        # 2. 전력 관련 노드에 전기 도면 메타데이터 추가
        q2 = """
        MATCH (n) WHERE n.name CONTAINS '전압' OR n.name CONTAINS 'DC' OR n.name CONTAINS '변전'
        SET n.drawing_id = 'DT-ELEC-100'
        SET n.file_path = 'C:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/동탄트램/도면/DT-ELEC-100_급전계통도.pdf'
        RETURN count(n) as count
        """
        res2 = session.run(q2)
        print(f"RODO: Added Electrical drawing to {res2.single()['count']} Power nodes.")

        # 3. 유지관리 관련 노드에 차량 도면 메타데이터 추가
        q3 = """
        MATCH (n) WHERE n.name CONTAINS '검사' OR n.name CONTAINS '유지' OR n.name CONTAINS '정비'
        SET n.drawing_id = 'DT-VEH-500'
        SET n.file_path = 'C:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/동탄트램/도면/DT-VEH-500_차량유지보수매뉴얼.pdf'
        RETURN count(n) as count
        """
        res3 = session.run(q3)
        print(f"RODO: Added Vehicle/Maintenance doc to {res3.single()['count']} Maintenance nodes.")
        
        print("RODO: Metadata injection completed successfully!")

if __name__ == "__main__":
    add_drawing_metadata()
