import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'

for r, d, files in os.walk(root):
    for f in files:
        if f.endswith('.html'):
            print(os.path.join(r, f))
