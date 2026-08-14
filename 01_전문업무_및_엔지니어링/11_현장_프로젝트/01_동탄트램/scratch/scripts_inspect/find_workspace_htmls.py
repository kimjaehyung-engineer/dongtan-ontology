import os, sys

sys.stdout.reconfigure(encoding='utf-8')

root_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'

print(f"=== Searching for ALL HTML files across the ENTIRE WORKSPACE ({root_dir}) ===")

found_htmls = []
for r, d, files in os.walk(root_dir):
    # skip node_modules or .git
    if 'node_modules' in r or '.git' in r or 'dist' in r:
        continue
    for f in files:
        if f.endswith('.html') or f.endswith('.htm'):
            found_htmls.append(os.path.join(r, f))

print(f"Total HTML files found in workspace: {len(found_htmls)}")

# Categorize HTML files by parent directory
dir_html_counts = {}
for p in found_htmls:
    parent = os.path.dirname(p)
    dir_html_counts[parent] = dir_html_counts.get(parent, 0) + 1

print("\n=== Top Directory Groups with HTML Files ===")
for d, count in sorted(dir_html_counts.items(), key=lambda x: x[1], reverse=True)[:30]:
    rel_d = os.path.relpath(d, root_dir)
    print(f"  [{count} files] {rel_d}")
