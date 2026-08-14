import os

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표'

print("=== Checking 09.공정표 subdirectories ===")
for root, dirs, files in os.walk(base_dir):
    rel = os.path.relpath(root, base_dir)
    print(f"[{rel}]")
    for f in files:
        if f.endswith(('.html', '.js', '.jsx', '.tsx', '.json')):
            print(f"  - {f}")
