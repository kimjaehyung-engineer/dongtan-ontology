import os, sys
sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'

print("=== Searching for Schedule / 공정표 files ===")
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if any(kw in f for kw in ['공정', '공기', 'Schedule', 'gantt', 'chainage', 'timeline']) or f.endswith(('.xlsx', '.html', '.json', '.dwg')):
            rel = os.path.relpath(os.path.join(root, f), base_dir)
            print(f"  {rel}")
