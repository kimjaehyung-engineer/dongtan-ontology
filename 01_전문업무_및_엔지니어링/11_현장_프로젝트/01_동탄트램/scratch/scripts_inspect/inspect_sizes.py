import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

file_v1 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램_노선평면도V1.html'
file_main = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램_노선평면도.html'

def inspect_file(path, label):
    print(f"=== {label} ===")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for r attribute setting in JS
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if 'setAttribute("r"' in line or "setAttribute('r'" in line or 'stroke-width' in line or 'station-marker' in line:
            print(f"Line {i+1}: {line.strip()[:140]}")

inspect_file(file_v1, "V1 HTML")
inspect_file(file_main, "Main HTML")
