import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect(r'C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\geotech_data.db')
c = conn.cursor()

c.execute("PRAGMA table_info(knowledge_nodes)")
print('knowledge_nodes columns:')
for col in c.fetchall():
    print(' ', col)

c.execute("PRAGMA table_info(knowledge_edges)")
print('knowledge_edges columns:')
for col in c.fetchall():
    print(' ', col)

c.execute("SELECT * FROM knowledge_nodes")
all_nodes = c.fetchall()
print(f'Total knowledge_nodes: {len(all_nodes)}')
for n in all_nodes:
    print('  ', n)

c.execute("SELECT * FROM knowledge_edges")
all_edges = c.fetchall()
print(f'Total knowledge_edges: {len(all_edges)}')
for e in all_edges[:15]:
    print('  ', e)
