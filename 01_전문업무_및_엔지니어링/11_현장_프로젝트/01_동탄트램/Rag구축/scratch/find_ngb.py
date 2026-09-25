from pathlib import Path
import pypdf

docs_dir = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\documents")
target_pdf = None
for f in docs_dir.glob("*.pdf"):
    if "토질" in f.name:
        target_pdf = f
        break

print("Checking PDF:", target_pdf)
if target_pdf:
    reader = pypdf.PdfReader(str(target_pdf))
    print(f"Total pages: {len(reader.pages)}")
    
    # 80~100 페이지 검색
    for p_idx in range(min(120, len(reader.pages))):
        text = reader.pages[p_idx].extract_text() or ""
        if "NGB" in text or "지층분포 특성" in text:
            print(f"Found match on PDF Page {p_idx + 1}!")
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            for l in lines[:15]:
                print("  ", l)
            break
