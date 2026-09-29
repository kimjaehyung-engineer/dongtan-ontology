import re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

server_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
if not server_file.exists():
    print(f"Error: {server_file} not found")
    sys.exit(1)

content = server_file.read_text(encoding="utf-8")

# 1. Optimize slice_pdf_pages to avoid font/image duplication bloat
old_slice = '''def slice_pdf_pages(file_path, page_indices):
    if HAS_FITZ:
        doc = fitz.open(file_path)
        new_doc = fitz.open()
        for idx in page_indices:
            if 0 <= idx < len(doc):
                new_doc.insert_pdf(doc, from_page=idx, to_page=idx)
        pdf_bytes = new_doc.tobytes()
        doc.close()
        new_doc.close()
        return pdf_bytes'''

new_slice = '''def slice_pdf_pages(file_path, page_indices):
    if HAS_FITZ:
        doc = fitz.open(file_path)
        valid_indices = sorted(list(set([idx for idx in page_indices if 0 <= idx < len(doc)])))
        if valid_indices:
            doc.select(valid_indices)
            pdf_bytes = doc.tobytes(garbage=4, deflate=True)
        else:
            pdf_bytes = b""
        doc.close()
        return pdf_bytes'''

if old_slice in content:
    content = content.replace(old_slice, new_slice)
    print("1. Successfully optimized slice_pdf_pages with doc.select and deflate!")
else:
    print("Warning: old_slice not found")

# 2. Limit section page accumulation in get_smart_pdf_payload
old_accum = '''    # Collect ALL pages from all matched sections without any page limit
    for sc, s in filtered_scored:
        sec_pages = list(range(s["start_page"] - 1, s["end_page"]))
        matched_sections.append(f"{s['title']} (p.{s['start_page']}~{s['end_page']})")
        for p in sec_pages:
            target_pages.add(p)'''

new_accum = '''    # Collect top-scoring sections up to max 75 pages to prevent bloat and guarantee sub-30s latency
    accumulated_pages = 0
    for sc, s in filtered_scored:
        sp = s["start_page"] - 1
        ep = s["end_page"]
        sec_len = ep - sp
        if accumulated_pages > 0 and accumulated_pages + sec_len > 75:
            # We already have the top match; avoid dragging lower-priority sections
            continue
        matched_sections.append(f"{s['title']} (p.{s['start_page']}~{s['end_page']})")
        for p in range(sp, ep):
            target_pages.add(p)
        accumulated_pages += sec_len'''

if old_accum in content:
    content = content.replace(old_accum, new_accum)
    print("2. Successfully capped section page accumulation to top relevant sections!")
else:
    print("Warning: old_accum not found")

# 3. Optimize models_to_try and prompt in inline PDF block (around line 3528)
old_inline_block = '''                models_to_try = [
                    "gemini-flash-lite-latest",
                    "gemini-3.5-flash-lite",
                    "gemini-3.6-flash",
                    "gemini-3.1-flash-lite",
                    "gemini-flash-latest"
                ]'''

new_inline_block = '''                models_to_try = [
                    "gemini-3.6-flash",
                    "gemini-3.5-flash-lite",
                    "gemini-flash-latest"
                ]'''

if old_inline_block in content:
    content = content.replace(old_inline_block, new_inline_block)
    print("3. Successfully prioritized gemini-3.6-flash in inline models_to_try!")
else:
    print("Warning: old_inline_block not found")

# 4. Optimize inline systemInstruction to enforce Table + Bullets
old_instruction = '''                                    "1. 본문의 비교 표(Table), 수치, 규격, 시공 및 시험 기준을 누락 없이 정밀하게 마크다운 표와 항목으로 정리하세요.\\n"
                                    "2. 문서에 없는 내용은 억지로 지어내지 말고 문서에 없다고 명확히 밝히세요."'''

new_instruction = '''                                    "[핵심 답변 규칙 (가독성 & 속도 최적화)]\\n"
                                    "1. [정확한 원본 페이지 번호 명시]: 모든 주요 사실과 조항마다 수록된 '정확한 원본 페이지 번호(예: p.87, p.142 등)'를 반드시 명시하세요.\\n"
                                    "2. [핵심 요약 표(Table) 우선 제시]: 장황한 줄글 대신, 핵심 내용(항목, 주요 조항/리스크 내용, 근거 페이지, 실무 대응방안)을 마크다운 표로 먼저 일목요연하게 정리하세요.\\n"
                                    "3. [두괄식 글머리 기호 서술]: 표 아래에 주요 핵심 포인트를 3~5개 항목의 간결한 글머리 기호(Bullet points)로 요약하세요. 불필요하게 긴 서술은 지양하고 핵심만 압축하세요.\\n"
                                    "4. [팩트 기반]: 추측하지 말고 문서에 명시된 사실만을 정확히 인용하세요."'''

if old_instruction in content:
    content = content.replace(old_instruction, new_instruction)
    print("4. Successfully updated inline systemInstruction with structured table and bullet rules!")
else:
    print("Warning: old_instruction not found")

server_file.write_text(content, encoding="utf-8")
print("\nAll optimizations saved to server.py successfully!")
