import sys
sys.stdout.reconfigure(encoding="utf-8")

target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(target_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "resp_data = {" in l or "self.respond_json(resp_data)" in l:
        print(f"Line {i+1}: {l.strip()}")
