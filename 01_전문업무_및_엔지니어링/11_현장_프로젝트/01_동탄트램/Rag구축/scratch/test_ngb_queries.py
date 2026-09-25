import sys
sys.path.append(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
import sql_query_engine

q1 = "제안설계 NGB 시추공 중 n<6 이하인 곳은?"
print("=== Query 1 ===", q1)
ans1 = sql_query_engine.generate_and_execute_sql(q1)
print(ans1 if ans1 else "No response")

q2 = "NGB-2 시추조사 정보는?"
print("\n=== Query 2 ===", q2)
ans2 = sql_query_engine.generate_and_execute_sql(q2)
print(ans2 if ans2 else "No response")
