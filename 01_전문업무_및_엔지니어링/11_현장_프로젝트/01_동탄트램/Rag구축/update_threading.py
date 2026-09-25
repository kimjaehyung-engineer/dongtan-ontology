target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(target_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update import
content = content.replace(
    "from http.server import HTTPServer, BaseHTTPRequestHandler",
    "from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer"
)

# 2. Update run() server instantiation
content = content.replace(
    "httpd = HTTPServer(server_address, SiteRAGHandler)",
    "httpd = ThreadingHTTPServer(server_address, SiteRAGHandler)"
)

with open(target_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated server to multi-threaded ThreadingHTTPServer")
