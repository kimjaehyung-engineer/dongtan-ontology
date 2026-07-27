import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_master_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

keywords = ["기출문제", "출제 이력", "출제이력", "자격시험", "117~138회"]
found_files = []

for root, dirs, files in os.walk(target_master_dir):
    for f in files:
        if f.endswith('.html'):
            f_path = os.path.join(root, f)
            with open(f_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            for kw in keywords:
                if kw in content:
                    found_files.append((f_path, kw))

if not found_files:
    print("✅ PERFECT! Zero exam/question keywords found across ALL HTML files in the manual!")
else:
    print(f"⚠️ Found {len(found_files)} instances of exam keywords:")
    for fp, kw in found_files[:10]:
        print(f" - File: {os.path.basename(fp)} | Keyword: '{kw}'")
