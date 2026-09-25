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

test_models = ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-flash-latest"]
for m in test_models:
    try:
        print(f"\nTesting model: {m}...")
        resp = client.models.generate_content(
            model=m,
            contents=[file_ref, "87페이지 표 4.4.1에 나오는 NGB-1과 NGB-2의 지층과 N치를 정확히 마크다운 표로 알려줘."]
        )
        print(f"SUCCESS with {m}!")
        with open("scratch/model_36_success.txt", "w", encoding="utf-8") as f:
            f.write(resp.text)
        print("Reply preview:")
        print(resp.text[:300].encode("utf-8", errors="replace").decode("utf-8"))
        break
    except Exception as e:
        print(f"FAILED with {m}:", e)
