import sys
sys.path.append(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
import sql_query_engine

q1 = "제안설계 NGB 시추공 중 n<6 이하인 곳은?"
ans1 = sql_query_engine.generate_and_execute_sql(q1)

with open("scratch/query_res1.txt", "w", encoding="utf-8") as f:
    if isinstance(ans1, dict):
        f.write(f"Matched Pages: {ans1.get('matched_pages')}\n")
        f.write(ans1.get("reply", ""))
    else:
        f.write(str(ans1))

q2 = "NGB-2 시추조사 정보는?"
ans2 = sql_query_engine.generate_and_execute_sql(q2)

with open("scratch/query_res2.txt", "w", encoding="utf-8") as f:
    if isinstance(ans2, dict):
        f.write(f"Matched Pages: {ans2.get('matched_pages')}\n")
        f.write(ans2.get("reply", ""))
    else:
        f.write(str(ans2))

print("Saved query responses!")
