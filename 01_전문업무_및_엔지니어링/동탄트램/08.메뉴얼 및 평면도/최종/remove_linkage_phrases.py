import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_attach_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

cleaned_files = 0

for root, dirs, files in os.walk(base_attach_dir):
    for f in files:
        if f.endswith(('.html', '.htm')):
            file_path = os.path.join(root, f)
            with open(file_path, 'r', encoding='utf-8') as h_file:
                content = h_file.read()
                
            original = content
            
            # 1. Replace [동탄트램 업무 매뉴얼 v1 연계] and similar in box headers
            content = re.sub(r'\[동탄트램 업무 매뉴얼 v1 연계\]\s*', '', content)
            content = re.sub(r'\[동탄트램 매뉴얼 v1\]\s*', '', content)
            content = re.sub(r'\[설계사 작성\]\s*', '', content)
            content = re.sub(r'분야별 설계기준 검토서 연계 규격', '분야별 상세 기술 설계기준', content)
            content = re.sub(r'첨부서류 연계 상세 설계기준', '상세 기술 설계기준', content)
            
            # Clean header titles in manual-v1-integration-box
            content = re.sub(r'<h4([^>]*)>\s*<span>📖</span>\s*분야별 핵심 기술', r'<h4\1><span>📖</span> 분야별 핵심 기술', content)
            
            # Remove any trailing "연계" in section titles if awkward
            content = content.replace('기술기준 연계', '기술기준')
            content = content.replace('설계기준 연계', '설계기준')
            
            if content != original:
                with open(file_path, 'w', encoding='utf-8') as h_file:
                    h_file.write(content)
                cleaned_files += 1

print(f"Cleaned meta phrases from {cleaned_files} HTML files!")
