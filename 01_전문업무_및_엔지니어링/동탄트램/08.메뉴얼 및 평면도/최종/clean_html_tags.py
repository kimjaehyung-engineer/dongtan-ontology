import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file1 = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설\3_지장물 이설 요청 (위수탁고)\표준서\지장물 이설 요청 (위수탁고)_표준서.html"
file2 = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설\4_도급자분 이설업체 선정(상_하수)\표준서\도급자분 이설업체 선정(상_하수)_표준서.html"

for f_path in [file1, file2]:
    if os.path.exists(f_path):
        with open(f_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove any lingering flow-step or empty insight blocks
        content = re.sub(r'<div class="flow-step">.*?</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="insight-title">.*?</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<p style="margin: 0 0 12px 0; font-size: 0.95rem; color: #92400e; font-weight: bold;">\s*</p>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div class="insight-box">\s*</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'^\s*</div>\s*$', '', content, flags=re.MULTILINE)

        with open(f_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Cleaned {os.path.basename(f_path)}")
