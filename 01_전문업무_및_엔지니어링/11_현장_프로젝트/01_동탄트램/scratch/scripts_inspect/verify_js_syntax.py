import sys
import subprocess
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

scripts = re.findall(r'<script[\s\S]*?>([\s\S]*?)</script>', content)
print(f"Total script blocks found: {len(scripts)}")

temp_js = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\temp_check.js'

for idx, s in enumerate(scripts):
    with open(temp_js, 'w', encoding='utf-8') as f_js:
        f_js.write(s)
    res = subprocess.run(['node', '-c', temp_js], capture_output=True, text=True, encoding='utf-8')
    if res.returncode == 0:
        print(f"Script block #{idx+1}: JS Syntax VALID (PASSED)")
    else:
        print(f"Script block #{idx+1}: JS Syntax ERROR:")
        print(res.stderr)

