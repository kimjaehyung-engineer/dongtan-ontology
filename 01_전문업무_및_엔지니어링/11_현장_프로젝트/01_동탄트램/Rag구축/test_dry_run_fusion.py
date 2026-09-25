# -*- coding: utf-8 -*-
import sys, json, re
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
import graph_intelligence

DOCS_DIR = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\documents")
META_INDEX_FILE = DOCS_DIR / "_metadata_index.json"

query = "차량기지 연약지반 시추공 N값 알려줘"
graph_intel = graph_intelligence.extract_graph_intelligence(query)
matched_graph_holes = set(graph_intel.get("matched_holes", []))
target_graph_docs = set(graph_intel.get("target_docs", []))
target_graph_pages = graph_intel.get("target_pages", [])

print("Graph Intelligence Summary:", graph_intel["summary"])
print("Matched Holes:", matched_graph_holes)
print("Target Docs from Graph:", target_graph_docs)

with open(META_INDEX_FILE, "r", encoding="utf-8") as f:
    meta_map = json.load(f)

scored_sections = []
for dn, dm in meta_map.items():
    doc_bonus = 0
    if dn in target_graph_docs:
        doc_bonus += 50
    for s in dm.get("sections", []):
        sc = doc_bonus
        sec_title = s.get("title", "")
        for gh in matched_graph_holes:
            if gh.lower() in sec_title.lower() or gh.lower() in " ".join(s.get("keywords", [])).lower():
                sc += 150
        sec_start = s.get("start_page", 1)
        sec_end = s.get("end_page", 1)
        for gp in target_graph_pages:
            if sec_start <= gp <= sec_end:
                sc += 100
        if sc > 0:
            scored_sections.append((sc, dn, s))

scored_sections.sort(key=lambda x: x[0], reverse=True)
print("\nTop 5 Scored Sections with Graph Boost:")
for sc, dn, s in scored_sections[:5]:
    print(f" - Score: {sc:4d} | Doc: {dn} | Section: {s.get('title')} (p.{s.get('start_page')}~{s.get('end_page')})")
