# -*- coding: utf-8 -*-
"""
server.py의 다중 공종 융합(Multi-Doc Fusion)에서
1) 동일 공종 중복 배제 (도메인별 최고득점 1개 문서만 선발: 전기, 건축, 토질·기초, 토목구조 등)
2) 문서당 최대 5쪽 제한으로 총 10~13쪽 초경량 융합 (응답 속도 15초 이내 보장)
을 적용하는 최적화 패치
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

# 1. doc_groups -> domain_groups 기반 중복 배제 선발 로직으로 교체
old_candidate_block = """                    doc_groups = {}
                    for sc, dn, fp, s in scored_sections:
                        if dn not in doc_groups:
                            doc_groups[dn] = {"max_score": sc, "file_path": fp, "sections": []}
                        doc_groups[dn]["sections"].append((sc, s))
                        if sc > doc_groups[dn]["max_score"]:
                            doc_groups[dn]["max_score"] = sc

                    sorted_doc_list = sorted(doc_groups.items(), key=lambda x: x[1]["max_score"], reverse=True)
                    
                    use_multi_doc_fusion = False
                    candidate_docs = []
                    if scored_sections and is_interdisciplinary:
                        top_sc = scored_sections[0][0]
                        min_sc = max(35, int(top_sc * 0.40))
                        for dn, ddata in sorted_doc_list:
                            if ddata["max_score"] >= min_sc and ddata["file_path"].exists():
                                candidate_docs.append((dn, ddata["file_path"], ddata["sections"]))
                                if len(candidate_docs) >= 4:
                                    break
                        if len(candidate_docs) >= 2:
                            use_multi_doc_fusion = True"""

new_candidate_block = """                    def get_domain_key(name):
                        if "전기" in name: return "전기"
                        if "건축" in name: return "건축"
                        if "토질" in name: return "토질 및 기초"
                        if "토목구조" in name: return "토목구조"
                        if "토목시공" in name: return "토목시공"
                        if "철도" in name or "궤도" in name: return "철도·궤도"
                        if "신호" in name: return "신호"
                        if "통신" in name: return "통신"
                        if "기계" in name: return "기계설비"
                        return name

                    # 동일 공종 중복 배제: 도메인별 최고득점 문서 1개씩 선발
                    domain_groups = {}
                    for sc, dn, fp, s in scored_sections:
                        dom = get_domain_key(dn)
                        if dom not in domain_groups:
                            domain_groups[dom] = {"max_score": sc, "doc_name": dn, "file_path": fp, "sections": []}
                        domain_groups[dom]["sections"].append((sc, s))
                        if sc > domain_groups[dom]["max_score"]:
                            domain_groups[dom]["max_score"] = sc
                            domain_groups[dom]["doc_name"] = dn
                            domain_groups[dom]["file_path"] = fp

                    sorted_domains = sorted(domain_groups.items(), key=lambda x: x[1]["max_score"], reverse=True)
                    
                    use_multi_doc_fusion = False
                    candidate_docs = []
                    if scored_sections and is_interdisciplinary:
                        top_sc = scored_sections[0][0]
                        min_sc = max(35, int(top_sc * 0.35))
                        for dom, ddata in sorted_domains:
                            if ddata["max_score"] >= min_sc and ddata["file_path"].exists():
                                candidate_docs.append((ddata["doc_name"], ddata["file_path"], ddata["sections"]))
                                if len(candidate_docs) >= 4:
                                    break
                        if len(candidate_docs) >= 2:
                            use_multi_doc_fusion = True"""

if old_candidate_block in content:
    content = content.replace(old_candidate_block, new_candidate_block, 1)
    print("1. Domain deduplication logic integrated.")
else:
    print("Warning: old_candidate_block not found!")

# 2. 문서당 최대 5쪽 제한으로 총 슬라이스 페이지 경량화
old_slice_loop = """                        reader = pypdf.PdfReader(str(fp))
                        num_pages = len(reader.pages)
                        doc_page_set = set()
                        for sc, s in d_secs[:2]:
                            sp = max(0, s.get("start_page", 1) - 1)
                            ep = min(num_pages, s.get("end_page", 1))
                            if len(doc_page_set) + (ep - sp) <= 8 or not doc_page_set:
                                for p in range(sp, ep):
                                    doc_page_set.add(p)
                                all_matched_titles.append(f"[{short_name}] {s.get('title', '')} (p.{sp+1}~{ep})")
                                all_active_sections.append({
                                    "title": f"[{short_name}] {s.get('title', '')}",
                                    "start_page": sp + 1,
                                    "end_page": ep,
                                    "section_id": s.get("section_id", "")
                                })"""

new_slice_loop = """                        reader = pypdf.PdfReader(str(fp))
                        num_pages = len(reader.pages)
                        doc_page_set = set()
                        for sc, s in d_secs[:2]:
                            sp = max(0, s.get("start_page", 1) - 1)
                            ep = min(num_pages, s.get("end_page", 1))
                            if ep - sp > 5:
                                ep = sp + 5
                            if len(doc_page_set) + (ep - sp) <= 5 or not doc_page_set:
                                actual_ep = min(ep, sp + (5 - len(doc_page_set))) if len(doc_page_set) > 0 else min(ep, sp + 5)
                                for p in range(sp, actual_ep):
                                    doc_page_set.add(p)
                                all_matched_titles.append(f"[{short_name}] {s.get('title', '')} (p.{sp+1}~{actual_ep})")
                                all_active_sections.append({
                                    "title": f"[{short_name}] {s.get('title', '')}",
                                    "start_page": sp + 1,
                                    "end_page": actual_ep,
                                    "section_id": s.get("section_id", "")
                                })"""

if old_slice_loop in content:
    content = content.replace(old_slice_loop, new_slice_loop, 1)
    print("2. 5-page per domain cap integrated.")
else:
    print("Warning: old_slice_loop not found!")

server_path.write_text(content, encoding="utf-8")
print("Optimization applied successfully!")
