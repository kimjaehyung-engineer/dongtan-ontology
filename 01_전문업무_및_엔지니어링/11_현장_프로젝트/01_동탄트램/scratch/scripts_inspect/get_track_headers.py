# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

html_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\동탄트램_업무_매뉴얼v1.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 3장 궤도 챕터 내의 h3 태그들을 찾음
track_start = content.find('id="sec-track"')
arch_start = content.find('id="sec-architecture"')

track_html = content[track_start:arch_start]

print("=== H3 headers in sec-track ===")
h3_matches = re.findall(r'<h3[^>]*>(.*?)</h3>', track_html, re.DOTALL)
for h3 in h3_matches:
    print(h3.strip())
