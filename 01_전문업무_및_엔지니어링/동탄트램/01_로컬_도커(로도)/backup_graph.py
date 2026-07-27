from importlib import import_module
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

runtime = import_module("dongtan_runtime")

def backup_graph():
    config = runtime.load_cloud_database_config()
    GraphDatabase = import_module("neo4j").GraphDatabase
    backup_file = "dongtan_tram_backup_20260516.cypher"

    print(f"Connecting to Memgraph at {config.uri}...")
    try:
        driver = GraphDatabase.driver(config.uri, **config.driver_kwargs())
        with driver.session() as session:
            with open(backup_file, "w", encoding="utf-8") as f:
                f.write("// Dongtan Tram Knowledge Graph Backup - 2026-05-16\n")
                f.write("MATCH (n) DETACH DELETE n;\n\n")

                # 1. Back up Nodes
                print("Backing up nodes...")
                nodes = session.run("MATCH (n) RETURN n, labels(n) as labels, id(n) as node_id")
                node_count = 0
                for record in nodes:
                    node = record["n"]
                    labels = record["labels"]
                    node_id = record["node_id"]
                    label_str = ":".join(labels)
                    props = dict(node)
                    # Handle escaping for strings
                    props_str = ", ".join([f"{k}: {repr(v)}" for k, v in props.items()])
                    f.write(f"CREATE (:{label_str} {{ {props_str}, backup_id: '{node_id}' }});\n")
                    node_count += 1
                print(f"Saved {node_count} nodes.")

                f.write("\n// Relationships\n")
                
                # 2. Back up Relationships
                print("Backing up relationships...")
                rels = session.run("MATCH (n)-[r]->(m) RETURN id(n) as start_id, type(r) as rel_type, properties(r) as rel_props, id(m) as end_id")
                rel_count = 0
                for record in rels:
                    start_id = record["start_id"]
                    rel_type = record["rel_type"]
                    rel_props = record["rel_props"]
                    end_id = record["end_id"]
                    props_str = ", ".join([f"{k}: {repr(v)}" for k, v in rel_props.items()])
                    f.write(f"MATCH (s {{ backup_id: '{start_id}' }}), (e {{ backup_id: '{end_id}' }}) ")
                    f.write(f"CREATE (s)-[:{rel_type} {{ {props_str} }}]->(e);\n")
                    rel_count += 1
                print(f"Saved {rel_count} relationships.")

                # 3. Clean up backup_ids
                f.write("\n// Cleanup\n")
                f.write("MATCH (n) REMOVE n.backup_id;\n")

        print(f"Backup completed successfully: {backup_file}")
        driver.close()

    except Exception as e:
        print(f"Error during backup: {e}")

if __name__ == "__main__":
    backup_graph()
