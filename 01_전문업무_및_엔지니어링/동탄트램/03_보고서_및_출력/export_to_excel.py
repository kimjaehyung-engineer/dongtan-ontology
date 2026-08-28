import csv
from importlib import import_module
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

runtime = import_module("dongtan_runtime")

def export_nodes_to_csv():
    config = runtime.load_cloud_database_config()
    GraphDatabase = import_module("neo4j").GraphDatabase
    driver = GraphDatabase.driver(config.uri, **config.driver_kwargs())
    try:
        with driver.session() as session:
            # Get all nodes and their properties
            query = "MATCH (n) RETURN n.name as Name, labels(n) as Category, properties(n) as Details"
            result = session.run(query)
            
            output_file = 'dongtan_tram_knowledge_base.csv'
            with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Category', 'Details/Properties'])
                
                count = 0
                for record in result:
                    name = record['Name']
                    category = ", ".join(record['Category']) if record['Category'] else "N/A"
                    details = str(record['Details'])
                    writer.writerow([name, category, details])
                    count += 1
                
        print(f"Export complete: {output_file} ({count} nodes exported)")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    export_nodes_to_csv()
