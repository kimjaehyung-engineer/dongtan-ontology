import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

f_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설\11_민원 저감 대책 수립\표준서\민원 저감 대책 수립_표준서.html"

with open(f_path, 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('<text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ 실시간 계측</text>', '<text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② 소음·진동 제어</text>', 1)

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Perfect Box 2 title fix applied!")
