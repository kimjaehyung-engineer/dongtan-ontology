import sys
sys.path.append(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
import sql_query_engine

q1 = "제안설계 NGB 시추공 중 n<6 이하인 곳은?"
ans1 = sql_query_engine.generate_and_execute_sql(q1)
print(f"=== Query 1: {q1} ===")
if ans1:
    print(ans1.encode("utf-8", errors="replace").decode("utf-8"))
else:
    print("No response")

q2 = "NGB-2 시추조사 정보는?"
ans2 = sql_query_engine.generate_and_execute_sql(q2)
print(f"\n=== Query 2: {q2} ===")
if ans2:
    print(ans2.encode("utf-8", errors="replace").decode("utf-8"))
else:
    print("No response")
