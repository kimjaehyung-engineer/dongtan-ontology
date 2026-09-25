import sqlite3

db_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\geotech_data.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Tables:", tables)

for t in tables:
    t_name = t[0]
    cols = cur.execute(f"PRAGMA table_info({t_name})").fetchall()
    count = cur.execute(f"SELECT count(*) FROM {t_name}").fetchone()[0]
    print(f"\nTable: {t_name} ({count} rows)")
    for col in cols:
        print(f"  {col[1]} ({col[2]})")
    
    sample = cur.execute(f"SELECT * FROM {t_name} LIMIT 3").fetchall()
    print("  Sample:", sample)
