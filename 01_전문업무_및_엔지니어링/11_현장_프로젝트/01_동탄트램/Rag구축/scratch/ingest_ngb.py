import sqlite3
from pathlib import Path

db_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\geotech_data.db")
conn = sqlite3.connect(str(db_path))
cur = conn.cursor()

doc_name = "#3편 증빙자료_토질 및 기초.pdf"
page_no = 87
facility = "차량기지 (제안설계)"

# 기존 NGB 데이터가 있다면 삭제 (멱등성 보장)
cur.execute("DELETE FROM boreholes WHERE hole_no LIKE 'NGB-%'")
cur.execute("DELETE FROM strata_layers WHERE hole_no LIKE 'NGB-%'")
cur.execute("DELETE FROM spt_records WHERE hole_no LIKE 'NGB-%'")

# 1. 시추공 데이터 (5공)
boreholes_data = [
    ("NGB-1", 9.0, 87, 87),
    ("NGB-2", 25.0, 87, 87),
    ("NGB-3", 12.5, 87, 87),
    ("NGB-4", 11.5, 87, 87),
    ("NGB-5", 23.5, 87, 87),
]

for hole, depth, p_start, p_end in boreholes_data:
    cur.execute("""
        INSERT INTO boreholes (doc_name, hole_no, facility, page_start, page_end, total_depth_m)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (doc_name, hole, facility, p_start, p_end, depth))

# 2. 지층 데이터 (strata_layers)
strata_data = [
    # NGB-1
    ("NGB-1", "풍화토", 0.0, 4.0, 4.0, "실트질 모래"),
    ("NGB-1", "풍화암", 4.0, 6.0, 2.0, "굴진시 암편 및 실트질모래로 분해"),
    ("NGB-1", "연암", 6.0, 9.0, 3.0, "편마암의 연암, TCR/RQD 86/6"),
    # NGB-2
    ("NGB-2", "매립층", 0.0, 4.5, 4.5, "자갈섞인 실트질 모래"),
    ("NGB-2", "퇴적층", 4.5, 11.0, 6.5, "자갈섞인 모래"),
    ("NGB-2", "풍화토", 11.0, 15.0, 4.0, "실트질 모래"),
    ("NGB-2", "풍화암", 15.0, 22.0, 7.0, "굴진시 암편 및 실트질모래로 분해"),
    ("NGB-2", "연암", 22.0, 25.0, 3.0, "편마암의 연암, TCR/RQD 83/3"),
    # NGB-3
    ("NGB-3", "매립층", 0.0, 2.0, 2.0, "모래섞인 자갈"),
    ("NGB-3", "풍화토", 2.0, 6.0, 4.0, "실트질 모래"),
    ("NGB-3", "풍화암", 6.0, 9.5, 3.5, "굴진시 암편 및 실트질모래로 분해"),
    ("NGB-3", "연암", 9.5, 12.5, 3.0, "편마암의 연암, TCR/RQD 97/14"),
    # NGB-4
    ("NGB-4", "매립층", 0.0, 1.0, 1.0, "자갈섞인 실트질 모래"),
    ("NGB-4", "퇴적층", 1.0, 4.5, 3.5, "자갈섞인 점토질 모래"),
    ("NGB-4", "풍화토", 4.5, 7.0, 2.5, "실트질 모래"),
    ("NGB-4", "풍화암", 7.0, 8.5, 1.5, "굴진시 암편 및 실트질모래로 분해"),
    ("NGB-4", "연암", 8.5, 11.5, 3.0, "편마암의 연암, TCR/RQD 65/0"),
    # NGB-5
    ("NGB-5", "매립층", 0.0, 7.8, 7.8, "자갈섞인 실트질 모래"),
    ("NGB-5", "퇴적층", 7.8, 10.7, 2.9, "실트질 모래"),
    ("NGB-5", "풍화토", 10.7, 15.2, 4.5, "실트질 모래"),
    ("NGB-5", "연암", 15.2, 23.5, 8.3, "편마암의 연암, TCR/RQD 63~100/0~22"),
]

for hole, name, top, btm, thk, desc in strata_data:
    cur.execute("""
        INSERT INTO strata_layers (doc_name, hole_no, page, stratum_name, depth_top_m, depth_bottom_m, thickness_m, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (doc_name, hole, page_no, name, top, btm, thk, desc))

# 3. SPT 시험 데이터 (spt_records)
spt_data = [
    # NGB-1: 50/20~50/14 (풍화토), 50/8~50/4 (풍화암)
    ("NGB-1", "S-1", 1.0, 50, "50/20", 50, 20),
    ("NGB-1", "S-2", 3.0, 50, "50/14", 50, 14),
    ("NGB-1", "S-3", 5.0, 50, "50/8", 50, 8),
    ("NGB-1", "S-4", 6.0, 50, "50/4", 50, 4),

    # NGB-2: 3/30~5/30 (매립 0~4.5m ⚠️), 11/30~26/30 (퇴적 4.5~11m), 23/30~50/12 (풍화토), 50/9~50/3 (풍화암)
    ("NGB-2", "S-1", 1.0, 3, "3/30", 3, 30),
    ("NGB-2", "S-2", 2.0, 4, "4/30", 4, 30),
    ("NGB-2", "S-3", 3.0, 5, "5/30", 5, 30),
    ("NGB-2", "S-4", 4.0, 5, "5/30", 5, 30),
    ("NGB-2", "S-5", 6.0, 11, "11/30", 11, 30),
    ("NGB-2", "S-6", 9.0, 26, "26/30", 26, 30),
    ("NGB-2", "S-7", 12.0, 23, "23/30", 23, 30),
    ("NGB-2", "S-8", 14.0, 50, "50/12", 50, 12),
    ("NGB-2", "S-9", 17.0, 50, "50/9", 50, 9),
    ("NGB-2", "S-10", 20.0, 50, "50/3", 50, 3),

    # NGB-3: 50/13 (매립), 50/14~50/11 (풍화토), 50/8~50/3 (풍화암)
    ("NGB-3", "S-1", 1.0, 50, "50/13", 50, 13),
    ("NGB-3", "S-2", 3.0, 50, "50/14", 50, 14),
    ("NGB-3", "S-3", 5.0, 50, "50/11", 50, 11),
    ("NGB-3", "S-4", 7.0, 50, "50/8", 50, 8),
    ("NGB-3", "S-5", 9.0, 50, "50/3", 50, 3),

    # NGB-4: 2/30~11/30 (퇴적 1.0~4.5m ⚠️), 42/30~50/15 (풍화토), 50/9~50/4 (풍화암)
    ("NGB-4", "S-1", 1.5, 2, "2/30", 2, 30),
    ("NGB-4", "S-2", 2.5, 6, "6/30", 6, 30),
    ("NGB-4", "S-3", 3.5, 11, "11/30", 11, 30),
    ("NGB-4", "S-4", 5.5, 42, "42/30", 42, 30),
    ("NGB-4", "S-5", 6.5, 50, "50/15", 50, 15),
    ("NGB-4", "S-6", 7.5, 50, "50/9", 50, 9),
    ("NGB-4", "S-7", 8.0, 50, "50/4", 50, 4),

    # NGB-5: 4/30~12/30 (매립 0~7.8m ⚠️), 13/30~26/30 (퇴적), 39/30~50/16 (풍화토)
    ("NGB-5", "S-1", 1.0, 4, "4/30", 4, 30),
    ("NGB-5", "S-2", 2.0, 5, "5/30", 5, 30),
    ("NGB-5", "S-3", 3.0, 5, "5/30", 5, 30),
    ("NGB-5", "S-4", 5.0, 8, "8/30", 8, 30),
    ("NGB-5", "S-5", 7.0, 12, "12/30", 12, 30),
    ("NGB-5", "S-6", 9.0, 13, "13/30", 13, 30),
    ("NGB-5", "S-7", 10.0, 26, "26/30", 26, 30),
    ("NGB-5", "S-8", 12.0, 39, "39/30", 39, 30),
    ("NGB-5", "S-9", 14.0, 50, "50/16", 50, 16),
]

for hole, s_no, depth, n_val, n_str, blows, pen in spt_data:
    cur.execute("""
        INSERT INTO spt_records (doc_name, hole_no, page, sample_no, depth_m, n_value, n_str, blows, penetration_cm)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (doc_name, hole, page_no, s_no, depth, n_val, n_str, blows, pen))

conn.commit()

# 통계 확인
print("Boreholes count:", cur.execute("SELECT count(*) FROM boreholes").fetchone()[0])
print("NGB boreholes:", cur.execute("SELECT hole_no, facility, total_depth_m, page_start FROM boreholes WHERE hole_no LIKE 'NGB-%'").fetchall())
print("NGB strata count:", cur.execute("SELECT count(*) FROM strata_layers WHERE hole_no LIKE 'NGB-%'").fetchone()[0])
print("NGB SPT count:", cur.execute("SELECT count(*) FROM spt_records WHERE hole_no LIKE 'NGB-%'").fetchone()[0])
print("NGB soft ground (<3m, N<6):", cur.execute("""
    SELECT hole_no, depth_m, n_value, n_str 
    FROM spt_records 
    WHERE hole_no LIKE 'NGB-%' AND depth_m <= 3.0 AND n_value < 6
""").fetchall())

conn.close()
print("NGB Data Ingested Successfully!")
