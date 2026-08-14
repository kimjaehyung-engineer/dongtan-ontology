import os, sys
sys.stdout.reconfigure(encoding='utf-8')

dir_tc = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp'

print("=== ALL FILES in time-chainage-mvp ===")
for root, dirs, files in os.walk(dir_tc):
    for f in files:
        path = os.path.join(root, f)
        rel = os.path.relpath(path, dir_tc)
        size = os.path.getsize(path)
        print(f"  {rel} ({size} bytes)")
