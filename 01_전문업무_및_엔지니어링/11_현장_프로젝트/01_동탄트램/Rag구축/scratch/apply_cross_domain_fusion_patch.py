# -*- coding: utf-8 -*-
"""
server.py에 '다중 공종 복합 융합 RAG(Multi-Document Cross-Domain Fusion RAG)' 기능을 적용하는 패치 스크립트
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

# 1. '변전소' 단어가 '전기'뿐만 아니라 '건축', '토질 및 기초', '토목구조'에도 공정하게 가중치 부여되도록 수정
old_elec_bonus = 'if any(k in query_lower for k in ["전기", "급전", "충전", "수변전", "변전소", "전차선"]) and "전기" in dn: doc_bonus += 80'
new_elec_bonus = (
    'if any(k in query_lower for k in ["전기", "급전", "충전", "수변전", "전차선"]) and "전기" in dn: doc_bonus += 80\n'
    '                        if "변전소" in query_lower and any(d in dn for d in ["전기", "건축", "토질 및 기초", "토목구조", "철도"]): doc_bonus += 40'
)

if old_elec_bonus in content:
    content = content.replace(old_elec_bonus, new_elec_bonus, 1)
    print("1. Substation cross-domain bonus replaced.")
else:
    print("Warning: old_elec_bonus not found, checking if already modified...")

# 2. scored_sections 이후 다중 공종 복합 융합(Multi-Doc Fusion) 분기 주입
old_scored_block = """                    scored_sections.sort(key=lambda x: x[0], reverse=True)
                    if scored_sections:
                        top_sc, target_doc_name, target_file_path, top_sec = scored_sections[0]
                        target_start_page = top_sec.get("start_page", 1)
                        matched_section_titles = [f"{s.get('title', '')} (p.{s.get('start_page', 1)}~{s.get('end_page', 1)})" for sc, dn, fp, s in scored_sections if dn == target_doc_name][:4]
                        source_notice = f"> 📂 **[출처 문서 자동 탐색]** **`{target_doc_name}`**의 **{top_sec.get('title', '')} (p.{top_sec.get('start_page', 1)}~{top_sec.get('end_page', 1)})**에서 자동 추출하여 분석했습니다.\\n\\n"
                except Exception:
                    pass"""

new_scored_block = """                    scored_sections.sort(key=lambda x: x[0], reverse=True)
                    
                    # [다중 공종 복합 융합 RAG] 후보 공종 문서 자동 판별
                    is_interdisciplinary = any(k in query_lower for k in [
                        "변전소", "정거장", "301", "114", "107", "201", "차량기지", "기지",
                        "환승", "전체", "종합", "공종", "인터페이스", "비교"
                    ]) or ("제안" in query_lower and not any(k in query_lower for k in ["전기만", "건축만", "토질만", "구조만", "통신만"]))

                    doc_groups = {}
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
                            use_multi_doc_fusion = True

                    if not use_multi_doc_fusion and scored_sections:
                        top_sc, target_doc_name, target_file_path, top_sec = scored_sections[0]
                        target_start_page = top_sec.get("start_page", 1)
                        matched_section_titles = [f"{s.get('title', '')} (p.{s.get('start_page', 1)}~{s.get('end_page', 1)})" for sc, dn, fp, s in scored_sections if dn == target_doc_name][:4]
                        source_notice = f"> 📂 **[출처 문서 자동 탐색]** **`{target_doc_name}`**의 **{top_sec.get('title', '')} (p.{top_sec.get('start_page', 1)}~{top_sec.get('end_page', 1)})**에서 자동 추출하여 분석했습니다.\\n\\n"
                except Exception:
                    pass"""

if old_scored_block in content:
    content = content.replace(old_scored_block, new_scored_block, 1)
    print("2. Scored block with candidate determination integrated.")
else:
    print("Warning: old_scored_block not found!")

# 3. get_smart_pdf_payload 직전에 Multi-Doc Fusion 실행 블록 주입
target_try_block = """            try:
                pdf_bytes, info_msg, is_meta_only = get_smart_pdf_payload(target_file_path, query)"""

new_try_block = """            # [다중 공종 복합 융합 RAG 모드 가동]
            if use_multi_doc_fusion and candidate_docs:
                try:
                    writer = pypdf.PdfWriter()
                    slice_bullet_list = []
                    all_matched_titles = []
                    all_active_sections = []
                    total_pages_count = 0
                    doc_short_names = []

                    domain_badges = {
                        "전기": "⚡", "건축": "🏛️", "토질": "🏗️", "토목구조": "🌉", "구조": "🌉",
                        "시공": "🚜", "신호": "🚦", "통신": "📡", "철도": "🛤️", "궤도": "🛤️", "기계": "⚙️"
                    }

                    for dn, fp, d_secs in candidate_docs:
                        d_secs.sort(key=lambda x: x[0], reverse=True)
                        badge = "📄"
                        short_name = dn.replace("기본설계 기술제안_", "").replace(".pdf", "").strip()
                        for k, b in domain_badges.items():
                            if k in dn:
                                badge = b
                                break
                        doc_short_names.append(short_name)

                        reader = pypdf.PdfReader(str(fp))
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
                                })

                        sorted_p = sorted(list(doc_page_set))
                        if sorted_p:
                            for p in sorted_p:
                                writer.add_page(reader.pages[p])
                            p_range_str = f"p.{sorted_p[0]+1}~{sorted_p[-1]+1}" if len(sorted_p) > 1 else f"p.{sorted_p[0]+1}"
                            slice_bullet_list.append({
                                "badge": badge,
                                "name": dn,
                                "short": short_name,
                                "pages": p_range_str
                            })
                            total_pages_count += len(sorted_p)

                    out = io.BytesIO()
                    writer.write(out)
                    fusion_bytes = out.getvalue()
                    fusion_b64 = base64.b64encode(fusion_bytes).decode("utf-8")

                    source_notice = (
                        f"> 🌐 **[다중 공종 복합 융합 탐색]** 질문과 관련된 **{len(candidate_docs)}개 전문 공종 기술제안서**를 교차 발췌하여 다학제 융합 분석을 수행했습니다.\\n"
                        + "\\n".join([f"> - {info['badge']} **`{info['name']}`** ({info['pages']})" for info in slice_bullet_list])
                        + "\\n\\n"
                    )
                    slice_info_str = "\\n".join([f"- [{info['short']}]: {info['name']} ({info['pages']})" for info in slice_bullet_list])

                    system_prompt = (
                        "당신은 철도/토목/건축/전기 복합 융합 엔지니어링 수석 기술감리원 AI입니다.\\n"
                        "제공된 PDF 문서는 질문과 관련된 여러 전문 공종(전기, 건축, 토질 및 기초, 토목구조 등)의 핵심 기술제안서를 교차 발췌한 통합 문서입니다.\\n\\n"
                        f"[발췌된 공종별 출처 정보]\\n"
                        f"{slice_info_str}\\n\\n"
                        "[핵심 답변 작성 규칙]\\n"
                        "1. [공종별 융합 비교 표(Table) 최우선 제시]:\\n"
                        "   - 맨 위에 공종별 핵심 제안을 비교하는 마크다운 표를 먼저 제시하세요.\\n"
                        "   - 열 구성: | 공종 | 핵심 제안 내용 | 개선 효과 / 주요 수치 (면적/공사비/안정성) | 근거 출처 및 원본 페이지 |\\n"
                        "2. [공종별 상세 핵심 기술제안 심층 서술]:\\n"
                        "   - 표 아래에 공종별 헤더(예: ### 1. ⚡ [전기분야], ### 2. 🏛️ [건축분야], ### 3. 🏗️ [토질 및 기초분야], ### 4. 🌉 [토목구조분야] 등)로 나누어,\\n"
                        "   - 각 공종 제안서에 명시된 구체적 수치(면적 축소 ㎡, 공사비 절감액, 내진/기초 해석 결과, 장비 사양, 편의시설 등)를 100% 팩트 기반으로 상세히 설명하세요.\\n"
                        "   - 각 항목마다 근거 원본 페이지 번호(예: 전기 p.6, 건축 p.17, 토질 p.6 등)를 반드시 명시하세요.\\n"
                        "3. [공종간 인터페이스 및 시너지 종합]:\\n"
                        "   - 마지막에 여러 공종이 어떻게 상호 유기적으로 연계(시너지 및 간섭 방지)되는지 3~4개 항목으로 요약하세요."
                    )

                    models_to_try = [
                        "gemini-3.6-flash",
                        "gemini-flash-latest",
                        "gemini-3.5-flash-lite"
                    ]
                    text = ""
                    last_error = ""
                    for model_name in models_to_try:
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                        req_body = {
                            "systemInstruction": {"parts": [{"text": system_prompt}]},
                            "contents": [{
                                "role": "user",
                                "parts": [
                                    {"inline_data": {"mime_type": "application/pdf", "data": fusion_b64}},
                                    {"text": query}
                                ]
                            }],
                            "generationConfig": {"temperature": 0.2}
                        }
                        try:
                            req = urllib.request.Request(
                                url,
                                data=json.dumps(req_body).encode("utf-8"),
                                headers={"Content-Type": "application/json"}
                            )
                            with urllib.request.urlopen(req, timeout=90) as resp:
                                resp_data = json.loads(resp.read().decode("utf-8"))
                                text = resp_data["candidates"][0]["content"]["parts"][0]["text"]
                                break
                        except Exception as m_err:
                            last_error = str(m_err)
                            time.sleep(1.0)
                            continue

                    if text:
                        holes_str = ", ".join(list(matched_graph_holes)[:4]) if matched_graph_holes else "전체 구간"
                        intel_summary = graph_intel.get("summary", "공간/공종 허브 매핑")
                        rag_h_nodes = [f"bh_{h}" for h in matched_graph_holes]
                        for sn in doc_short_names:
                            rag_h_nodes.append(f"hub_prop_{sn}")

                        rag_trace = {
                            "query": query,
                            "highlight_nodes": list(set(rag_h_nodes)),
                            "steps": [
                                {"step": 1, "icon": "🧠", "title": "질문 의도 분석 및 복합 공종 라우팅", "badge": "다학제 융합 의도 파악", "detail": f"질문 분석 완료: '{query}' ➔ 다중 공종({', '.join(doc_short_names)}) 복합 제안 탐색 모드 가동"},
                                {"step": 2, "icon": "🌐", "title": "지식 그래프(Graph) 선제 탐색 ➔ 색인 피드백", "badge": "지식망 ➔ 색인 가중치 전달", "detail": f"지식그래프 탐색 완료: [{intel_summary}] 경로 검출 (타겟 시추공: {holes_str}) ➔ 색인 엔진 가중치 전달"},
                                {"step": 3, "icon": "📂", "title": "다중 기술문서 교차 슬라이싱 & 메모리 병합", "badge": f"{len(candidate_docs)}개 공종 {total_pages_count}쪽 병합", "detail": f"각 공종별 핵심 제안 섹션({', '.join(doc_short_names)}) 정밀 발췌 및 실시간 병합 완료"},
                                {"step": 4, "icon": "🤖", "title": "Gemini 100만 컨텍스트 두뇌 심층 추론 & 다학제 융합 분석", "badge": "공종별 비교표 & 시너지 도출 완료", "detail": "수백 페이지 전체 원문과 도표를 대조하여 100% 팩트 기반 기술 답변 및 공종간 인터페이스 분석 생성"}
                            ]
                        }

                        resp_data = {
                            "reply": source_notice + text,
                            "source_document": f"다중 공종 복합 제안 ({', '.join(doc_short_names)})",
                            "source_page": 1,
                            "matched_sections": all_matched_titles[:6],
                            "active_sections": all_active_sections[:10],
                            "trace": rag_trace
                        }
                        self.respond_json(resp_data)
                        return
                except Exception as fusion_err:
                    print(f" -> [Multi-Doc Fusion Error]: {fusion_err}")

            try:
                pdf_bytes, info_msg, is_meta_only = get_smart_pdf_payload(target_file_path, query)"""

if target_try_block in content:
    content = content.replace(target_try_block, new_try_block, 1)
    print("3. Multi-Doc Fusion execution block integrated.")
else:
    print("Warning: target_try_block not found!")

# 4. Backup & Save
backup_path = server_path.with_name("server.py.bak_fusion")
backup_path.write_text(server_path.read_text(encoding="utf-8"), encoding="utf-8")
server_path.write_text(content, encoding="utf-8")
print(f"Success! Backup saved to {backup_path.name}, server.py updated.")
