# -*- coding: utf-8 -*-
"""
9대 기술제안서 섹션 페이지 구간 연속화 및 정밀 키워드(정거장 번호, 시설물, 도메인) 전수 색인 고도화 스크립트
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import re
import json
from pathlib import Path
from pypdf import PdfReader

DOCS_ROOT = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\Rag구축\01_SOURCE_DOCUMENTS\02_기본설계_기술제안")
RAG_DIR = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
META_INDEX_FILE = RAG_DIR / "documents" / "_metadata_index.json"

KEYWORDS_CATALOG = [
    '301', '302', '303', '101', '107', '112', '114', '201', '209', '210', 'S01',
    '병점', '망포', '동탄', '오산', '차량기지', '변전소', '변전실', '환승', '지하차도',
    '승강장', '가시설', '비탈면', '무도상', '분기기', '충전', 'lte-r', 'cbtc', 'u타입',
    '내진', '침하', '경관', '환기덕트', '공조', '소방', '수전', '배전'
]

def extract_enriched_proposals():
    results = {}
    for f in sorted(DOCS_ROOT.glob("*.pdf")):
        reader = PdfReader(str(f))
        total_p = len(reader.pages)
        page_texts = [reader.pages[i].extract_text() or "" for i in range(total_p)]
        
        raw_sections = []
        for idx, text in enumerate(page_texts):
            p_num = idx + 1
            m = re.search(r'제안번호\s*([가-힣\w\s,]+-\d{2})\s*(?:기술적\s*과제)?([^\n\r]+)?', text)
            if m:
                code = m.group(1).strip()
                desc = (m.group(2) or "").strip()
                full_title = f"[{code}] {desc}" if desc else f"[{code}] 기술제안 세부내용"
                raw_sections.append({
                    "task_id": code,
                    "title": full_title[:90],
                    "start_page": p_num
                })
        
        # If no explicit sections found
        if not raw_sections:
            sections = [
                {
                    "title": "제1장 제안개요 및 핵심요약",
                    "task_id": f"{f.stem}-ch1",
                    "start_page": 1,
                    "end_page": min(3, total_p)
                },
                {
                    "title": "제2장 기술제안 세부사항",
                    "task_id": f"{f.stem}-ch2",
                    "start_page": min(4, total_p),
                    "end_page": total_p
                }
            ]
        else:
            # Sort by start_page
            raw_sections.sort(key=lambda x: x["start_page"])
            
            # Ensure overview chapter if first section starts > 1
            sections = []
            if raw_sections[0]["start_page"] > 1:
                sections.append({
                    "task_id": f"{f.stem}-overview",
                    "title": "제1장 제안개요 및 총괄 요약",
                    "start_page": 1,
                    "end_page": raw_sections[0]["start_page"] - 1
                })
            
            for i, sec in enumerate(raw_sections):
                start_p = sec["start_page"]
                end_p = raw_sections[i+1]["start_page"] - 1 if (i + 1 < len(raw_sections)) else total_p
                if end_p < start_p: end_p = start_p
                sections.append({
                    "task_id": sec["task_id"],
                    "title": sec["title"],
                    "start_page": start_p,
                    "end_page": end_p
                })
        
        # Now scan text in each section's exact page range to collect keywords & facilities
        for s in sections:
            sp = s["start_page"]
            ep = s["end_page"]
            sec_text = " ".join(page_texts[sp-1:ep])
            
            # Matched keywords
            kws = [s["task_id"]]
            for kw in KEYWORDS_CATALOG:
                if kw in sec_text and kw not in kws:
                    kws.append(kw)
            
            facilities = []
            if any(k in sec_text for k in ['차량기지', '기지', '검수고']): facilities.append('차량기지')
            if any(k in sec_text for k in ['정거장', '역사', '승강장', '환승']): facilities.append('정거장')
            if any(k in sec_text for k in ['본선', '1공구', '2공구', '노선']): facilities.append('본선')
            for stn in ['301', '302', '303', '107', '114', '201', '209', '210', '병점', '망포', '동탄', '오산']:
                if stn in sec_text and stn not in facilities:
                    facilities.append(stn)
            if not facilities:
                facilities = ['전구간']
            
            s["facility"] = facilities
            s["keywords"] = kws

        results[f.name] = {
            "total_pages": total_p,
            "sections": sections
        }
        print(f"[{f.name}] ({total_p}p, {len(sections)} sections indexed with deep keywords)")
    
    return results

def update_metadata_index():
    print("=== Extracting enriched metadata across 9 proposal PDFs ===")
    enriched = extract_enriched_proposals()

    meta_map = {}
    if META_INDEX_FILE.exists():
        with open(META_INDEX_FILE, "r", encoding="utf-8") as f:
            meta_map = json.load(f)

    for doc_name, data in enriched.items():
        meta_map[doc_name] = data

    with open(META_INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(meta_map, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Successfully updated {META_INDEX_FILE} with deep station and facility keywords!")

if __name__ == "__main__":
    update_metadata_index()
