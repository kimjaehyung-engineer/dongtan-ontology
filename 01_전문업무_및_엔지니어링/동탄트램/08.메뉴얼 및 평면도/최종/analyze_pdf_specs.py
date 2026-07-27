import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("pdf_extracted_knowledge.json", "r", encoding="utf-8") as f:
    knowledge = json.load(f)

print("=== DESIGN CRITERIA KNOWLEDGE ANALYSIS ===\n")

for pdf_name, text in knowledge.items():
    print(f"==========================================")
    print(f"FILE: {pdf_name}")
    print(f"==========================================")
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Print key headings or numbers/standards mentioned
    headings = []
    for line in lines:
        if re.match(r'^(제?\d+장|\d+\.\d+|\<|\[|•|▪|\#)', line):
            headings.append(line)
            
    print(f"Total lines: {len(lines)}, Headings/Sections found: {len(headings)}")
    print("Sample Headings/Key Items:")
    for h in headings[:15]:
        print("  *", h)
    print("\n")
