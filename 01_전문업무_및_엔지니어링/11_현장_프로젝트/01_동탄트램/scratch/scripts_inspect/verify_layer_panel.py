import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('class="layer-panel"')
if idx != -1:
    panel_text = text[idx:idx+1100]
    print("=== UPDATED LAYER PANEL HTML ===")
    print(panel_text)

    print("\nVerification Checks:")
    print("  '정거장 번호':", "정거장 번호" in panel_text)
    print("  '교차로 구간선' (clean):", "교차로 구간선</label>" in panel_text or "교차로 구간선\n" in panel_text or "교차로 구간선 <" in panel_text)
    print("  '교차로명 라벨' (clean):", "교차로명 라벨</label>" in panel_text or "교차로명 라벨\n" in panel_text or "교차로명 라벨 <" in panel_text)
    print("  '(노선 오버레이)' removed:", "(노선 오버레이)" not in panel_text)
    print("  '(구간연장)' removed:", "(구간연장)" not in panel_text)
