import fitz  # PyMuPDF
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\분야별설계기준(설계사정리)"

pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]

print("Found PDF files:")
for f in pdf_files:
    pdf_path = os.path.join(pdf_dir, f)
    doc = fitz.open(pdf_path)
    print(f"\n--- PDF: {f} (Pages: {len(doc)}) ---")
    full_text = ""
    for page_num in range(min(5, len(doc))): # print first 5 pages
        full_text += f"\n[Page {page_num+1}]\n" + doc[page_num].get_text()
    print(full_text[:1500]) # First 1500 chars
