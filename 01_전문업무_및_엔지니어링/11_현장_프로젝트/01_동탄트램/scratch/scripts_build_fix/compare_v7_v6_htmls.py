import os, sys

sys.stdout.reconfigure(encoding='utf-8')

v7_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)v7'
v6_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)v6'

print(f"=== Inspecting HTML counts per subfolder in v7 vs v6 ===")

def inspect_folder(target_path, name):
    print(f"\n--- {name} ({target_path}) ---")
    if not os.path.exists(target_path):
        print("Path does not exist!")
        return
    for item in os.listdir(target_path):
        sub = os.path.join(target_path, item)
        if os.path.isdir(sub):
            html_count = 0
            for r, d, files in os.walk(sub):
                for f in files:
                    if f.endswith('.html') or f.endswith('.htm'):
                        html_count += 1
            print(f"  Folder '{item}': {html_count} HTML files")

inspect_folder(v7_dir, "v7 Folder")
inspect_folder(v6_dir, "v6 Folder")
