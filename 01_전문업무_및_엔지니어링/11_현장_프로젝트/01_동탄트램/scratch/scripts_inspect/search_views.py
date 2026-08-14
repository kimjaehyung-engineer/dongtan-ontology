import sys
sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(f_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'container-resource-view', text)]
print(f"Occurrences of 'container-resource-view': {len(matches)}")
for idx in matches:
    print("--- MATCH AT ---")
    print(text[max(0, idx-100):min(len(text), idx+200)])
