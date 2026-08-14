import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    text = f.read()

matches = [m.start() for m in re.finditer(r'intersection-zoom-modal', text)]
print("Matches for 'intersection-zoom-modal':", len(matches))
for idx in matches:
    print(text[max(0, idx-100):min(len(text), idx+300)])
    print("-" * 50)
