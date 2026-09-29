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

# Test 1: gemini-flash-latest with focused page hint
print("Test 1: gemini-flash-latest with page hint p.142~198...", flush=True)
t0 = time.time()
resp = client.models.generate_content(
    model="gemini-flash-latest",
    contents=[file_ref, "입찰안내서 제3편 계약특수조건(p.142~198)을 중점 분석하여 핵심 계약 리스크 3~5가지를 표로 요약해줘."],
    config=genai.types.GenerateContentConfig(temperature=0.1)
)
print(f"gemini-flash-latest finished in {time.time()-t0:.2f}s! Chars: {len(resp.text)}", flush=True)

# Test 2: gemini-2.5-flash with page hint p.142~198
print("\nTest 2: gemini-2.5-flash with page hint p.142~198...", flush=True)
t0 = time.time()
resp = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[file_ref, "입찰안내서 제3편 계약특수조건(p.142~198)을 중점 분석하여 핵심 계약 리스크 3~5가지를 표로 요약해줘."],
    config=genai.types.GenerateContentConfig(temperature=0.1)
)
print(f"gemini-2.5-flash finished in {time.time()-t0:.2f}s! Chars: {len(resp.text)}", flush=True)
