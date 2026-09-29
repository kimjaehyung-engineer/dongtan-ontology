import sys, os, urllib.request, json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

env_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\.env")
api_key = ""
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
with urllib.request.urlopen(url, timeout=10) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    for m in data.get("models", []):
        methods = m.get("supportedGenerationMethods", [])
        if "generateContent" in methods:
            name = m["name"].replace("models/", "")
            disp = m.get("displayName", "")
            limit = m.get("inputTokenLimit", 0)
            print(f"{name:32s} | {disp:30s} | {limit}")
