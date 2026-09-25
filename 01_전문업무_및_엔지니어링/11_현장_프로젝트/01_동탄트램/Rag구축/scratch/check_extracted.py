import sqlite3

conn = sqlite3.connect(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\geotech_data.db")
c = conn.cursor()
nodes = c.execute("SELECT id, label, type, facility, description FROM knowledge_nodes").fetchall()
print(f"=== Knowledge Nodes in DB: {len(nodes)} ===")
for n in nodes:
    print(f"[{n[2]}] {n[0]}: {n[1]} ({n[3]})")
    print(f"    설명: {n[4]}")

edges = c.execute("SELECT src_id, tgt_id, relation, label, is_warning FROM knowledge_edges").fetchall()
print(f"\n=== Knowledge Edges in DB: {len(edges)} ===")
for e in edges:
    print(f"[{e[2]}] {e[0]} --> {e[1]} (label={e[3]}, warning={e[4]})")
