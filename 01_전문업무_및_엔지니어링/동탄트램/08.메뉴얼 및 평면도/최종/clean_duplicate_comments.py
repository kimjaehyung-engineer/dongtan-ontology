import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

print(f"Cleaning duplicate comments in Standard HTML files...")

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html') and '표준서' in f:
            f_path = os.path.join(root, f)
            with open(f_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Clean duplicate HTML comments
            cleaned_content = re.sub(r'(\s*<!-- 화성시 및 5대 위탁.*?-->\s*)+', '\n    <!-- 동탄트램 위수탁 지장물 5대 관종별 정량적 공학 기술 시방 기준 -->\n    ', content)

            if cleaned_content != content:
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(cleaned_content)

print("🎉 Successfully cleaned duplicate HTML comments!")
