import re
from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

print(f"Original server.py length: {len(content)} chars")

# 1. get_smart_pdf_payload 수정
# 기존 15쪽 가위질 코드 교체
old_slice_block = """    if not doc_meta and file_size_mb > 15.0:
        indices = list(range(15))
        return slice_pdf_pages(file_path, indices), f"[안내] 20MB 초과 전체 문서 중 주요 15쪽만 로드되었습니다.", False"""

new_slice_block = """    if file_size_mb > 20.0 and not sections:
        # 20MB 초과 대형 스캔 문서는 15쪽으로 자르지 않고 Google File API 통업로드로 처리
        return None, f"[Google File API 롱컨텍스트] {file_path.name} 전체({round(file_size_mb, 1)}MB) 전수 탐색 모드", False"""

if old_slice_block in content:
    content = content.replace(old_slice_block, new_slice_block)
    print("Replaced 15-page slicing with Google File API flag!")
else:
    # regex replace if encoding or whitespace differed
    content = re.sub(
        r'if not doc_meta and file_size_mb > 15\.0:.*?return slice_pdf_pages\(file_path, indices\)[^\n]+, False',
        new_slice_block,
        content,
        flags=re.DOTALL
    )
    print("Replaced slicing via regex pattern!")

# 2. /api/chat 에서 pdf_bytes is None (대형 파일) 일 때 Google File API 분기 추가
old_b64_call = """                pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")"""

new_b64_call = """                # 20MB 초과 대형 파일(또는 None)인 경우 Google File API Long-Context 모드 가동
                if pdf_bytes is None:
                    try:
                        from google import genai
                        import gemini_file_manager
                        
                        client = genai.Client(api_key=api_key)
                        file_ref = gemini_file_manager.get_or_upload_file(client, file_path)
                        
                        system_prompt = (
                            "당신은 철도/토목/지반 엔지니어링 및 설계보고서, 시추주상도 분석 전문 AI입니다.\\n"
                            "제공된 대용량 PDF 문서 전체(수백 페이지)를 면밀히 분석하여 질문에 100% 팩트 기반으로 답변하세요.\\n\\n"
                            "[핵심 규칙]\\n"
                            "1. 반드시 해당 내용이 수록된 '정확한 원본 페이지 번호(예: p.87 등)'를 명시하세요.\\n"
                            "2. 지층, 심도, N치, 토질 특성 등 표(Table) 데이터는 마크다운 표로 깔끔하게 정리하세요.\\n"
                            "3. 제안설계 NGB 시추공, 기본설계 GB/NH/DT 시추공 등의 구분을 명확히 설명하세요.\\n"
                            "4. 추측하지 말고 문서에 명시된 사실만을 정확히 인용하세요."
                        )
                        
                        models_to_try = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash"]
                        text = ""
                        for m_name in models_to_try:
                            try:
                                resp = client.models.generate_content(
                                    model=m_name,
                                    contents=[file_ref, query],
                                    config=genai.types.GenerateContentConfig(
                                        system_instruction=system_prompt,
                                        temperature=0.1
                                    )
                                )
                                if resp and resp.text:
                                    text = resp.text.strip()
                                    break
                            except Exception as m_err:
                                last_error = str(m_err)
                                continue
                                
                        if not text:
                            self.respond_json({"error": f"Google File API 분석 실패: {last_error}"}, 500)
                            return
                            
                        self.respond_json({
                            "reply": text,
                            "source_document": target_doc_name,
                            "source_page": target_start_page or 1,
                            "matched_sections": matched_section_titles
                        })
                        return
                    except Exception as file_api_err:
                        self.respond_json({"error": f"Google File API 오류: {str(file_api_err)}"}, 500)
                        return

                pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")"""

if old_b64_call in content:
    content = content.replace(old_b64_call, new_b64_call)
    print("Integrated Google File API handling into /api/chat!")
else:
    print("Could not find old_b64_call, checking...")

server_path.write_text(content, encoding="utf-8")
print(f"Server.py updated successfully! New length: {len(content)} chars")
