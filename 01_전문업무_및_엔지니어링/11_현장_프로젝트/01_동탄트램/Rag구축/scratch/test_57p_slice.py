import os, sys, time, fitz, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from google import genai

sys.stdout.reconfigure(encoding='utf-8')

env_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\.env")
api_key = ""
for line in env_file.read_text(encoding="utf-8").splitlines():
    if line.startswith("GEMINI_API_KEY="):
        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")

client = genai.Client(api_key=api_key)
doc_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\documents\입찰안내서(동탄트램).pdf")

# Slice p.142~198 (57 pages)
print("Slicing p.142~198 from 입찰안내서...", flush=True)
doc = fitz.open(str(doc_path))
new_doc = fitz.open()
for p in range(141, 198):
    new_doc.insert_pdf(doc, from_page=p, to_page=p)

sliced_bytes = new_doc.tobytes(deflate=True)
print(f"Sliced bytes: {len(sliced_bytes)} bytes ({len(sliced_bytes)/(1024):.1f} KB)", flush=True)

# Test with gemini-3.6-flash and gemini-3.5-flash-lite
prompt = """당신은 철도/토목/지반 엔지니어링 및 입찰안내서 분석 전문 AI입니다.
제공된 PDF 문서는 입찰안내서 제3장 공사계약특수조건(p.142~198) 발췌본입니다.
계약상 핵심 리스크를 분석하여:
1. [핵심 요약 표(Table)]: 항목, 주요 리스크 내용, 근거 페이지(p.XX), 실무 대응방안
2. [두괄식 핵심 포인트]: 3~5개 불렛포인트 요약
형식으로 신속하고 명확하게 답변하세요."""

for m in ["gemini-3.6-flash", "gemini-3.5-flash-lite"]:
    print(f"\nTesting {m} with 57-page slice...", flush=True)
    t0 = time.time()
    try:
        resp = client.models.generate_content(
            model=m,
            contents=[
                genai.types.Part.from_bytes(data=sliced_bytes, mime_type="application/pdf"),
                "입찰안내서상 계약상 리스크를 분석해줘"
            ],
            config=genai.types.GenerateContentConfig(
                system_instruction=prompt,
                temperature=0.1
            )
        )
        elapsed = time.time() - t0
        print(f"SUCCESS with {m} in {elapsed:.2f}s! Chars: {len(resp.text)}", flush=True)
        print("--- PREVIEW ---", flush=True)
        print(resp.text[:600], flush=True)
        break
    except Exception as e:
        print(f"FAILED with {m} in {time.time()-t0:.2f}s: {e}", flush=True)
