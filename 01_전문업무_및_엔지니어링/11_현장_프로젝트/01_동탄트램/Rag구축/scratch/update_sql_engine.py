from pathlib import Path

sql_engine_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\sql_query_engine.py")
content = sql_engine_path.read_text(encoding="utf-8")

# 1. 키워드에 ngb 추가
content = content.replace('"nh-", "gb-", "dt-"', '"nh-", "gb-", "dt-", "ngb-", "제안설계"')

# 2. hole_no 정규식에 NGB 추가
content = content.replace(r"r'\b(NH-\d+|GB-\d+|DT-\d+)\b'", r"r'\b(NH-\d+|GB-\d+|DT-\d+|NGB-\d+)\b'")

# 3. doc_filter에 제안설계/NGB 분기 추가
old_depot_branch = 'elif "차량기지" in q_lower or "gb" in q_lower:\n        doc_filter = "AND (s.hole_no LIKE \'GB%\' OR h.facility LIKE \'%차량기지%\')"'
new_depot_branch = """elif "ngb" in q_lower or "제안설계" in q_lower:
        doc_filter = "AND s.hole_no LIKE 'NGB%'"
    elif "차량기지" in q_lower or "gb" in q_lower:
        doc_filter = "AND (s.hole_no LIKE 'GB%' OR s.hole_no LIKE 'NGB%' OR h.facility LIKE '%차량기지%')\""""

if old_depot_branch in content:
    content = content.replace(old_depot_branch, new_depot_branch)
else:
    # flexible regex
    import re
    content = re.sub(
        r'elif\s+["\']차량기지["\']\s+in\s+q_lower\s+or\s+["\']gb["\']\s+in\s+q_lower:.*?doc_filter\s*=\s*["\'][^"\']+["\']',
        new_depot_branch,
        content
    )

sql_engine_path.write_text(content, encoding="utf-8")
print("sql_query_engine.py updated with NGB support successfully!")
