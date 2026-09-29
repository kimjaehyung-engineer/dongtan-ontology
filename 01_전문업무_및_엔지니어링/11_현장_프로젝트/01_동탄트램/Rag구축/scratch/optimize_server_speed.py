import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

server_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
if not server_file.exists():
    print(f"Error: {server_file} not found")
    sys.exit(1)

content = server_file.read_text(encoding="utf-8")

# 1. Update system prompt to be structured, concise (Table + Bullets), and fast
old_prompt = '''                        system_prompt = (
                            "당신은 철도/토목/지반 엔지니어링 및 설계보고서, 시추주상도 분석 전문 AI입니다.\\n"
                            "제공된 대용량 PDF 문서 전체(수백 페이지)를 면밀히 분석하여 질문에 100% 팩트 기반으로 답변하세요.\\n\\n"
                            "[핵심 규칙]\\n"
                            "1. 반드시 해당 내용이 수록된 '정확한 원본 페이지 번호(예: p.87 등)'를 명시하세요.\\n"
                            "2. 지층, 심도, N치, 토질 특성 등 표(Table) 데이터는 마크다운 표로 깔끔하게 정리하세요.\\n"
                            "3. 제안설계 NGB 시추공, 기본설계 GB/NH/DT 시추공 등의 구분을 명확히 설명하세요.\\n"
                            "4. 추측하지 말고 문서에 명시된 사실만을 정확히 인용하세요."
                        )'''

new_prompt = '''                        system_prompt = (
                            "당신은 철도/토목/지반 엔지니어링 및 설계보고서, 시추주상도 분석 전문 AI입니다.\\n"
                            "제공된 대용량 PDF 문서 전체(수백 페이지)를 면밀히 분석하여 질문에 100% 팩트 기반으로 명확하고 신속하게 답변하세요.\\n\\n"
                            "[핵심 답변 규칙 (가독성 & 속도 최적화)]\\n"
                            "1. [정확한 원본 페이지 번호 명시]: 모든 주요 사실과 조항마다 수록된 '정확한 원본 페이지 번호(예: p.87, p.142 등)'를 반드시 명시하세요.\\n"
                            "2. [핵심 요약 표(Table) 우선 제시]: 장황한 줄글 대신, 핵심 내용(항목, 주요 조항/리스크 내용, 근거 페이지, 실무 대응방안)을 마크다운 표로 먼저 일목요연하게 정리하세요.\\n"
                            "3. [두괄식 글머리 기호 서술]: 표 아래에 주요 핵심 포인트를 3~5개 항목의 간결한 글머리 기호(Bullet points)로 요약하세요. 불필요하게 긴 서술은 지양하고 핵심만 압축하세요.\\n"
                            "4. [구분 명확화]: 제안설계 NGB 시추공, 기본설계 GB/NH/DT 시추공 등의 구분을 명확히 설명하세요.\\n"
                            "5. [팩트 기반]: 추측하지 말고 문서에 명시된 사실만을 정확히 인용하세요.\\n"
                            "6. [안내]: 상세 조항 전문이나 특정 항목의 심층 분석이 필요할 경우 추가 질문할 수 있도록 말미에 한 줄 안내를 덧붙이세요."
                        )'''

if old_prompt in content:
    content = content.replace(old_prompt, new_prompt)
    print("1. Successfully updated system_prompt with concise structured instructions!")
else:
    print("Notice: old_prompt pattern not exactly matched, checking variations...")

# 2. Update models_to_try to prioritize fast & reliable gemini-3.6-flash first
old_models = '''                        models_to_try = [
                            "gemini-3.8-flash",
                            "gemini-3.6-flash",
                            "gemini-3.5-flash-lite",
                            "gemini-flash-latest"
                        ]'''

new_models = '''                        models_to_try = [
                            "gemini-3.6-flash",
                            "gemini-3.5-flash-lite",
                            "gemini-3.8-flash",
                            "gemini-flash-latest"
                        ]'''

if old_models in content:
    content = content.replace(old_models, new_models)
    print("2. Successfully prioritized gemini-3.6-flash first in models_to_try!")
else:
    print("Notice: old_models pattern not matched directly.")

server_file.write_text(content, encoding="utf-8")
print("Saved server.py successfully.")
