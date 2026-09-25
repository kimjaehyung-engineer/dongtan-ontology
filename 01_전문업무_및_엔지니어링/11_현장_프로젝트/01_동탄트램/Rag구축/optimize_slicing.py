target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(target_path, "r", encoding="utf-8") as f:
    content = f.read()

old_slicing = """    scored.sort(key=lambda x: x[0], reverse=True)
    target_pages = set()
    matched_sections = []
    if scored:
        for sc, s in scored:
            sec_pages = list(range(s["start_page"] - 1, s["end_page"]))
            if target_pages and len(target_pages) + len(sec_pages) > 25:
                break
            matched_sections.append(f"{s['title']} (p.{s['start_page']}~{s['end_page']})")
            for p in sec_pages:
                target_pages.add(p)
            if len(target_pages) >= 20:
                break
    else:
        matched_sections.append("주요 대표 시작 페이지")
        rep_pages = [1, 7, 42, 93, 126, 129, 154, 170, 186, 192, 196, 198, 219]
        for rp in rep_pages:
            if rp - 1 < doc_meta.get("total_pages", 221):
                target_pages.add(rp - 1)

    sorted_pages = sorted(list(target_pages))
    if len(sorted_pages) > 30:
        sorted_pages = sorted_pages[:30]"""

new_slicing = """    scored.sort(key=lambda x: x[0], reverse=True)
    target_pages = set()
    matched_sections = []
    if scored:
        top_sc = scored[0][0]
        # 핵심 연관도 섹션만 선별 (최고점수의 50% 이상만 수용하여 불필요한 페이지 배제)
        rel_threshold = max(3, int(top_sc * 0.45))
        filtered_scored = [item for item in scored if item[0] >= rel_threshold]

        for sc, s in filtered_scored:
            sec_pages = list(range(s["start_page"] - 1, s["end_page"]))
            if target_pages and len(target_pages) + len(sec_pages) > 14:
                break
            matched_sections.append(f"{s['title']} (p.{s['start_page']}~{s['end_page']})")
            for p in sec_pages:
                target_pages.add(p)
            if len(target_pages) >= 10:
                break

    if not target_pages:
        matched_sections.append("주요 대표 시작 페이지")
        rep_pages = [1, 7, 42, 93, 126, 129, 154, 170, 186, 192, 196, 198, 219]
        for rp in rep_pages:
            if rp - 1 < doc_meta.get("total_pages", 221):
                target_pages.add(rp - 1)

    sorted_pages = sorted(list(target_pages))
    if len(sorted_pages) > 12:
        sorted_pages = sorted_pages[:12]"""

if old_slicing in content:
    content = content.replace(old_slicing, new_slicing)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully optimized slicing limits (10~12 pages max)")
else:
    print("Failed to find old slicing block")
