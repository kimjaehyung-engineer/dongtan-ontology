import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect(r'C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\geotech_data.db')
c = conn.cursor()

c.execute("SELECT id, label, type, facility, doc_name, page FROM knowledge_nodes WHERE doc_name LIKE '%입찰%'")
nodes = c.fetchall()
print(f"=== Nodes for 입찰안내서 ({len(nodes)}개) ===")
for n in nodes:
    print(' ', n)

c.execute("SELECT id, src_id, tgt_id, relation, label, doc_name, page FROM knowledge_edges WHERE doc_name LIKE '%입찰%'")
edges = c.fetchall()
print(f"\n=== Edges for 입찰안내서 ({len(edges)}개) ===")
for e in edges:
    print(' ', e)
