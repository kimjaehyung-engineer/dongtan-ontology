import sys, os, urllib.request, json, time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
rag_dir = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
env_file = rag_dir / ".env"
api_key = ""
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()

# List all models
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
with urllib.request.urlopen(url, timeout=10) as resp:
    data = json.loads(resp.read().decode("utf-8"))

models = [m["name"].replace("models/", "") for m in data.get("models", []) if "generateContent" in m.get("supportedGenerationMethods", [])]

working_models = []
for m in models:
    if any(skip in m for skip in ["tts", "image", "transcribe", "clip", "robotics", "computer-use"]):
        continue
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
    req_body = {
        "contents": [{"role": "user", "parts": [{"text": "Say OK"}]}]
    }
    t0 = time.time()
    try:
        req = urllib.request.Request(url, data=json.dumps(req_body).encode("utf-8"), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            ans = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            print(f"[{m}] SUCCESS ({time.time()-t0:.2f}s): {ans[:30]}")
            working_models.append(m)
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="ignore")
        print(f"[{m}] HTTP {e.code} ({time.time()-t0:.2f}s)")
    except Exception as e:
        print(f"[{m}] ERR ({time.time()-t0:.2f}s): {e}")

print("\n--- ALL WORKING MODELS RIGHT NOW ---")
print(working_models)
