import os, sys
sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'

print("=== Searching for Activity List Excel / Schedule Files ===")
found_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if '06' in f or 'Activity' in f or '예정공정표' in f or 'Activity List' in f:
            path = os.path.join(root, f)
            rel = os.path.relpath(path, base_dir)
            size = os.path.getsize(path)
            found_files.append((rel, path, size))
            print(f"  Found: {rel} ({size} bytes)")

if not found_files:
    print("  No files matched '06' or 'Activity List' directly in filename search.")
    print("\n  Searching for all .xlsx files in 08.메뉴얼 및 평면도, 09.공정표, 00_원본_데이터...")
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith('.xlsx'):
                path = os.path.join(root, f)
                rel = os.path.relpath(path, base_dir)
                size = os.path.getsize(path)
                print(f"    .xlsx: {rel} ({size} bytes)")
