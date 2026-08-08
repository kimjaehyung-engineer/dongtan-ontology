import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function renderConstructionSections()')
if idx != -1:
    end_idx = text.find('function ', idx + 10)
    print("=== renderConstructionSections SNIPPET ===")
    print(text[idx:end_idx][:1000])

idx2 = text.find('function selectConstructionSection(')
if idx2 != -1:
    end_idx2 = text.find('function ', idx2 + 10)
    print("\n=== selectConstructionSection SNIPPET ===")
    print(text[idx2:end_idx2][:1000])
