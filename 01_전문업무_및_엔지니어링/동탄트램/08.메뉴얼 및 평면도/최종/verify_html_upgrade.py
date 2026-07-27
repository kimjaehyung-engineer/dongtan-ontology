import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설\3_지장물 이설 요청 (위수탁고)\표준서\지장물 이설 요청 (위수탁고)_표준서.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=== Verification of Upgraded Standard HTML File ===")
print("File Size:", len(content), "bytes")
print("Contains SVG Box:", "<svg" in content)
print("Contains Dogeub/Witak Table:", "table-dogeub-witak" in content)
print("Contains Mindmap Box:", "insight-box" in content)
print("Contains 8 Major Pipeline Types:", all(k in content for k in ["상수관", "하수관", "오수관로", "도시가스관", "지역난방관", "통신관로", "특고압 전력관", "광역상수관"]))
