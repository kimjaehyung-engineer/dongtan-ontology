import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Find all occurrences of .light-theme
positions = [m.start() for m in re.finditer(r'\.light-theme', text)]
print(f"Found {len(positions)} occurrences of '.light-theme'")
for p in positions:
    ctx = text[max(0,p-30):p+100]
    print(f"  Position {p}: ...{ctx}...")
