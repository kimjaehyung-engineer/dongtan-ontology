import os, sys

sys.stdout.reconfigure(encoding='utf-8')

search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'

keywords = [
    '03_기술제안 1공구',
    '03_기술제안 2공구',
    '06_기술제안 1공구',
    '06_기술제안 2공구',
    '공기산출',
    'Activity List'
]

print("=== Search Target Excel & Data Files ===")
found_files = []
for root, dirs, files in os.walk(search_dir):
    for f in files:
        if any(k in f for k in ['기술제안', '공기산출', 'Activity']) and not f.startswith('~$'):
            fp = os.path.join(root, f)
            found_files.append(fp)
            print(f"- {f}\n  Path: {fp}")
