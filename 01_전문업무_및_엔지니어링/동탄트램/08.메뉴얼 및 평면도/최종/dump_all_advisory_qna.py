import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("subcontractor_advisory_extracted.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for fname, text in data.items():
    print(f"==========================================")
    print(f"FULL TEXT: {fname}")
    print(f"==========================================")
    print(text)
    print("\n" + "="*50 + "\n")
