import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
meta_file = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\documents\_metadata_index.json"
with open(meta_file, encoding='utf-8') as f:
    meta = json.load(f)

query = '입찰안내서상 계약상 리스크'
query_lower = query.lower()
query_tokens = re.split(r'[\s,._/?!~()\[\]]+', query_lower)
all_subs = set()
for t in query_tokens:
    if len(t) >= 2:
        all_subs.add(t)
        for suffix in ['상', '의', '에', '서', '을', '를', '은', '는', '이', '가', '으로', '로', '에서']:
            if t.endswith(suffix) and len(t) - len(suffix) >= 2:
                all_subs.add(t[:-len(suffix)])

doc = meta['입찰안내서(동탄트램).pdf']
scored = []
for s in doc.get('sections', []):
    score = 0
    title = s.get('title', '')
    title_l = title.lower()
    for kw in s.get('keywords', []):
        if kw.lower() in query_lower: score += 6
        for tok in all_subs:
            if tok in kw.lower(): score += 5
    for tok in all_subs:
        if tok in title_l: score += 10
    if title_l in query_lower: score += 15
    if score > 0:
        scored.append((score, s))

scored.sort(key=lambda x: x[0], reverse=True)
print('Query tokens/subs:', all_subs)
for sc, s in scored:
    sp = s.get('start_page', 1)
    ep = s.get('end_page', 1)
    title = s.get('title')
    print(f"Score {sc:3d} | p.{sp:3d}~{ep:3d} ({ep-sp+1:2d}p) | {title}")
