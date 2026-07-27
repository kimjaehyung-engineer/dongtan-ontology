import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\통신분야"

folder1 = os.path.join(base_dir, "8_자재 인력 장비 등 투입 사전 검토")
folder2 = os.path.join(base_dir, "8_자재 _ 인원 _ 장비 등 투입 사전 검토")

# Copy entire enriched tree from folder1 to folder2
if os.path.exists(folder1):
    os.makedirs(folder2, exist_ok=True)
    for root, dirs, files in os.walk(folder1):
        rel_path = os.path.relpath(root, folder1)
        target_root = os.path.join(folder2, rel_path)
        os.makedirs(target_root, exist_ok=True)
        
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_root, file)
            shutil.copy2(src_file, dst_file)
            print(f"   ✓ [COPIED] {file} -> {target_root}")

            # Also create underscore variant file names if needed
            alt_name = file.replace("자재 인력 장비", "자재 _ 인원 _ 장비")
            if alt_name != file:
                alt_dst = os.path.join(target_root, alt_name)
                shutil.copy2(src_file, alt_dst)
                print(f"   ✓ [VARIANT COPIED] {alt_name} -> {target_root}")

print("\n🎉 SUCCESSFULLY SYNCHRONIZED BOTH FOLDER PATHS FOR WBS 9000-2-8!")
