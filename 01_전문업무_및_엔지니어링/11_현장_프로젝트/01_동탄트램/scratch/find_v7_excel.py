import os

search_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'

matches = []
for root, dirs, files in os.walk(search_root):
    for f in files:
        if '매뉴얼' in f and ('BODY' in f or '집행' in f) and f.endswith(('.xlsm', '.xlsx')):
            matches.append(os.path.join(root, f))
        elif 'v7' in f.lower() and f.endswith(('.xlsm', '.xlsx')):
            matches.append(os.path.join(root, f))

print("=== Found Excel Files ===")
for m in matches:
    print(m)
