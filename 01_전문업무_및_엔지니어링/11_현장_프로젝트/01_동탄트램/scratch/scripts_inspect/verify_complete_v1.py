import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function selectConstructionSection(')
if idx != -1:
    end_idx = text.find('function ', idx + 10)
    func_text = text[idx:end_idx]
    print(f"selectConstructionSection function length: {len(func_text)}")
    print("Contains drawer-active-card:", "drawer-active-card" in func_text)
    print("Contains matchedIntersections:", "matchedIntersections" in func_text)
    print("Contains openIntersectionDrawer:", "openIntersectionDrawer" in func_text)
    print("\nEnd of function snippet:")
    print(func_text[-400:])
