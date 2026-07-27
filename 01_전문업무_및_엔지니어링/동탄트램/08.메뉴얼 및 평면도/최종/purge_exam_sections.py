import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

cleaned_file_count = 0

print(f"Scanning HTML files in '{target_dir}' to purge all exam / question history sections...")

for root, dirs, files in os.walk(target_dir):
    for f in files:
        if f.endswith('.html'):
            f_path = os.path.join(root, f)
            with open(f_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            orig_content = content
            
            # Pattern 1: Delete entire h2/h4 section of 기출문제 and its following table / div / container
            content = re.sub(r'<h[24][^>]*>.*?(?:관련 기출문제|출제 이력|자격시험).*?</h[24]>\s*(?:<div[^>]*>.*?</div>|<table[^>]*>.*?</table>|\s*)*', '', content, flags=re.DOTALL | re.IGNORECASE)

            # Pattern 2: Remove any leftover div or block with '기출문제' or '출제 이력' or '117~138회'
            content = re.sub(r'<div[^>]*class="[^"]*key-takeaway[^"]*"[^>]*>.*?117~138회.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<div[^>]*>.*?기술사 자격시험 연계 출제 이력.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<table[^>]*>.*?출제 문제 원문.*?</table>', '', content, flags=re.DOTALL | re.IGNORECASE)
            
            # Pattern 3: Remove lingering <h2> or <h4> headers mentioning 기출문제 or 출제 이력
            content = re.sub(r'<h[24][^>]*>.*?(?:기출문제|출제 이력|자격시험).*?</h[24]>', '', content, flags=re.IGNORECASE)

            if content != orig_content:
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                cleaned_file_count += 1
                print(f"Cleaned exam sections from: {os.path.basename(f_path)}")

print(f"\n🎉 Cleaned exam/question sections from total {cleaned_file_count} HTML files!")
