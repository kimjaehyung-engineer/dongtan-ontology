import sys
sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(f_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<div id="container-resource-view"[\s\S]*?</div>\s*</div>', text)
print("Matches found for container-resource-view:", len(matches))

idx = text.find('id="container-resource-view"')
if idx != -1:
    print(text[max(0, idx-300):min(len(text), idx+600)])
