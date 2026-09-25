import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect(r'C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\geotech_data.db')
c = conn.cursor()

c.execute("SELECT id, label, type, description, page FROM knowledge_nodes WHERE page <= 8 AND doc_name LIKE '%입찰안내서%'")
for r in c.fetchall():
    print(r)
