import os
from neo4j import GraphDatabase

# Memgraph Connection
URI = "bolt+ssc://3.70.13.61:7687"
USER = "skjh0717@gmail.com"
PASSWORD = "ssmg25rk$12#"

def export_for_google_sheets():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    try:
        with driver.session() as session:
            query = "MATCH (n) RETURN n.name as Name, labels(n)[0] as Category, properties(n) as Details"
            result = session.run(query)
            
            output_file = 'copy_to_google_sheets.txt'
            # Use tab (\t) as separator for Google Sheets copy-paste compatibility
            with open(output_file, 'w', encoding='utf-8-sig') as f:
                f.write("노드명\t카테고리\t세부속성\n")
                count = 0
                for record in result:
                    name = record['Name'] if record['Name'] else ""
                    category = record['Category'] if record['Category'] else "N/A"
                    # Clean up details string to prevent newline issues in sheets
                    details = str(record['Details']).replace('\n', ' ').replace('\r', '')
                    f.write(f"{name}\t{category}\t{details}\n")
                    count += 1
                
        print(f"File created: {output_file} ({count} nodes)")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    export_for_google_sheets()
