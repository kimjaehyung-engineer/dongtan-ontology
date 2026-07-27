import fitz
import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

subcontractor_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\협력업체 자문"

files = [f for f in os.listdir(subcontractor_dir) if f.endswith('.pdf')]

extracted = {}

for f in files:
    path = os.path.join(subcontractor_dir, f)
    doc = fitz.open(path)
    text = ""
    for i, page in enumerate(doc):
        text += f"\n--- Page {i+1} ---\n" + page.get_text()
    extracted[f] = text
    print(f"Extracted {f}: {len(text)} characters, {len(doc)} pages")

with open("subcontractor_advisory_extracted.json", "w", encoding="utf-8") as out:
    json.dump(extracted, out, ensure_ascii=False, indent=2)

print("Saved to subcontractor_advisory_extracted.json")
