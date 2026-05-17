from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

def analyze_monthly_inspection():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        print("RODO: Deep Diving into 'Monthly Inspection' Node...")
        
        # 1. 정확한 이름과 속성 추출
        q = """
        MATCH (n)
        WHERE n.name CONTAINS '월상'
        OPTIONAL MATCH (n)-[r]-(m)
        RETURN n.name as target_name, properties(n) as props, 
               type(r) as rel_type, m.name as neighbor_name
        """
        result = session.run(q)
        records = list(result)
        
        if not records:
            print("RODO: Could not find any node containing '월상'.")
            return

        print(f"RODO: Analyzing node: {records[0]['target_name']}")
        print(f"RODO: Node Properties: {records[0]['props']}")
        
        print("\nRODO: Connections Found:")
        for rec in records:
            if rec['rel_type']:
                print(f" - [{rec['rel_type']}] -> {rec['neighbor_name']}")
            else:
                print(" - (No connections found)")

    driver.close()

if __name__ == "__main__":
    analyze_monthly_inspection()
