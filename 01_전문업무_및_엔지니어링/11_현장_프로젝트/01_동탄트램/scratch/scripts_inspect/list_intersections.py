import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const intersectionData = (\[[\s\S]*?\]);', text)
if m:
    data = json.loads(m.group(1))
    print(f"Total intersections found: {len(data)}")
    for i, item in enumerate(data):
        print(f"#{i+1}: [{item.get('tool')}] #{item.get('no')} - {item.get('name')} (STA {item.get('startSta')}~{item.get('endSta')})")
else:
    print("Could not find intersectionData pattern!")
