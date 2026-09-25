from pathlib import Path
import re

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

loc = {"__file__": str(server_path)}
exec(content[:content.find("class SiteRAGHandler")], loc, loc)
html = loc.get("HTML_TEMPLATE", "")

# script 태그 추출
scripts = re.findall(r'<script(?:\s+[^>]*)?>(.*?)</script>', html, re.DOTALL)
print(f"Found {len(scripts)} script tags in HTML.")

for i, s in enumerate(scripts):
    if not s.strip(): continue
    # node 가 있으면 node --check 로 검증
    temp_js = Path("scratch/test_syntax.js")
    temp_js.write_text(s, encoding="utf-8")
    print(f"Script {i+1} saved ({len(s)} chars).")
