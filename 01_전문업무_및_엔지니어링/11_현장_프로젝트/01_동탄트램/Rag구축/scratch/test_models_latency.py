import os, sys, time
from pathlib import Path
from google import genai

sys.stdout.reconfigure(encoding='utf-8')

env_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\.env")
api_key = ""
if env_file.exists():
    for line in env_file.read_text(encoding='utf-8').splitlines():
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip().strip('"').strip("'")

if not api_key:
    api_key = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=api_key)

models = ["gemini-3.8-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-flash-latest", "gemini-2.0-flash", "gemini-2.5-flash"]

for m in models:
    t0 = time.time()
    try:
        resp = client.models.generate_content(
            model=m,
            contents="test",
        )
        print(f"Model {m}: SUCCESS ({time.time()-t0:.2f}s)")
    except Exception as e:
        print(f"Model {m}: FAILED ({time.time()-t0:.2f}s) -> {str(e)[:100]}")
