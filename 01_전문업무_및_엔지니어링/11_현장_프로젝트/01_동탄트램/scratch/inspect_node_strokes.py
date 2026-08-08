import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Check for references to circle stroke reset or station-marker styles
matches = re.findall(r'.*station-marker.*', text)
for m in matches[:10]:
    print(m)

# Find stroke attribute resets in Javascript
stroke_resets = re.findall(r'.*setAttribute\("stroke".*', text)
for s in stroke_resets[:15]:
    print(s)
