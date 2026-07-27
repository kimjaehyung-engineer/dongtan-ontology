import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_master_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

cleaned_count = 0

print(f"Scanning ALL HTML files in '{target_master_dir}' to completely purge exam history / question sections...")

for root, dirs, files in os.walk(target_master_dir):
    for f in files:
        if f.endswith('.html'):
            f_path = os.path.join(root, f)
            with open(f_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            orig_content = content
            
            # Remove any section or table containing 기출문제, 출제 이력, 자격시험
            content = re.sub(r'<h[1-6][^>]*>.*?(?:관련 기출문제|출제 이력|자격시험|117~138회).*?</h[1-6]>\s*(?:<div[^>]*>.*?</div>|<table[^>]*>.*?</table>|\s*)*', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<div[^>]*>.*?기술사 자격시험 연계 출제 이력.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<table[^>]*>.*?출제 문제 원문.*?</table>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<h[1-6][^>]*>.*?(?:기출문제|출제 이력|자격시험).*?</h[1-6]>', '', content, flags=re.IGNORECASE)

            if content != orig_content:
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                cleaned_count += 1
                print(f"Purged exam section from: {os.path.relpath(f_path, target_master_dir)}")

print(f"\n🎉 Completely purged exam / question sections from total {cleaned_count} HTML files in master directory!")
