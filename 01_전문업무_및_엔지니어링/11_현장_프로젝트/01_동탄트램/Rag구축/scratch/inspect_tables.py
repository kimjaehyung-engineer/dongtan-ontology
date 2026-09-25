import sqlite3

conn = sqlite3.connect(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\geotech_data.db")
c = conn.cursor()
tables = c.execute("SELECT name, sql FROM sqlite_master WHERE type='table'").fetchall()
for t, sql in tables:
    print(f"Table: {t}")
    print(sql)
    print("=" * 40)
