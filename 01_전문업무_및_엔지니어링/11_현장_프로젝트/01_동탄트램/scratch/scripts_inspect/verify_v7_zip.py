import os, zipfile, sys

sys.stdout.reconfigure(encoding='utf-8')

zip_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼 BODY (집행단계)v7.zip'

with zipfile.ZipFile(zip_path, 'r') as z:
    file_list = z.namelist()
    print(f"Total entries in ZIP: {len(file_list)}")
    print("=== First 10 entries in ZIP ===")
    for f in file_list[:10]:
        print("  -", f)
