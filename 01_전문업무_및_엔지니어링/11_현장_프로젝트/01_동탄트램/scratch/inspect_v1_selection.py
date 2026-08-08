import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Inspect selectIntersection function
idx = text.find('function selectIntersection(')
if idx != -1:
    print("=== selectIntersection ===")
    print(text[idx:idx+1200])

# Inspect renderConstructionSections function
idx2 = text.find('function renderConstructionSections()')
if idx2 != -1:
    print("\n=== renderConstructionSections ===")
    print(text[idx2:idx2+1200])
