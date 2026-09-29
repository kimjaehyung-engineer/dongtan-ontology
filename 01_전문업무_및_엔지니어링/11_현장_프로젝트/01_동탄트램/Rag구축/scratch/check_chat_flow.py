import sys, json, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
rag_dir = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
sys.path.insert(0, str(rag_dir))
import server

query = "동탄역 핵심이슈는 머지?"
# Let's inspect what happens in server.py from lines 3480 to 3840
with open(server.META_INDEX_FILE, "r", encoding="utf-8") as f:
    meta_map = json.load(f)

query_lower = query.lower()
query_tokens = [w for w in re.split(r'[\s,._/?!~()\[\]]+', query_lower) if len(w) >= 1]
target_nums = server.extract_target_numbers(query_lower)
is_base = any(k in query_lower for k in ["차량기지", "건축기지", "기지", "gb"])

scored_sections = []
for dn, dm in meta_map.items():
    root = server.get_configured_docs_root()
    fp = root / dn
    if not fp.exists():
        matches = list(root.rglob(dn))
        fp = matches[0] if matches else (server.DOCS_DIR / dn)
    if not fp.exists(): continue

    doc_bonus = 0
    # ...
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

        for kw in s.get("keywords", []):
            if kw.lower() in query_lower: sc += 6
            for tok in query_tokens:
                if tok in kw.lower(): sc += 3

        if any(tok in sec_title.lower() for tok in query_tokens): sc += 15
        for tok in query_tokens:
            if tok in s.get("summary", "").lower(): sc += 2

        if sc > 0:
            scored_sections.append((sc, dn, fp, s))

scored_sections.sort(key=lambda x: x[0], reverse=True)
print(f"Top 3 scored sections:")
for sc, dn, fp, s in scored_sections[:3]:
    print(f"[{sc}] {dn} (p.{s.get('start_page')}~{s.get('end_page')}) - path: {fp}")

target_score, target_doc_name, target_file_path, best_section = scored_sections[0]
print(f"\nTarget doc name: {target_doc_name}")
print(f"Target file path: {target_file_path}")

pdf_bytes, info_msg, is_meta_only = server.get_smart_pdf_payload(target_file_path, query)
print(f"pdf_bytes is None?: {pdf_bytes is None}")
print(f"info_msg: {info_msg}")
if pdf_bytes:
    print(f"pdf_bytes length: {len(pdf_bytes)} bytes")
