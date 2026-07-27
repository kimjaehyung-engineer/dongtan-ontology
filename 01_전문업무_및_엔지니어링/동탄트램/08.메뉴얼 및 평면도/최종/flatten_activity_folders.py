import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_attach_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

target_subfolders = ['표준서', '수행지침', '체크리스트']

moved_files_count = 0
removed_dirs_count = 0

for root, dirs, files in os.walk(base_attach_dir, topdown=False):
    dirname = os.path.basename(root)
    if dirname in target_subfolders:
        parent_dir = os.path.dirname(root)
        # Move all files in root to parent_dir
        for f in files:
            src_path = os.path.join(root, f)
            dest_path = os.path.join(parent_dir, f)
            # Handle potential file collision safely
            if os.path.exists(dest_path) and src_path != dest_path:
                os.remove(dest_path)
            shutil.move(src_path, dest_path)
            moved_files_count += 1
            
        # After moving files, remove the subfolder if empty
        remaining = os.listdir(root)
        if not remaining:
            os.rmdir(root)
            removed_dirs_count += 1

print(f"Flattening complete!")
print(f"  - Total files moved out to activity folders: {moved_files_count}")
print(f"  - Total subfolders ('표준서', '수행지침', '체크리스트') removed: {removed_dirs_count}")
