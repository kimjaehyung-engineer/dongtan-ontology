server_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "async function fetchDocs" in l:
        print(f"fetchDocs start: {i+1}")
        for j in range(i, min(len(lines), i+80)):
            if lines[j].strip().startswith("async function deleteDoc"):
                print(f"fetchDocs end: {j}")
                break
