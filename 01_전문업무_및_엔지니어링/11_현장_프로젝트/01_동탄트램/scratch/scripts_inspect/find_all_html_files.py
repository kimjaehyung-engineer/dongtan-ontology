import os

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'

print("=== Searching for index.html or time-chainage html across workspace ===")
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if 'chainage' in f.lower() or ('index' in f.lower() and f.endswith('.html')):
            full = os.path.join(root, f)
            print(f"Found: {full}")
