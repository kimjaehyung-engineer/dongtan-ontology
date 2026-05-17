from neo4j import GraphDatabase
import os

def restore_graph():
    uri = "bolt://localhost:7687"
    backup_file = "dongtan_tram_backup_20260516.cypher"
    
    # Path with Korean characters handling
    full_backup_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\dongtan_tram_backup_20260516.cypher"
    if not os.path.exists(full_backup_path):
        full_backup_path = "dongtan_tram_backup_20260516.cypher"

    print(f"Connecting to Local Memgraph at {uri}...")
    try:
        driver = GraphDatabase.driver(uri, auth=("", ""))
        with driver.session() as session:
            print(f"Reading backup file: {full_backup_path}")
            with open(full_backup_path, "r", encoding="utf-8") as f:
                queries = f.read().split(";")
                
                print(f"Executing {len(queries)} queries to restore data...")
                for i, query in enumerate(queries):
                    query = query.strip()
                    if query:
                        session.run(query)
                        if i % 100 == 0:
                            print(f"Restored {i} queries...")

        print("Data restoration completed successfully!")
        driver.close()

    except Exception as e:
        print(f"Error during restoration: {e}")

if __name__ == "__main__":
    restore_graph()
