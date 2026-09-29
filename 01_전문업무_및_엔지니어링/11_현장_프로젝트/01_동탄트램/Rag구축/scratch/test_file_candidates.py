import sys, os, time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
rag_dir = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
sys.path.insert(0, str(rag_dir))

from google import genai
import gemini_file_manager

env_file = rag_dir / ".env"
api_key = ""
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()

client = genai.Client(api_key=api_key)

root = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\Rag구축\01_SOURCE_DOCUMENTS")
fp = root / "02_기본설계_기술제안" / "기본설계 기술제안_ 신호.pdf"
file_ref = gemini_file_manager.get_or_upload_file(client, fp)

# Test candidate models for File API
candidates = [
    "gemini-3-flash-preview",
    "gemini-3.1-flash-lite-preview",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-3.8-flash",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemma-4-26b-a4b-it"
]

for m in candidates:
    t0 = time.time()
    try:
        resp = client.models.generate_content(
            model=m,
            contents=[file_ref, "Hello, reply OK"],
        )
        print(f"[{m}] SUCCESS ({time.time()-t0:.2f}s): {resp.text[:30]}", flush=True)
    except Exception as e:
        err = str(e)
        if "503" in err:
            print(f"[{m}] 503 High Demand ({time.time()-t0:.2f}s)", flush=True)
        elif "429" in err:
            print(f"[{m}] 429 Quota/Rate Limit ({time.time()-t0:.2f}s)", flush=True)
        elif "404" in err:
            print(f"[{m}] 404 Not Found ({time.time()-t0:.2f}s)", flush=True)
        else:
            print(f"[{m}] ERR ({time.time()-t0:.2f}s): {err[:80]}", flush=True)
