import sys
sys.stdout.reconfigure(encoding="utf-8")

target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(target_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

pos = 0
for i, l in enumerate(lines):
    if "Pure Global Multi-Document Index Routing" in l:
        pos = i
        break

for i in range(pos, min(pos+75, len(lines))):
    print(f"{i+1}: {lines[i]}", end="")
