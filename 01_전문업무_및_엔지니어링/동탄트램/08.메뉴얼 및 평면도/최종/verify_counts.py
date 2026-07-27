import os

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

total_html = 0
disciplines = {}

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            total_html += 1
            rel_path = os.path.relpath(root, base_dir)
            disc = rel_path.split(os.sep)[0]
            disciplines[disc] = disciplines.get(disc, 0) + 1

print(f"Total HTML files found in attachment directory: {total_html}")
for disc, count in sorted(disciplines.items()):
    print(f"  - {disc}: {count} HTML files")
