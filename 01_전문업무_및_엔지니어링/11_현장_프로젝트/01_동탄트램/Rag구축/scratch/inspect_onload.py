server_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for j in range(1765, min(len(lines), 1835)):
    clean = lines[j].strip().encode('ascii', errors='replace').decode('ascii')
    print(f"{j+1}: {clean}")
