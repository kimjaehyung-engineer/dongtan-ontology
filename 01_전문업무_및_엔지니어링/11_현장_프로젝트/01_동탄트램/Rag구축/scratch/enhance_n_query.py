from pathlib import Path

sql_engine_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\sql_query_engine.py")
content = sql_engine_path.read_text(encoding="utf-8")

old_pattern = """    m_depth = re.search(r'(\d+(?:\.\d+)?)\s*m\s*(?:이내|상부|내|미만|이하)?', q_lower)
    m_n = re.search(r'[nN]\s*(?:치)?\s*([<>]=?|=)\s*(\d+)', q_lower)

    if m_depth and m_n:"""

new_pattern = """    m_depth = re.search(r'(\d+(?:\.\d+)?)\s*m\s*(?:이내|상부|내|미만|이하)?', q_lower)
    m_n = re.search(r'[nN]\s*(?:치)?\s*([<>]=?|=)\s*(\d+)', q_lower)

    if m_n:
        max_d = float(m_depth.group(1)) if m_depth else 999.0"""

if old_pattern in content:
    content = content.replace(old_pattern, new_pattern)
    # 아래 max_d 정의 부분 수정
    content = content.replace("        max_d = float(m_depth.group(1))\n        op = m_n.group(1)", "        op = m_n.group(1)")
    sql_engine_path.write_text(content, encoding="utf-8")
    print("Enhanced depth-optional N-query matching successfully!")
else:
    print("Could not find old_pattern, checking regex...")
    import re
    content = re.sub(
        r'if m_depth and m_n:\s+max_d = float\(m_depth\.group\(1\)\)',
        'if m_n:\n        max_d = float(m_depth.group(1)) if m_depth else 999.0',
        content
    )
    sql_engine_path.write_text(content, encoding="utf-8")
    print("Enhanced via regex!")
