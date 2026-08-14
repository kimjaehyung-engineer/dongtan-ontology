import os, sys

sys.stdout.reconfigure(encoding='utf-8')

search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'

print("=== Search Folder and Files ===")
for root, dirs, files in os.walk(search_dir):
    for d in dirs:
        if '매뉴얼BODY(집행단계-첨부폴더)' in d:
            print("Folder Found:", os.path.join(root, d))
    for f in files:
        if '매뉴얼 BODY (집행단계)v7.xlsm' in f and not f.startswith('~$'):
            print("Excel File Found:", os.path.join(root, f))
