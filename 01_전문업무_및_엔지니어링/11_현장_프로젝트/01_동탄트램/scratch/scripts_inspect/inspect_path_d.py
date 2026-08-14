import sys
import os
import glob
import re

sys.stdout.reconfigure(encoding='utf-8')

search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]

with open(file_v1, 'r', encoding='utf-8') as f:
    v1 = f.read()

# Search for SVG path d attributes
for path_id in ['pBN', 'pBS', 'pRW', 'pRE']:
    m = re.search(r'id="' + path_id + r'"[^>]*d="([^"]+)"', v1)
    if m:
        print(f"Path [{path_id}] d attribute:")
        print(" ", m.group(1))
    else:
        # Check if d attribute is set via JS
        print(f"Path [{path_id}] not having inline d attribute, checking JS...")
        for line in v1.splitlines():
            if path_id in line and ('setAttribute("d"' in line or 'd=' in line or 'M ' in line):
                print(" ", line.strip()[:140])
