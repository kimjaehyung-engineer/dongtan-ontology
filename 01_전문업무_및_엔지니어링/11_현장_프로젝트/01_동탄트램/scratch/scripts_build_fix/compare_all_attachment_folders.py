import os, sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\최종'

folders = [
    '매뉴얼BODY(집행단계-첨부폴더)',
    '매뉴얼BODY(집행단계-첨부폴더)v6',
    '매뉴얼BODY(집행단계-첨부폴더)v7'
]

print("=== Detailed HTML file count comparison across ALL attachment folders ===")

for fname in folders:
    fpath = os.path.join(base_dir, fname)
    print(f"\n📁 [{fname}]")
    if not os.path.exists(fpath):
        print("  -> DOES NOT EXIST!")
        continue
    
    subdirs = [d for d in os.listdir(fpath) if os.path.isdir(os.path.join(fpath, d))]
    for sd in sorted(subdirs):
        sd_path = os.path.join(fpath, sd)
        html_files = []
        all_files = []
        for r, d, files in os.walk(sd_path):
            for f in files:
                all_files.append(os.path.join(r, f))
                if f.endswith('.html') or f.endswith('.htm'):
                    html_files.append(os.path.join(r, f))
        print(f"  - Sector '{sd}': {len(html_files)} HTMLs / Total {len(all_files)} files")
