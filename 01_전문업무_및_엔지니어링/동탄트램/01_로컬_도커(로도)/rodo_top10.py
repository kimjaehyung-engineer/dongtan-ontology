from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = ""
PASSWORD = ""

def get_top_10_hubs():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    with driver.session() as session:
        q = """
        MATCH (n)
        OPTIONAL MATCH (n)-[r]-()
        WITH n, count(r) as degree
        RETURN n.name as name, degree
        ORDER BY degree DESC
        LIMIT 10
        """
        result = session.run(q)
        print("RODO: --- [Top 10 Knowledge Hubs] ---")
        for i, record in enumerate(result, 1):
            name = record['name']
            degree = record['degree']
            print(f"{i:2d}. {name:<40} | Degree: {degree}")

    driver.close()

if __name__ == "__main__":
    get_top_10_hubs()
