# -*- coding: utf-8 -*-
import sys, json, os, io, urllib.request, base64
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
import pypdf

# 1. Load API Key
env_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\.env")
api_key = ""
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if "GEMINI_API_KEY" in line:
            api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
if not api_key:
    api_key = os.getenv("GEMINI_API_KEY", "")

root = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\Rag구축\01_SOURCE_DOCUMENTS")

targets = [
    ("전기", "기본설계 기술제안_ 전기.pdf", [5, 6]), # 0-indexed: p.6~7
    ("건축", "기본설계 기술제안_ 건축.pdf", [13, 14, 15, 16, 17]), # p.14~18
    ("토질 및 기초", "기본설계 기술제안_ 토질 및 기초.pdf", [5, 6]), # p.6~7
    ("토목구조", "기본설계 기술제안_ 토목구조.pdf", [8, 9, 13]), # p.9~10, p.14
]

writer = pypdf.PdfWriter()
slice_info = []
for domain, fname, pages in targets:
    matches = list(root.rglob(fname))
    if matches:
        fpath = matches[0]
        reader = pypdf.PdfReader(str(fpath))
        page_names = f"p.{pages[0]+1}~{pages[-1]+1}" if len(pages) > 1 else f"p.{pages[0]+1}"
        slice_info.append(f"- [{domain}]: {fname} ({page_names})")
        for p in pages:
            if p < len(reader.pages):
                writer.add_page(reader.pages[p])

out = io.BytesIO()
writer.write(out)
pdf_bytes = out.getvalue()
pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")
print(f"Combined PDF size: {len(pdf_bytes)/1024:.1f} KB, Total pages: {len(writer.pages)}")
print("Slice info:")
for si in slice_info:
    print(" ", si)

query = "301정거장 변전소에 대한 제안사항을 물어봣어. 전기, 건축, 토질/기초, 구조 등 전 공종의 제안사항을 비교 정리해줘."

slice_info_str = "\n".join(slice_info)
system_prompt = (
    "당신은 철도/토목/건축/전기 복합 융합 엔지니어링 수석 기술감리원 AI입니다.\n"
    "제공된 PDF 문서는 301정거장 및 변전소와 관련된 여러 전문 공종(전기, 건축, 토질 및 기초, 토목구조 등)의 핵심 기술제안서를 교차 발췌한 통합 문서입니다.\n\n"
    f"[발췌된 공종별 출처 정보]\n"
    f"{slice_info_str}\n\n"
    "[핵심 답변 작성 규칙]\n"
    "1. [공종별 융합 비교 표(Table) 최우선 제시]:\n"
    "   - 맨 위에 공종([전기], [건축], [토질 및 기초], [토목구조])별 핵심 제안을 비교하는 마크다운 표를 먼저 제시하세요.\n"
    "   - 열 구성: | 공종 | 핵심 제안 내용 | 개선 효과 / 주요 수치 (면적/공사비/안정성) | 근거 출처 및 원본 페이지 |\n"
    "2. [공종별 상세 핵심 기술제안 심층 서술]:\n"
    "   - 표 아래에 공종별 헤더(예: ### 1. ⚡ [전기분야], ### 2. 🏛️ [건축분야], ### 3. 🏗️ [토질 및 기초분야], ### 4. 🌉 [토목구조분야])로 나누어,\n"
    "   - 각 공종 제안서에 명시된 구체적 수치(예: 변전소 면적 축소 ㎡, 공사비 절감 억 원, 내진/기초 해석 결과, 승무원 편의시설 등)를 100% 팩트 기반으로 상세히 설명하세요.\n"
    "   - 각 항목마다 근거 원본 페이지 번호(예: 전기 p.6, 건축 p.17, 토질 p.6 등)를 반드시 명시하세요.\n"
    "3. [공종간 인터페이스 및 시너지 종합]:\n"
    "   - 마지막에 여러 공종이 변전소 및 301정거장 구축 시 어떻게 유기적으로 연계(시너지 및 간섭 방지)되는지 3~4개 글머리 기호로 요약하세요."
)

models_to_try = [
    "gemini-3.6-flash",
    "gemini-flash-latest"
]

for model_name in models_to_try:
    print(f"\nTrying model: {model_name}...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    req_body = {
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "application/pdf",
                            "data": pdf_b64
                        }
                    },
                    {"text": query}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2
        }
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(req_body).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=90) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
            text = resp_data["candidates"][0]["content"]["parts"][0]["text"]
            print("\n=== GEMINI RESPONSE ===")
            print(text)
            break
    except Exception as e:
        print(f"Error with {model_name}: {e}")
