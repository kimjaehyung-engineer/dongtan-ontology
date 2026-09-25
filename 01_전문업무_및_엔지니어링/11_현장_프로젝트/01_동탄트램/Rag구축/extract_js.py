import sys

target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(target_path, "r", encoding="utf-8") as f:
    code = f.read()

# find <script> in HTML_TEMPLATE
s_start = code.find("<script>")
s_end = code.find("</script>", s_start)

if s_start == -1 or s_end == -1:
    print(f"Script tag not found! start: {s_start}, end: {s_end}")
    sys.exit(1)

js_code = code[s_start+8:s_end]
print(f"Extracted JS code length: {len(js_code)}")

with open(r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\Rag구축\extracted.js", "w", encoding="utf-8") as f:
    f.write(js_code)

print("Saved to extracted.js")
