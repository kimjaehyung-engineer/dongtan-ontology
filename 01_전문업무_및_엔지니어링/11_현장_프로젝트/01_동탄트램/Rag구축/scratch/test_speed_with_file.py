import os, sys, time
from pathlib import Path
from google import genai
sys.path.insert(0, str(Path(__file__).parent.parent))
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

models = ["gemini-flash-latest", "gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-2.5-flash"]

for m in models:
    t0 = time.time()
    try:
        resp = client.models.generate_content(
            model=m,
            contents=[file_ref, "입찰안내서의 핵심 계약 리스크 3가지를 표로 아주 간단히 요약해줘."],
        )
        print(f"Model {m}: SUCCESS in {time.time()-t0:.2f}s | chars: {len(resp.text)}")
    except Exception as e:
        print(f"Model {m}: FAILED in {time.time()-t0:.2f}s -> {e}")
