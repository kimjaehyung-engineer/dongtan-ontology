import os

tc_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp'

print("=== Checking package.json / vite in time-chainage-mvp ===")
pkg_path = os.path.join(tc_root, 'package.json')
if os.path.exists(pkg_path):
    print("✓ Found package.json:")
    with open(pkg_path, 'r', encoding='utf-8') as f:
        print(f.read())
else:
    print("!! package.json NOT found in time-chainage-mvp")
