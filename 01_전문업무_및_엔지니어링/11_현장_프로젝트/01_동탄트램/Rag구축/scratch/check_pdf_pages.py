from pathlib import Path
import pypdf

docs_dir = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\documents")
target_pdf = list(docs_dir.glob("*토질*.pdf"))[0]

reader = pypdf.PdfReader(str(target_pdf))
print(f"Total pages: {len(reader.pages)}")

# 80~120 페이지의 텍스트 길이 및 내용 샘플 확인
for p_idx in range(75, 105):
    text = reader.pages[p_idx].extract_text() or ""
    print(f"Page {p_idx+1}: text length = {len(text)}")
    if "87" in text or "지층" in text or "제안" in text or "NGB" in text:
        first_line = text.splitlines()[0] if text.splitlines() else ""
        print(f"  --> Match on Page {p_idx+1}: {first_line[:60]}")
