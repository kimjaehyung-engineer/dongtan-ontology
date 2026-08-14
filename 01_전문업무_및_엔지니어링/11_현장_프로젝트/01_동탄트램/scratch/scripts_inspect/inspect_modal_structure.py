import sys
import os
import glob
import re

sys.stdout.reconfigure(encoding='utf-8')

# Target V1 HTML file
search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Target V1 HTML file for modal integration:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

print("File size:", len(content))
print("Modal structure present:", "id=\"zoomModal\"" in content or "modal" in content)
