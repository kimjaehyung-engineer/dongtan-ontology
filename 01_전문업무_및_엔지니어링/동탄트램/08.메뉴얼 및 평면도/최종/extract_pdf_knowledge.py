import fitz
import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\분야별설계기준(설계사정리)"

pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]

extracted_knowledge = {}

for f in pdf_files:
    pdf_path = os.path.join(pdf_dir, f)
    doc = fitz.open(pdf_path)
    text = ""
    for i, page in enumerate(doc):
        text += f"\n--- Page {i+1} ---\n" + page.get_text()
    
    extracted_knowledge[f] = text
    print(f"Extracted {f}: {len(text)} characters")

with open("pdf_extracted_knowledge.json", "w", encoding="utf-8") as out:
    json.dump(extracted_knowledge, out, ensure_ascii=False, indent=2)

print("Saved all extracted text to pdf_extracted_knowledge.json")
