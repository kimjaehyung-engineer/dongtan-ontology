import sqlite3

db_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\geotech_data.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("Boreholes count:", cur.execute("SELECT count(*) FROM boreholes").fetchone()[0])
print("Facilities:", cur.execute("SELECT DISTINCT facility, doc_name, count(*) FROM boreholes GROUP BY facility, doc_name").fetchall())

# 연약층 (심도 3m 이내 N < 6)
soft_ground = cur.execute("""
    SELECT DISTINCT b.hole_no, b.facility, s.depth_m, s.n_value, b.page_start, b.doc_name
    FROM spt_records s
    JOIN boreholes b ON s.hole_no = b.hole_no
    WHERE s.depth_m <= 3.0 AND s.n_value < 6
    ORDER BY b.hole_no, s.depth_m
""").fetchall()

print(f"\nSoft Ground (<3m, N<6) Count: {len(soft_ground)}")
for r in soft_ground[:10]:
    print(" ", r)
