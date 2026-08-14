import os, sys

tc_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp'

print("=== Checking time-chainage-mvp directory ===")
if os.path.exists(tc_dir):
    for root, dirs, files in os.walk(tc_dir):
        rel = os.path.relpath(root, tc_dir)
        print(f"Directory: {rel}")
        for f in files[:10]:
            print(f"  - {f}")
else:
    print("!! time-chainage-mvp directory not found")
