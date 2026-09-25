server_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if ".doc-list" in l or ".doc-item" in l:
        print(f"Match at line {i+1}")
        for j in range(max(0, i-5), min(len(lines), i+45)):
            clean = lines[j].strip().encode('ascii', errors='replace').decode('ascii')
            print(f"  {j+1}: {clean}")
        break
