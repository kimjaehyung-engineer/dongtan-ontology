import re
import sys

target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(target_path, "r", encoding="utf-8") as f:
    code = f.read()

old_start = "    # If specific borehole numbers are requested (e.g. 7~9), strictly pick those"
old_end = "    info_str = f\"[색인 라우팅] {', '.join(matched_sections)} 총 {len(sorted_pages)}페이지만 메모리에서 추출하여 분석합니다.\""

start_idx = code.find(old_start)
end_idx = code.find(old_end)

if start_idx == -1 or end_idx == -1:
    print(f"Could not find boundaries: {start_idx}, {end_idx}")
    sys.exit(1)

new_block = '''    # If specific borehole numbers are requested (e.g. 7~9), strictly pick those
    if target_nums and any(item[0] >= 40 for item in scored):
        filtered_scored = [item for item in scored if item[0] >= 35]
    else:
        # NO PAGE COUNT LIMIT: Include ALL matching sections completely!
        top_sc = scored[0][0] if scored else 0
        rel_threshold = max(3, int(top_sc * 0.35))
        filtered_scored = [item for item in scored if item[0] >= rel_threshold]

    # Collect ALL pages from all matched sections without any page limit
    for sc, s in filtered_scored:
        sec_pages = list(range(s["start_page"] - 1, s["end_page"]))
        matched_sections.append(f"{s['title']} (p.{s['start_page']}~{s['end_page']})")
        for p in sec_pages:
            target_pages.add(p)

    if not target_pages:
        matched_sections.append("전체 주요 섹션")
        for s in sections[:15]:
            matched_sections.append(f"{s['title']} (p.{s['start_page']}~{s['end_page']})")
            for p in range(s["start_page"] - 1, s["end_page"]):
                target_pages.add(p)

    sorted_pages = sorted(list(target_pages))
    sliced_bytes = slice_pdf_pages(file_path, sorted_pages)

    # Safe guard ONLY for HTTP 20MB limit (Gemini API payload ceiling)
    if len(sliced_bytes) > 18 * 1024 * 1024:
        while len(sorted_pages) > 5 and len(sliced_bytes) > 18 * 1024 * 1024:
            sorted_pages = sorted_pages[:int(len(sorted_pages) * 0.8)]
            sliced_bytes = slice_pdf_pages(file_path, sorted_pages)

    info_str = f"[색인 전수 추출] {', '.join(matched_sections[:8])} 등 총 {len(sorted_pages)}페이지 전체를 메모리에서 추출하여 분석합니다."'''

code = code[:start_idx] + new_block + code[end_idx + len(old_end):]

with open(target_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Successfully removed all page limits in server.py")
