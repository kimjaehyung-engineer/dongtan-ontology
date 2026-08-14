import sys
import os
import glob
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Target V1 HTML file:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

# Verify SVG path IDs in HTML
for p in ["pBN", "pBS", "pRW", "pRE"]:
    print(f"Path #{p} present in HTML:", f'id="{p}"' in content)
