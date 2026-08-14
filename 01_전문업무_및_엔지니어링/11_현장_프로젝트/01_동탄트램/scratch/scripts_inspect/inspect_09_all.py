import os, sys
sys.stdout.reconfigure(encoding='utf-8')

dir_09 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표'

for root, dirs, files in os.walk(dir_09):
    print(f"\nDirectory: {root}")
    for d in dirs:
        print(f"  [DIR] {d}")
    for f in files:
        fp = os.path.join(root, f)
        print(f"  [FILE] {f} ({os.path.getsize(fp)} bytes)")
