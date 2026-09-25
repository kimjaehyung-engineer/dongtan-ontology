import json
import os
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

env_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\.env"
api_key = ""
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()

test_cases = [
    {
        "desc": "1. 기술제안서 4대 과제 질의",
        "query": "4대 제안과제의 주요 핵심 내용과 공학적 차별화 전략을 알려줘",
        "expected_doc": "기술제안_4편 토질 및 기초(97~116).pdf"
    },
    {
        "desc": "2. 차량기지 시추공 GB-1 질의",
        "query": "차량기지 시추공 GB-1의 지하수위와 암반심도를 요약해줘",
        "expected_doc": "기본설계 시추주상도(1공구)_45공.pdf"
    },
    {
        "desc": "3. 2공구 본선 시추공 DT-5 질의",
        "query": "2공구 시추공 DT-5의 표준관입시험 N치와 토질 구성을 알려줘",
        "expected_doc": "기본설계 시추주상도(2공구)_27공.pdf"
    },
    {
        "desc": "4. S01 변전소 가시설 질의",
        "query": "S01 변전소 가시설 흙막이벽체의 구조계산 안전율을 알려줘",
        "expected_doc": "#3편 증빙자료_토질 및 기초.pdf"
    },
    {
        "desc": "5. 차량기지 비탈면 사면안정 질의",
        "query": "차량기지 깎기 비탈면의 사면안정 검토 결과를 알려줘",
        "expected_doc": "토질_차량기지 비탈면 안정성 검토-rev01_260630.pdf"
    }
]

print("=== 5개 기술문서 대상 자동 라우팅 전수 검증 시작 ===")
all_pass = True

for tc in test_cases:
    print(f"\n[{tc['desc']}]")
    print(f"질문: {tc['query']}")
    payload = {"api_key": api_key, "query": tc["query"]}
    req = urllib.request.Request(
        "http://127.0.0.1:8080/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            routed_doc = data.get("source_document")
            page = data.get("source_page")
            sections = data.get("matched_sections", [])
            print(f"  ➔ 응답 상태: {resp.status} OK")
            print(f"  ➔ 자동 매칭된 문서: {routed_doc}")
            print(f"  ➔ 시작 페이지: p.{page}")
            print(f"  ➔ 매칭 섹션: {sections[:2]}")
            if routed_doc == tc["expected_doc"]:
                print("  ✅ 라우팅 일치 (PASS)")
            else:
                print(f"  ❌ 라우팅 불일치 (FAIL): 예상={tc['expected_doc']}, 실제={routed_doc}")
                all_pass = False
    except Exception as e:
        print(f"  ❌ 오류 발생: {e}")
        all_pass = False

print("\n==========================================")
if all_pass:
    print("🎉 축하합니다! 5개 문서 전수 자동 라우팅 검증 100% 통과 (ALL PASS)!")
else:
    print("⚠️ 일부 문서 라우팅 검증 실패")
