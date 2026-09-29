import os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from google import genai
import gemini_file_manager

sys.stdout.reconfigure(encoding='utf-8')

env_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\.env")
api_key = ""
for line in env_file.read_text(encoding="utf-8").splitlines():
    if line.startswith("GEMINI_API_KEY="):
        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")

client = genai.Client(api_key=api_key)
doc_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\documents\입찰안내서(동탄트램).pdf")
file_ref = gemini_file_manager.get_or_upload_file(client, doc_path)

prompt = """당신은 철도/토목/지반 엔지니어링 및 입찰안내서 분석 전문 AI입니다.
입찰안내서상 계약상 핵심 리스크를 분석하여:
1. [핵심 요약 표(Table)]: 항목, 주요 리스크 내용, 근거 페이지(p.XX), 실무 대응방안
2. [두괄식 핵심 포인트]: 3~5개 불렛포인트 요약
형식으로 신속하고 명확하게 답변하세요."""

print("Starting test with gemini-3.6-flash...", flush=True)
t0 = time.time()
resp = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=[file_ref, "입찰안내서상 계약상 리스크를 분석해줘"],
    config=genai.types.GenerateContentConfig(
        system_instruction=prompt,
        temperature=0.1
    )
)
elapsed = time.time() - t0
print(f"gemini-3.6-flash SUCCESS in {elapsed:.2f}s!", flush=True)
print(f"Length: {len(resp.text)} chars", flush=True)
print("--- PREVIEW ---", flush=True)
print(resp.text[:800], flush=True)
