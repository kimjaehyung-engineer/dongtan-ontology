import sys

target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(target_path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = """            if META_INDEX_FILE.exists():
                try:
                    with open(META_INDEX_FILE, "r", encoding="utf-8") as f:
                        meta_map = json.load(f)
                    
                    query_lower = query.lower()
                    scored_sections = []
                    for dn, dm in meta_map.items():
                        fp = DOCS_DIR / dn
                        if not fp.exists(): continue
                        for s in dm.get("sections", []):
                            sc = 0
                            for fac in s.get("facility", []):
                                if fac.lower() in query_lower: sc += 6
                            for kw in s.get("keywords", []):
                                if kw.lower() in query_lower: sc += 4
                            if s.get("title", "").lower() in query_lower: sc += 5
                            if s.get("task_id", "").lower() in query_lower: sc += 5
                            if sc > 0:
                                scored_sections.append((sc, dn, fp, s))
                    
                    scored_sections.sort(key=lambda x: x[0], reverse=True)
                    if scored_sections:
                        top_sc, target_doc_name, target_file_path, top_sec = scored_sections[0]
                        target_start_page = top_sec["start_page"]
                        matched_section_titles = [f"{s['title']} (p.{s['start_page']}~{s['end_page']})" for sc, dn, fp, s in scored_sections if dn == target_doc_name][:4]
                        source_notice = f"> 📂 **[출처 문서 자동 탐색]** **`{target_doc_name}`**의 **{top_sec['title']} (p.{top_sec['start_page']}~{top_sec['end_page']})**에서 자동 추출하여 분석했습니다.\\n\\n"
                except Exception:
                    pass"""

new_block = """            if META_INDEX_FILE.exists():
                try:
                    with open(META_INDEX_FILE, "r", encoding="utf-8") as f:
                        meta_map = json.load(f)
                    
                    query_lower = query.lower()
                    query_tokens = [w for w in re.split(r'[\\s,._/?!~()\\[\\]]+', query_lower) if len(w) >= 2]
                    
                    scored_sections = []
                    for dn, dm in meta_map.items():
                        fp = DOCS_DIR / dn
                        if not fp.exists(): continue

                        doc_bonus = 0
                        if "제안" in query_lower and "기술제안" in dn: doc_bonus += 15
                        if ("비탈면" in query_lower or "사면" in query_lower) and "비탈면" in dn: doc_bonus += 10
                        if ("가시설" in query_lower or "구조계산" in query_lower or "변전소" in query_lower) and "3편" in dn: doc_bonus += 10
                        if ("차량기지" in query_lower or "gb" in query_lower or "1공구" in query_lower or "nh" in query_lower) and "1공구" in dn: doc_bonus += 10
                        if ("2공구" in query_lower or "dt" in query_lower) and "2공구" in dn: doc_bonus += 10

                        for s in dm.get("sections", []):
                            sc = doc_bonus
                            for fac in s.get("facility", []):
                                if fac.lower() in query_lower: sc += 8
                                for tok in query_tokens:
                                    if tok in fac.lower(): sc += 3
                            for kw in s.get("keywords", []):
                                if kw.lower() in query_lower: sc += 6
                                for tok in query_tokens:
                                    if tok in kw.lower(): sc += 3
                            title_l = s.get("title", "").lower()
                            if title_l in query_lower: sc += 10
                            for tok in query_tokens:
                                if tok in title_l: sc += 4
                            task_l = s.get("task_id", "").lower()
                            if task_l in query_lower: sc += 8
                            for tok in query_tokens:
                                if tok in task_l: sc += 3

                            if sc > 0:
                                scored_sections.append((sc, dn, fp, s))
                    
                    scored_sections.sort(key=lambda x: x[0], reverse=True)
                    if scored_sections:
                        top_sc, target_doc_name, target_file_path, top_sec = scored_sections[0]
                        target_start_page = top_sec.get("start_page", 1)
                        matched_section_titles = [f"{s.get('title', '')} (p.{s.get('start_page', 1)}~{s.get('end_page', 1)})" for sc, dn, fp, s in scored_sections if dn == target_doc_name][:4]
                        source_notice = f"> 📂 **[출처 문서 자동 탐색]** **`{target_doc_name}`**의 **{top_sec.get('title', '')} (p.{top_sec.get('start_page', 1)}~{top_sec.get('end_page', 1)})**에서 자동 추출하여 분석했습니다.\\n\\n"
                except Exception:
                    pass"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully replaced routing logic in server.py")
else:
    print("Failed to find old routing block in server.py")
    sys.exit(1)
