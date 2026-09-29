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

query = "동탄역 핵심이슈는 머지?"
t0 = time.time()
try:
    resp = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        contents=[file_ref, f"당신은 엔지니어링 전문가입니다. 다음 질문에 대해 문서에 기반하여 한국어로 요약 답변하세요:\n질문: {query}"],
    )
    print(f"SUCCESS ({time.time()-t0:.2f}s):\n{resp.text}", flush=True)
except Exception as e:
    print(f"ERR ({time.time()-t0:.2f}s): {e}", flush=True)
