from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

old_guard = """    # Safe guard ONLY for HTTP 20MB limit (Gemini API payload ceiling)
    if len(sliced_bytes) > 18 * 1024 * 1024:
        while len(sorted_pages) > 5 and len(sliced_bytes) > 18 * 1024 * 1024:
            sorted_pages = sorted_pages[:int(len(sorted_pages) * 0.8)]
            sliced_bytes = slice_pdf_pages(file_path, sorted_pages)"""

new_guard = """    # 18MB 초과 시 페이지를 강제로 5장으로 줄이지 않고, Google File API 롱컨텍스트 모드로 직결 전환!
    if len(sliced_bytes) > 18 * 1024 * 1024:
        info_str = f"[Google File API 롱컨텍스트] {', '.join(matched_sections[:6])} 전체({len(sorted_pages)}p, 18MB 초과)를 자르지 않고 Google 멀티모달 통업로드로 분석합니다."
        return None, info_str, False"""

if old_guard in content:
    content = content.replace(old_guard, new_guard)
    server_path.write_text(content, encoding="utf-8")
    print("Replaced 18MB page-shrinking loop with Google File API handover!")
else:
    import re
    content = re.sub(
        r'# Safe guard ONLY for HTTP 20MB limit.*?sliced_bytes = slice_pdf_pages\(file_path, sorted_pages\)',
        new_guard,
        content,
        flags=re.DOTALL
    )
    server_path.write_text(content, encoding="utf-8")
    print("Replaced 18MB guard via regex!")
