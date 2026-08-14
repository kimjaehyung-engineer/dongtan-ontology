import sys
sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'station', text, re.IGNORECASE)]
print(f"Total 'station' references: {len(matches)}")

# Search for select station event listener or function
for m in re.finditer(r'select.*stn|stn.*select|station.*select|select.*station|node', text, re.IGNORECASE):
    idx = m.start()
    snippet = text[max(0, idx-100):min(len(text), idx+200)]
    if 'option' in snippet or 'change' in snippet or 'nodes' in snippet:
        print("--- MATCH ---")
        print(snippet)
        print("="*40)
