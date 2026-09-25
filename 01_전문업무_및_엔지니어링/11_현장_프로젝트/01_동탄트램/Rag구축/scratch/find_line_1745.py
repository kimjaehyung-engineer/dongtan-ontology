from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

# HTML_TEMPLATE 찾기
lines = content.splitlines()
print(f"Total lines in server.py: {len(lines)}")

# HTML_TEMPLATE 시작 찾기
html_start = -1
for i, l in enumerate(lines):
    if "HTML_TEMPLATE = '''" in l or 'HTML_TEMPLATE = """' in l:
        html_start = i
        break

print(f"HTML_TEMPLATE starts at line {html_start + 1}")

# 브라우저 기준 line 1745는 HTML_TEMPLATE 내부의 라인일 것임
# HTML_TEMPLATE 만 따로 추출해서 1740~1755 라인 확인
html_lines = []
in_html = False
for l in lines:
    if "HTML_TEMPLATE =" in l:
        in_html = True
    if in_html:
        html_lines.append(l)
    if in_html and l.strip().endswith("'''") and "HTML_TEMPLATE =" not in l:
        break

print(f"Total HTML lines: {len(html_lines)}")

# HTML_TEMPLATE 라인 1735~1755 출력
for idx in range(1730, min(1760, len(html_lines))):
    print(f"{idx+1}: {html_lines[idx]}")
