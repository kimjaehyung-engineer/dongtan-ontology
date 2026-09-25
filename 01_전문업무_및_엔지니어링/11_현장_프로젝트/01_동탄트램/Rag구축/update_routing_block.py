import sys

target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(target_path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = """                    query_lower = query.lower()
                    query_tokens = [w for w in re.split(r'[\s,._/?!~()\[\]]+', query_lower) if len(w) >= 2]
                    
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
                                scored_sections.append((sc, dn, fp, s))"""

new_block = """                    query_lower = query.lower()
                    query_tokens = [w for w in re.split(r'[\s,._/?!~()\[\]]+', query_lower) if len(w) >= 1]
                    target_nums = extract_target_numbers(query_lower)
                    is_base = any(k in query_lower for k in ["차량기지", "건축기지", "기지", "gb"])
                    
                    scored_sections = []
                    for dn, dm in meta_map.items():
                        fp = DOCS_DIR / dn
                        if not fp.exists(): continue

                        doc_bonus = 0
                        if "제안" in query_lower and "기술제안" in dn: doc_bonus += 15
                        if ("비탈면" in query_lower or "사면" in query_lower) and "비탈면" in dn: doc_bonus += 10
                        if ("가시설" in query_lower or "구조계산" in query_lower or "변전소" in query_lower) and "3편" in dn: doc_bonus += 10
                        if (is_base or "1공구" in query_lower or "nh" in query_lower) and "1공구" in dn: doc_bonus += 15
                        if ("2공구" in query_lower or "dt" in query_lower) and "2공구" in dn: doc_bonus += 10

                        for s in dm.get("sections", []):
                            sc = doc_bonus
                            sec_title = s.get("title", "")
                            m = re.search(r'(?:GB|NH|DT)-(\d+)', sec_title)
                            sec_num = int(m.group(1)) if m else None

                            for fac in s.get("facility", []):
                                if fac.lower() in query_lower: sc += 8
                                for tok in query_tokens:
                                    if tok in fac.lower(): sc += 3
                            if is_base and "차량기지" in s.get("facility", []):
                                sc += 15
                            elif not is_base and "본선" in s.get("facility", []):
                                sc += 5

                            if sec_num is not None and sec_num in target_nums:
                                sc += 40  # Massive priority for explicit borehole number/range

                            for kw in s.get("keywords", []):
                                if kw.lower() in query_lower: sc += 6
                                for tok in query_tokens:
                                    if tok in kw.lower(): sc += 3
                            title_l = sec_title.lower()
                            if title_l in query_lower: sc += 10
                            for tok in query_tokens:
                                if tok in title_l: sc += 4
                            task_l = s.get("task_id", "").lower()
                            if task_l in query_lower: sc += 8
                            for tok in query_tokens:
                                if tok in task_l: sc += 3

                            if sc > 0:
                                scored_sections.append((sc, dn, fp, s))"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully updated routing scoring block")
else:
    print("Failed to find old routing block")
    sys.exit(1)
