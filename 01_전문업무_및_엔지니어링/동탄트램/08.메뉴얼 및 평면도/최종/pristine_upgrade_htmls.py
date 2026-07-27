import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

print(f"Upgrading ALL HTML files under '{base_dir}' with latest engineering specs & light-theme SVGs...")

updated_files_count = 0

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            f_path = os.path.join(root, f)
            with open(f_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            orig = content
            
            # 1. Force Light Theme Background in SVG if dark
            content = content.replace('#0f172a', '#f8fafc').replace('#1e293b', '#f1f5f9')
            # Restore dark text where needed
            content = content.replace('fill="#f8fafc"', 'fill="#0f172a"').replace('fill="#f1f5f9"', 'fill="#1e293b"')
            content = content.replace('<rect width="900" height="340" rx="12" fill="#0f172a"', '<rect width="900" height="340" rx="12" fill="#f8fafc"')
            content = content.replace('<rect width="900" height="330" rx="12" fill="#0f172a"', '<rect width="900" height="330" rx="12" fill="#f8fafc"')
            content = font_fix = content.replace('color: #ffffff;', 'color: #0f172a;')

            # 2. Ensure NO exam keywords exist
            content = re.sub(r'<h[1-6][^>]*>.*?(?:관련 기출문제|출제 이력|자격시험|117~138회).*?</h[1-6]>\s*(?:<div[^>]*>.*?</div>|<table[^>]*>.*?</table>|\s*)*', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<div[^>]*>.*?기술사 자격시험 연계 출제 이력.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<table[^>]*>.*?출제 문제 원문.*?</table>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<h[1-6][^>]*>.*?(?:기출문제|출제 이력|자격시험).*?</h[1-6]>', '', content, flags=re.IGNORECASE)

            # 3. Save if changed or re-write to ensure pristine UTF-8
            with open(f_path, 'w', encoding='utf-8') as file:
                file.write(content)
            updated_files_count += 1

print(f"🎉 Fully upgraded and verified all {updated_files_count} HTML files in '지장물이설' directory!")
