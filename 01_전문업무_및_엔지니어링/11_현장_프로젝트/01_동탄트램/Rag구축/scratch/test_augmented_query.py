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

system_prompt = """당신은 철도/토목/지반 엔지니어링 및 입찰안내서 분석 전문 AI입니다.
제공된 대용량 PDF 문서를 분석하여 질문에 100% 팩트 기반으로 명확하고 신속하게 답변하세요.

[핵심 답변 규칙 (가독성 & 속도 최적화)]
1. [정확한 원본 페이지 번호 명시]: 모든 주요 사실과 조항마다 수록된 '정확한 원본 페이지 번호(예: p.87, p.142 등)'를 반드시 명시하세요.
2. [핵심 요약 표(Table) 우선 제시]: 장황한 줄글 대신, 핵심 내용(항목, 주요 조항/리스크 내용, 근거 페이지, 실무 대응방안)을 마크다운 표로 먼저 일목요연하게 정리하세요.
3. [두괄식 글머리 기호 서술]: 표 아래에 주요 핵심 포인트를 3~5개 항목의 간결한 글머리 기호(Bullet points)로 요약하세요. 불필요하게 긴 서술은 지양하고 핵심만 압축하세요.
4. [팩트 기반]: 추측하지 말고 문서에 명시된 사실만을 정확히 인용하세요."""

query = "입찰안내서상 계약상 리스크\n\n[참고 지침: 원본 문서의 제3편 계약특수조건(p.142~198) 관련 내용을 우선적으로 집중 검토하세요.]"

print("Querying with gemini-flash-latest...", flush=True)
t0 = time.time()
resp = client.models.generate_content(
    model="gemini-flash-latest",
    contents=[file_ref, query],
    config=genai.types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.1
    )
)
elapsed = time.time() - t0
print(f"\n[RESULT] Finished in {elapsed:.2f} seconds!", flush=True)
print(f"Reply Length: {len(resp.text)} chars", flush=True)
print("\n--- CONTENT ---\n", flush=True)
print(resp.text, flush=True)
