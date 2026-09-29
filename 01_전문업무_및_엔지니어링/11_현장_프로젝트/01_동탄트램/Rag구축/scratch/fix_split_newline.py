# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

SERVER_PATH = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")

with open(SERVER_PATH, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

replaced = False
for i, l in enumerate(lines):
    if "let descHtml =" in l and "split(" in l:
        print(f"Found line {i+1}: {l.strip()}")
        lines[i] = "          let descHtml = (nodeData.rawDesc || ('ID: ' + nodeData.id)).split(String.fromCharCode(10)).join('<br>');\n"
        replaced = True
        break

if replaced:
    with open(SERVER_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("SUCCESS: Fixed split newline in server.py!")
else:
    print("WARNING: Could not find target line!")
