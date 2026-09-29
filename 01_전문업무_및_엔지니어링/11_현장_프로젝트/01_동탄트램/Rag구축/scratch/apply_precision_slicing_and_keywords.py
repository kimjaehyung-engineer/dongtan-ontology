import sys, re, json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

rag_dir = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
meta_file = rag_dir / "documents" / "_metadata_index.json"
server_file = rag_dir / "server.py"

# 1. Update _metadata_index.json for 입찰안내서 sections with meaningful keywords
if meta_file.exists():
    data = json.load(open(meta_file, encoding='utf-8'))
    if "입찰안내서(동탄트램).pdf" in data:
        doc = data["입찰안내서(동탄트램).pdf"]
        for s in doc.get("sections", []):
            title = s.get("title", "")
            kws = list(s.get("keywords", []))
            
            if "계약" in title or "특수조건" in title or "리스크" in title:
                kws.extend(["계약", "계약상", "리스크", "특수조건", "설계변경", "위험", "책임", "지연배상금", "하자"])
            if "유의사항" in title or "입찰안내서" in title:
                kws.extend(["입찰안내서", "입찰안내서상", "유의사항", "일반사항", "입찰조건", "참가자격"])
            if "실시설계" in title or "지침" in title:
                kws.extend(["실시설계", "설계지침", "토목", "궤도", "건축", "정거장"])
            if "시공" in title:
                kws.extend(["시공지침", "공사", "안전관리", "품질관리"])
            if "평가" in title or "배점" in title:
                kws.extend(["기술제안평가", "배점기준", "감점"])
                
            s["keywords"] = list(set(kws))
        
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("1. Enriched _metadata_index.json keywords for 입찰안내서 successfully!")

# 2. Update get_smart_pdf_payload in server.py with subword matching
content = server_file.read_text(encoding="utf-8")

old_code = '''    scored = []
    for s in sections:
        score = 0
        sec_title = s.get("title", "")
        m = re.search(r'(?:GB|NH|DT)-(\d+)', sec_title)
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
            scored.append((score, s))'''

new_code = '''    query_tokens = re.split(r'[\s,._/?!~()\[\]]+', query_lower)
    all_subs = set()
    for t in query_tokens:
        if len(t) >= 2:
            all_subs.add(t)
            for suffix in ['상', '의', '에', '서', '을', '를', '은', '는', '이', '가', '으로', '로', '에서']:
                if t.endswith(suffix) and len(t) - len(suffix) >= 2:
                    all_subs.add(t[:-len(suffix)])

    scored = []
    for s in sections:
        score = 0
        sec_title = s.get("title", "")
        sec_title_l = sec_title.lower()
        m = re.search(r'(?:GB|NH|DT)-(\d+)', sec_title)
        sec_num = int(m.group(1)) if m else None

        # facility matching
        for fac in s.get("facility", []):
            fac_l = fac.lower()
            if fac_l in query_lower:
                score += 8
            for tok in all_subs:
                if tok in fac_l:
                    score += 4
        if is_base and "차량기지" in s.get("facility", []):
            score += 15
        elif not is_base and "본선" in s.get("facility", []):
            score += 5

        # exact borehole number match (massive bonus)
        if sec_num is not None and sec_num in target_nums:
            score += 40

        for kw in s.get("keywords", []):
            kw_l = kw.lower()
            if kw_l in query_lower:
                score += 6
            for tok in all_subs:
                if tok in kw_l:
                    score += 5

        # Token & subword matching against section title
        for tok in all_subs:
            if tok in sec_title_l:
                score += 10
        if sec_title_l in query_lower:
            score += 15

        if score > 0:
            scored.append((score, s))'''

if old_code in content:
    content = content.replace(old_code, new_code)
    server_file.write_text(content, encoding="utf-8")
    print("2. Updated server.py section matching with Korean subword & keyword logic!")
else:
    print("Warning: old_code not found in server.py")
