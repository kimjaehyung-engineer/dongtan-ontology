import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Search for id="drawer-..."
matches = re.finditer(r'id="(drawer-[^"]*)"', text)
for m in matches:
    print("Found ID:", m.group(1))

# Check selectIntersection to see how active card ID is referenced
idx = text.find('function selectIntersection(')
if idx != -1:
    print("\n=== selectIntersection drawer card reference ===")
    m_card = re.search(r'document\.getElementById\("([^"]*)"\)', text[idx:idx+1500])
    if m_card:
        print("Active card ID referenced:", m_card.group(1))
    print(text[idx+500:idx+1200])
