import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
lines = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py").read_text(encoding='utf-8').splitlines()

for idx, l in enumerate(lines):
    if "/api/chat" in l:
        print(f"Line {idx+1}: {l}")
