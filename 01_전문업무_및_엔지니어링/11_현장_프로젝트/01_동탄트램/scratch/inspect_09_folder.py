import os, sys
sys.stdout.reconfigure(encoding='utf-8')

dir_09 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표'

print("=== ALL FILES inside 09.공정표 ===")
found = 0
for root, dirs, files in os.walk(dir_09):
    for f in files:
        found += 1
        path = os.path.join(root, f)
        rel = os.path.relpath(path, dir_09)
        size = os.path.getsize(path)
        print(f"  {rel} ({size} bytes)")

if found == 0:
    print("  No files found directly in 09.공정표")
