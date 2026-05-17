import pandas as pd

nodes_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\rfp_nodes.csv"
rels_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\rfp_relationships.csv"

nodes = pd.read_csv(nodes_path)
rels = pd.read_csv(rels_path)

print("// 1. Clean up")
print("MATCH (n) DETACH DELETE n;")

print("\n// 2. Create Nodes")
print("CREATE ")
node_lines = []
for _, r in nodes.iterrows():
    # Clean id to be used in variable name (n_RFP_A_001)
    var_id = str(r["id"]).replace("-", "_")
    # Clean content for name
    name = str(r["content"]).replace("'", "\\'").replace("\n", " ")
    label = str(r["label"])
    node_lines.append(f"(n_{var_id}:{label} {{id:'{r['id']}', name:'{name}', section:'{r['section']}', risk:'{r['risk_level']}'}})")
print(",\n".join(node_lines) + ";")

print("\n// 3. Create Relationships")
for _, r in rels.iterrows():
    print(f"MATCH (a {{id:'{r['source']}'}}), (b {{id:'{r['target']}'}}) CREATE (a)-[:{r['type']}]->(b);")

print("\n// 4. Return all")
print("MATCH (n) RETURN n;")
