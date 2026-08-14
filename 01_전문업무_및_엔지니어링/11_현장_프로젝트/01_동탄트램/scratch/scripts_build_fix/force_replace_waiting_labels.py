import os
import re

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램"
html_manual = os.path.join(base_dir, "08.메뉴얼 및 평면도", "동탄트램_업무_매뉴얼.html")
html_standalone = os.path.join(base_dir, "08.메뉴얼 및 평면도", "동탄도시철도_시스템_실시간_시뮬레이터.html")

default_overviews = {
    "normal": "⚡ 전력·무선통신·광백본망·관제센터·현장신호가 유기적으로 맞물려 무사고 열차 자동운행을 보증하는 표준 계통 루프입니다.",
    "emergency": "🚨 승객 비상벨 작동 시 LTE-R 무선을 거쳐 관제센터가 전선 전력을 끊고(0V) 신호등을 적색으로 즉각 쇄정하는 방호 루프입니다.",
    "switch": "🔀 CTC 회차 명령에 따라 충돌 위험 검증 후 선로전환기가 레일을 대피선으로 꺾고 황색 주의 신호를 켜는 경로 전환 루프입니다.",
    "poweroff": "🔋 전차선 급전이 중단되더라도 트램 지붕의 대용량 배터리를 방전하여 다음역까지 안전하게 대피(Coasting)하는 구동 루프입니다."
}

# ─────────────────────────────────────────────────────────────────────────────
# 1. 매뉴얼 (동탄트램_업무_매뉴얼.html) 수정
# ─────────────────────────────────────────────────────────────────────────────
with open(html_manual, 'r', encoding='utf-8') as f:
    manual = f.read()

# 정규식을 이용해 id="sys-flow-desc-모드" 영역의 내부를 강제로 대기텍스트로 치환합니다.
# 공백이나 줄바꿈에 구애받지 않도록 꼼꼼하게 매칭합니다.
for mode, desc in default_overviews.items():
    pattern = rf'(<div\s+id="sys-flow-desc-{mode}"[^>]*>)([\s\S]*?)(</div>)'
    
    def replacer(match):
        # div 태그 부분은 유지하고 내부 텍스트만 쉬운 핵심 개요 설명으로 대체
        # 들여쓰기도 보기 좋게 맞춰 줍니다.
        return f'{match.group(1)}\n                                {desc}\n                            {match.group(3)}'
        
    manual = re.sub(pattern, replacer, manual)

with open(html_manual, 'w', encoding='utf-8') as f:
    f.write(manual)


# ─────────────────────────────────────────────────────────────────────────────
# 2. 독립 시뮬레이터 (동탄도시철도_시스템_실시간_시뮬레이터.html) 수정
# ─────────────────────────────────────────────────────────────────────────────
with open(html_standalone, 'r', encoding='utf-8') as f:
    standalone = f.read()

for mode, desc in default_overviews.items():
    pattern = rf'(<div\s+id="flow-desc-{mode}"[^>]*>)([\s\S]*?)(</div>)'
    
    def replacer_s(match):
        return f'{match.group(1)}\n                {desc}\n            {match.group(3)}'
        
    standalone = re.sub(pattern, replacer_s, standalone)

with open(html_standalone, 'w', encoding='utf-8') as f:
    f.write(standalone)

print("정규식(re.sub) 기반 강제 치환 작업 완료.")
