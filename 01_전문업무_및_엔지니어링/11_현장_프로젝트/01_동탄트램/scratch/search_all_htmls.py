import os, sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도'

print(f"=== Searching for HTML files in {base_dir} ===")

found_htmls = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html') or f.endswith('.htm'):
            full_path = os.path.join(root, f)
            found_htmls.append(full_path)

print(f"Found total {len(found_htmls)} HTML files.")

for p in found_htmls:
    rel_p = os.path.relpath(p, base_dir)
    print(" -", rel_p)
