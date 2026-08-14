import os, sys
sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'

print("=== Search for 06_기술제안 / Activity List files ===")
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if '06' in f or 'Activity' in f or '예정공정표' in f or 'Activity List' in f or '천우씨엠' in f:
            path = os.path.join(root, f)
            rel = os.path.relpath(path, base_dir)
            size = os.path.getsize(path)
            print(f"  {rel} ({size} bytes)")
