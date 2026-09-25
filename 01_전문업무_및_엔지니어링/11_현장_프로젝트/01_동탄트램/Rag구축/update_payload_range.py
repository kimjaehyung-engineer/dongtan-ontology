import re
import sys

target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(target_path, "r", encoding="utf-8") as f:
    code = f.read()

# Helper function to be added before get_smart_pdf_payload
helper_code = '''def extract_target_numbers(query):
    nums = set()
    # range like 7~9, 7-9, 7 - 9
    for m in re.finditer(r'(\\d+)\\s*[~-]\\s*(\\d+)', query):
        try:
            s_n, e_n = int(m.group(1)), int(m.group(2))
            if s_n <= e_n and e_n - s_n <= 30:
                nums.update(range(s_n, e_n + 1))
        except ValueError:
            pass
    # single like 7번, GB-7, 7호, 7
    for m in re.finditer(r'(?:gb|nh|dt|공번|시추공|시추|번)?\\s*(\\d+)\\s*(?:번|호|공)?', query, re.I):
        try:
            val = int(m.group(1))
            if val < 200:
                nums.add(val)
        except ValueError:
            pass
    return nums

'''

if "def extract_target_numbers(" not in code:
    pos = code.find("def get_smart_pdf_payload")
    code = code[:pos] + helper_code + code[pos:]
    print("Added extract_target_numbers helper")

# Now update get_smart_pdf_payload
old_func_start = "def get_smart_pdf_payload(file_path, query=\"\"):"
old_func_end = "def get_server_ip():"

start_idx = code.find(old_func_start)
end_idx = code.find(old_func_end)

if start_idx == -1 or end_idx == -1:
    print(f"Could not find get_smart_pdf_payload boundaries: {start_idx}, {end_idx}")
    sys.exit(1)

new_payload_func = '''def get_smart_pdf_payload(file_path, query=""):
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    meta_map = {}
    if META_INDEX_FILE.exists():
        try:
            with open(META_INDEX_FILE, "r", encoding="utf-8") as f:
                meta_map = json.load(f)
        except Exception:
            pass

    doc_meta = meta_map.get(file_path.name)
    if not doc_meta and file_size_mb <= 15.0:
        with open(file_path, "rb") as f:
            return f.read(), "", False

    if not doc_meta and file_size_mb > 15.0:
        indices = list(range(15))
        return slice_pdf_pages(file_path, indices), f"[안내] 20MB 제한으로 전체 중 주요 15페이지만 로드되었습니다.", False

    sections = doc_meta.get("sections", [])
    query_lower = query.lower()
    is_pure_toc = any(k in query_lower for k in ["목차 보여", "색인 보여", "문서 구조", "목차 확인"])
    if is_pure_toc and len(query.strip()) <= 30:
        overview_text = f"### [{doc_meta.get('document_name')}] 정밀 탐색 색인 정보\\n"
        overview_text += f"- 총 페이지: {doc_meta.get('total_pages')}p\\n"
        overview_text += f"- 개요: {doc_meta.get('description')}\\n\\n"
        overview_text += "| 섹션ID | 분류 | 제목 | 페이지 | 대상시설 |\\n"
        overview_text += "| :--- | :--- | :--- | :---: | :--- |\\n"
        for s in sections:
            fac = ", ".join(s.get("facility", []))
            task_val = s.get("task_id", s.get("section_id", "-"))
            overview_text += f"| {s.get('section_id', '-')} | {task_val} | {s.get('title', '-')} | **p.{s.get('start_page', 1)}~{s.get('end_page', 1)}** | {fac} |\\n"
        return None, overview_text, True

    target_nums = extract_target_numbers(query_lower)
    is_base = any(k in query_lower for k in ["차량기지", "건축기지", "기지", "gb"])

    scored = []
    for s in sections:
        score = 0
        sec_title = s.get("title", "")
        m = re.search(r'(?:GB|NH|DT)-(\\d+)', sec_title)
        sec_num = int(m.group(1)) if m else None

        # facility matching
        for fac in s.get("facility", []):
            if fac.lower() in query_lower:
                score += 8
        if is_base and "차량기지" in s.get("facility", []):
            score += 15
        elif not is_base and "본선" in s.get("facility", []):
            score += 5

        # exact borehole number match (massive bonus)
        if sec_num is not None and sec_num in target_nums:
            score += 40

        for kw in s.get("keywords", []):
            if kw.lower() in query_lower:
                score += 4
        if sec_title.lower() in query_lower:
            score += 6

        if score > 0:
            scored.append((score, s))

    scored.sort(key=lambda x: x[0], reverse=True)
    target_pages = set()
    matched_sections = []

    # If specific borehole numbers are requested (e.g. 7~9), strictly pick those
    if target_nums and any(item[0] >= 40 for item in scored):
        filtered_scored = [item for item in scored if item[0] >= 35]
        max_limit = 12
    else:
        # If whole vehicle base is requested, allow all GB-1~9 (p.40~54, 15 pages)
        top_sc = scored[0][0] if scored else 0
        rel_threshold = max(3, int(top_sc * 0.45))
        filtered_scored = [item for item in scored if item[0] >= rel_threshold]
        max_limit = 16 if is_base else 12

    for sc, s in filtered_scored:
        sec_pages = list(range(s["start_page"] - 1, s["end_page"]))
        if target_pages and len(target_pages) + len(sec_pages) > (max_limit + 2):
            break
        matched_sections.append(f"{s['title']} (p.{s['start_page']}~{s['end_page']})")
        for p in sec_pages:
            target_pages.add(p)
        if len(target_pages) >= max_limit:
            break

    if not target_pages:
        matched_sections.append("주요 대표 시작 페이지")
        rep_pages = [1, 7, 42, 93, 126, 129, 154, 170, 186, 192, 196, 198, 219]
        for rp in rep_pages:
            if rp - 1 < doc_meta.get("total_pages", 221):
                target_pages.add(rp - 1)

    sorted_pages = sorted(list(target_pages))
    sliced_bytes = slice_pdf_pages(file_path, sorted_pages)
    info_str = f"[색인 라우팅] {', '.join(matched_sections)} 총 {len(sorted_pages)}페이지만 메모리에서 추출하여 분석합니다."
    return sliced_bytes, info_str, False

'''

code = code[:start_idx] + new_payload_func + code[end_idx:]
print("Updated get_smart_pdf_payload")

with open(target_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved server.py")
