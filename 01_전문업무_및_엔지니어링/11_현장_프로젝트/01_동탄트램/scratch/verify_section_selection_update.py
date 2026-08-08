import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print("HTML size:", len(text))

idx = text.find('function selectConstructionSection(')
if idx != -1:
    block = text[idx:idx+1500]
    print("Contains matchedIntersections:", "matchedIntersections" in block)
    print("Contains openIntersectionDrawer:", "openIntersectionDrawer" in block)
    print("Contains drawer-active-card:", "drawer-active-card" in block)
    print("\n=== selectConstructionSection SNIPPET ===")
    print(block[:800])
