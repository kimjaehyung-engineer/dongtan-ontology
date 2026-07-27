import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

print("Checking directories for Act 3 and Act 4:")
for item in os.listdir(base_dir):
    full_path = os.path.join(base_dir, item)
    if os.path.isdir(full_path):
        if "요청" in item or "이설업체" in item or "3_" in item or "4_" in item:
            print(f" 📂 Folder: {item}")
            for sub in os.listdir(full_path):
                sub_p = os.path.join(full_path, sub)
                if os.path.isdir(sub_p):
                    print(f"    └─ Sub: {sub} | files: {os.listdir(sub_p)}")
