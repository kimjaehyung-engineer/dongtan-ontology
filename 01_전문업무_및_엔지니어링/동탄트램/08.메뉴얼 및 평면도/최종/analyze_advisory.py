import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("subcontractor_advisory_extracted.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for fname, text in data.items():
    print(f"==========================================")
    print(f"FILE: {fname}")
    print(f"==========================================")
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for line in lines[:60]:
        print(line)
    print("\n" + "="*50 + "\n")
