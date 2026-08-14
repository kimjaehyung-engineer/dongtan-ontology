import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print("HTML size:", len(text))

# Check for renderConstructionSections snippet
idx = text.find('function renderConstructionSections()')
if idx != -1:
    block = text[idx:idx+1200]
    print("Contains <line> in renderConstructionSections:", "createElementNS" in block and "line" in block)
    print("\n=== renderConstructionSections SNIPPET ===")
    print(block[:600])

# Check for selectConstructionSection snippet
idx2 = text.find('function selectConstructionSection(')
if idx2 != -1:
    block2 = text[idx2:idx2+1200]
    print("Contains <line> in selectConstructionSection:", "createElementNS" in block2 and "line" in block2)
    print("\n=== selectConstructionSection SNIPPET ===")
    print(block2[:600])
