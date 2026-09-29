import os, sys
from pathlib import Path
from google import genai

sys.stdout.reconfigure(encoding='utf-8')
env_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\.env")
api_key = ""
for line in env_file.read_text(encoding="utf-8").splitlines():
    if line.startswith("GEMINI_API_KEY="):
        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")

client = genai.Client(api_key=api_key)

print("=== Available Google GenAI Models ===")
for m in client.models.list():
    name = m.name
    if "gemini" in name.lower():
        print(name)
