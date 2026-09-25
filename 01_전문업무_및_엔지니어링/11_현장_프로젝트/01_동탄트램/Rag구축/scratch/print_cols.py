import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect(r'C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\geotech_data.db')
c = conn.cursor()
c.execute("PRAGMA table_info(knowledge_edges)")
print('knowledge_edges columns:', [col[1] for col in c.fetchall()])
c.execute("PRAGMA table_info(knowledge_nodes)")
print('knowledge_nodes columns:', [col[1] for col in c.fetchall()])
