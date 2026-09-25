import os
from pathlib import Path
from google import genai

api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    env_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\.env")
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("GEMINI_API_KEY="):
                api_key = line.split("=", 1)[1].strip()

client = genai.Client(api_key=api_key)
file_ref = client.files.get(name="files/rpfjfbyylm31")
print("Remote file:", file_ref.name, file_ref.state.name)

test_models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-lite"]
for m in test_models:
    try:
        print(f"\nTesting model: {m}...")
        resp = client.models.generate_content(
            model=m,
            contents=[file_ref, "87페이지 표 4.4.1에 나오는 NGB-1과 NGB-2의 지층과 N치를 알려줘."]
        )
        print(f"SUCCESS with {m}!")
        print("Reply preview:", resp.text[:300] if resp.text else "No text")
        break
    except Exception as e:
        print(f"FAILED with {m}:", e)
