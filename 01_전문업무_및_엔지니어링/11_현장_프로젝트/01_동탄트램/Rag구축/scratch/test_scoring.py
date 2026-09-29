import sys, os, json, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
rag_dir = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
sys.path.insert(0, str(rag_dir))
import server

query = "동탄역 핵심이슈는 머지?"
META_INDEX_FILE = server.DOCS_DIR / "_metadata_index.json"
print("META_INDEX_FILE exists:", META_INDEX_FILE.exists())
with open(META_INDEX_FILE, "r", encoding="utf-8") as f:
    meta_map = json.load(f)

query_lower = query.lower()
query_tokens = [w for w in re.split(r'[\s,._/?!~()\[\]]+', query_lower) if len(w) >= 1]
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
    if "본선" in query_lower and "본선" in dn: doc_bonus += 15
    if "동탄역" in query_lower:
        if "건축" in dn or "토목구조" in dn or "철도" in dn:
            doc_bonus += 20

    for s in dm.get("sections", []):
        sc = doc_bonus
        sec_title = s.get("title", "")
        for fac in s.get("facility", []):
            if fac.lower() in query_lower: sc += 8
            for tok in query_tokens:
                if tok in fac.lower(): sc += 3
        for kw in s.get("keywords", []):
            if kw.lower() in query_lower: sc += 6
        if any(tok in sec_title.lower() for tok in query_tokens): sc += 15
        for tok in query_tokens:
            if tok in s.get("summary", "").lower(): sc += 2
        if sc > 0:
            scored_sections.append((sc, dn, fp, s))

scored_sections.sort(key=lambda x: x[0], reverse=True)
print(f"Total scored sections: {len(scored_sections)}")
for sc, dn, fp, s in scored_sections[:10]:
    t = s.get('title')
    sp = s.get('start_page')
    ep = s.get('end_page')
    print(f"[{sc}] {dn} -> {t} (p.{sp}~{ep})")

if scored_sections:
    best = scored_sections[0]
    payload, msg, is_meta = server.get_smart_pdf_payload(best[2], query)
    print("\nPayload size:", len(payload) if payload else "None (large file)")
    print("Payload msg:", msg)
