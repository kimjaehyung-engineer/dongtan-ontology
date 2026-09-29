import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

# 1. Update threshold to 1.5MB
old_thresh = """    # 3MB 초과 시 REST API 인라인 전송 시 503(High Demand/용량초과) 에러가 발생하므로 Google File API 모드로 직결 전환!
    if len(sliced_bytes) > 3 * 1024 * 1024:
        info_str = f"[Google File API 롱컨텍스트] {', '.join(matched_sections[:6])} 등 총 {len(sorted_pages)}p({round(len(sliced_bytes)/(1024*1024), 1)}MB) 전수 탐색 모드"
        return None, info_str, False"""

new_thresh = """    # 1.5MB 초과 시 REST API 인라인 base64 전송 시 503(High Demand/용량초과) 에러가 발생하므로 Google File API 모드로 직결 전환!
    if len(sliced_bytes) > 1.5 * 1024 * 1024:
        info_str = f"[Google File API 롱컨텍스트] {', '.join(matched_sections[:6])} 등 총 {len(sorted_pages)}p({round(len(sliced_bytes)/(1024*1024), 1)}MB) 전수 탐색 모드"
        return None, info_str, False"""

if old_thresh in content:
    content = content.replace(old_thresh, new_thresh, 1)
    print("1. Updated sliced_bytes threshold to 1.5MB!")
else:
    print("1. Warning: old_thresh not found!")

# 2. Extract system_prompt as an explicit variable before models_to_try loop
old_loop_start = """                pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")

                models_to_try = [
                    "gemini-3.6-flash",
                    "gemini-3.5-flash-lite",
                    "gemini-3.8-flash",
                    "gemini-flash-latest"
                ]
                last_error = ""
                text = ""

                for model_name in models_to_try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                    req_body = {
                        "systemInstruction": {
                            "parts": [{
                                "text": (
                                    "당신은 토목/건축/기계 엔지니어링 현장 기술 시방서 및 설계보고서 전문 감리원/수석 엔지니어 AI입니다.\\n"
                                    "제공된 PDF 문서는 전체 원본 문서에서 질문과 관련된 핵심 섹션을 정밀 추출한 발췌본입니다.\\n"
                                    f"[문서 발췌 정보 & 도메인 지식]\\n"
                                    f"- 추출된 원본 범위: {info_msg}\\n"
                                    "- 시추공 약어 기준: GB = 차량기지 시추공, NH = 1공구 본선 시추공, DT = 2공구 본선 시추공.\\n"
                                    "- 주상도 서식에 '차량기지'라는 한글 단어 대신 공번 'GB'로 표기되어 있으므로 GB 공번을 차량기지 조사 결과로 정확히 인식하여 분석하세요.\\n"
                                    "- 답변 시 발췌본 내부의 임의 페이지가 아닌, 위 [추출된 원본 범위]에 기재된 '원본 페이지 번호(예: p.40, p.44 등)'를 기준으로 인용하여 명시하세요.\\n"
                                    "[핵심 답변 규칙 (가독성 & 속도 최적화)]\\n"
                                    "1. [정확한 원본 페이지 번호 명시]: 모든 주요 사실과 조항마다 수록된 '정확한 원본 페이지 번호(예: p.87, p.142 등)'를 반드시 명시하세요.\\n"
                                    "2. [핵심 요약 표(Table) 우선 제시]: 장황한 줄글 대신, 핵심 내용(항목, 주요 조항/리스크 내용, 근거 페이지, 실무 대응방안)을 마크다운 표로 먼저 일목요연하게 정리하세요.\\n"
                                    "3. [두괄식 글머리 기호 서술]: 표 아래에 주요 핵심 포인트를 3~5개 항목의 간결한 글머리 기호(Bullet points)로 요약하세요. 불필요하게 긴 서술은 지양하고 핵심만 압축하세요.\\n"
                                    "4. [팩트 기반]: 추측하지 말고 문서에 명시된 사실만을 정확히 인용하세요."
                                )
                            }]
                        },"""

new_loop_start = """                pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")

                system_prompt = (
                    "당신은 토목/건축/기계 엔지니어링 현장 기술 시방서 및 설계보고서 전문 감리원/수석 엔지니어 AI입니다.\\n"
                    "제공된 PDF 문서는 전체 원본 문서에서 질문과 관련된 핵심 섹션을 정밀 추출한 발췌본입니다.\\n"
                    f"[문서 발췌 정보 & 도메인 지식]\\n"
                    f"- 추출된 원본 범위: {info_msg}\\n"
                    "- 시추공 약어 기준: GB = 차량기지 시추공, NH = 1공구 본선 시추공, DT = 2공구 본선 시추공.\\n"
                    "- 주상도 서식에 '차량기지'라는 한글 단어 대신 공번 'GB'로 표기되어 있으므로 GB 공번을 차량기지 조사 결과로 정확히 인식하여 분석하세요.\\n"
                    "- 답변 시 발췌본 내부의 임의 페이지가 아닌, 위 [추출된 원본 범위]에 기재된 '원본 페이지 번호(예: p.40, p.44 등)'를 기준으로 인용하여 명시하세요.\\n"
                    "[핵심 답변 규칙 (가독성 & 속도 최적화)]\\n"
                    "1. [정확한 원본 페이지 번호 명시]: 모든 주요 사실과 조항마다 수록된 '정확한 원본 페이지 번호(예: p.87, p.142 등)'를 반드시 명시하세요.\\n"
                    "2. [핵심 요약 표(Table) 우선 제시]: 장황한 줄글 대신, 핵심 내용(항목, 주요 조항/리스크 내용, 근거 페이지, 실무 대응방안)을 마크다운 표로 먼저 일목요연하게 정리하세요.\\n"
                    "3. [두괄식 글머리 기호 서술]: 표 아래에 주요 핵심 포인트를 3~5개 항목의 간결한 글머리 기호(Bullet points)로 요약하세요. 불필요하게 긴 서술은 지양하고 핵심만 압축하세요.\\n"
                    "4. [팩트 기반]: 추측하지 말고 문서에 명시된 사실만을 정확히 인용하세요."
                )

                models_to_try = [
                    "gemini-3.6-flash",
                    "gemini-3.5-flash-lite",
                    "gemini-3.8-flash",
                    "gemini-flash-latest"
                ]
                last_error = ""
                text = ""

                for model_name in models_to_try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                    req_body = {
                        "systemInstruction": {
                            "parts": [{"text": system_prompt}]
                        },"""

if old_loop_start in content:
    content = content.replace(old_loop_start, new_loop_start, 1)
    print("2. Defined system_prompt explicitly before loop!")
else:
    print("2. Warning: old_loop_start not found!")

# 3. In the File API Fallback (line 4000+), provide fallback system prompt if needed:
server_path.write_text(content, encoding="utf-8")
print("Saved server.py changes successfully!")
