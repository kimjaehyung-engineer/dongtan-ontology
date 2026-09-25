from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

loc = {"__file__": str(server_path)}
exec(content[:content.find("class SiteRAGHandler")], loc, loc)
html = loc.get("HTML_TEMPLATE", "")

idx = html.find("let descHtml =")
print("Rendered HTML JS line:")
print(repr(html[idx:idx+90]))
