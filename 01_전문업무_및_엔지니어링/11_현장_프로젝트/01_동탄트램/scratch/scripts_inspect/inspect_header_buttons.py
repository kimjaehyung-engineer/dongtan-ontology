import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<header')
if idx != -1:
    end_idx = text.find('</header>', idx)
    print("=== HEADER HTML ===")
    print(text[idx:end_idx+10])

# Search for buttons or elements with absolute positioning or flex layout in header
print("\n=== Header / Toggle Button CSS ===")
matches = re.findall(r'(\.[a-zA-Z0-9_\-]*btn[^{]*?\{[^}]*?\})', text)
for m in matches[:10]:
    print(" ", m)
