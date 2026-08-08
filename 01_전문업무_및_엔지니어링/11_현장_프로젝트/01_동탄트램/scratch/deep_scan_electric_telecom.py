import os, sys

sys.stdout.reconfigure(encoding='utf-8')

target_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'

print(f"=== Deep Scanning for Electric & Telecom HTML files in {target_root} ===")

electric_telecom_files = []

for root, dirs, files in os.walk(target_root):
    if 'node_modules' in root or '.git' in root:
        continue
    for f in files:
        if f.endswith('.html') or f.endswith('.htm'):
            low_f = f.lower()
            low_r = root.lower()
            if '전기' in low_r or '전기' in low_f or '통신' in low_r or '통신' in low_f or '전력' in low_f or '변전' in low_f:
                full_p = os.path.join(root, f)
                electric_telecom_files.append(full_p)

print(f"Found {len(electric_telecom_files)} Electric & Telecom related HTML files:")
for p in electric_telecom_files:
    rel_p = os.path.relpath(p, target_root)
    print("  -", rel_p)
