import os, sys
sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'

print("=== Searching for exact 06 Activity List files in workspace ===")
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if '06' in f and ('Activity' in f or '예정공정표' in f or '공정표' in f):
            path = os.path.join(root, f)
            rel = os.path.relpath(path, base_dir)
            size = os.path.getsize(path)
            print(f"  EXACT MATCH: {rel} ({size} bytes)")
