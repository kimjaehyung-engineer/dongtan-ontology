import sys
sys.stdout.reconfigure(encoding="utf-8")

target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(target_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(70, 110):
    print(f"{i+1}: {lines[i]}", end="")
