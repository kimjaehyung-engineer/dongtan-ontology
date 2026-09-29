import sys, os, urllib.request, json, time, base64
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
import server

query = "동탄역 핵심이슈는 머지?"

# Let's inspect what query_sections_with_bonus or routing produces
print("Testing routing for query:", query)
# Let's see what target_doc_name, target_file_path, and pdf_bytes are selected!
scored = server.query_sections_with_bonus(query)
print(f"Scored sections count: {len(scored)}")
if scored:
    for s in scored[:5]:
        print(f"  Score: {s[0]} | Doc: {s[1]} | Title: {s[3].get('title')} (p.{s[3].get('start_page')}~{s[3].get('end_page')})")
    
    target_score, target_doc_name, target_file_path, best_section = scored[0]
    print(f"\nTop Target: {target_doc_name} at {target_file_path}")
    
    pdf_bytes, info_msg, is_meta_only = server.get_smart_pdf_payload(target_file_path, query)
    print(f"Payload info_msg: {info_msg}")
    print(f"is_meta_only: {is_meta_only}")
    if pdf_bytes:
        print(f"pdf_bytes size: {len(pdf_bytes)} bytes ({len(pdf_bytes)/1024/1024:.2f} MB)")
        pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")
        
        # Test each model in models_to_try
        env_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\.env")
        api_key = ""
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("GEMINI_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()

        models_to_try = [
            "gemini-3.6-flash",
            "gemini-3.5-flash-lite",
            "gemini-flash-latest"
        ]

        system_prompt = (
            "당신은 토목/건축/기계 엔지니어링 현장 기술 시방서 및 설계보고서 전문 감리원/수석 엔지니어 AI입니다.\n"
            "제공된 PDF 문서는 전체 원본 문서에서 질문과 관련된 핵심 섹션을 정밀 추출한 발췌본입니다.\n"
            f"[문서 발췌 정보 & 도메인 지식]\n"
            f"- 추출된 원본 범위: {info_msg}\n"
            "[핵심 답변 규칙]\n"
            "1. 원본 페이지 번호 명시\n"
            "2. 표 우선 제시\n"
            "3. 글머리 기호 요약\n"
            "4. 팩트 기반"
        )

        for m_name in models_to_try:
            print(f"\n---> Testing model: {m_name}")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m_name}:generateContent?key={api_key}"
            req_body = {
                "systemInstruction": {"parts": [{"text": system_prompt}]},
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"inline_data": {"mime_type": "application/pdf", "data": pdf_b64}},
                            {"text": query}
                        ]
                    }
                ],
                "generationConfig": {"temperature": 0.2}
            }
            t0 = time.time()
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(req_body).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=90) as resp:
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    ans = resp_data["candidates"][0]["content"]["parts"][0]["text"]
                    print(f"SUCCESS in {time.time()-t0:.2f}s! Ans preview:\n{ans[:200]}")
                    break
            except urllib.error.HTTPError as e:
                err = e.read().decode("utf-8", errors="ignore")
                print(f"HTTPError {e.code} in {time.time()-t0:.2f}s: {err}")
            except Exception as e:
                print(f"Exception in {time.time()-t0:.2f}s: {e}")
    else:
        print("pdf_bytes is None (Large file mode)")
