import os
from neo4j import GraphDatabase
import csv

# Memgraph Connection
URI = "bolt+ssc://3.70.13.61:7687"
USER = "skjh0717@gmail.com"
PASSWORD = "ssmg25rk$12#"

def export_nodes_to_csv():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
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
