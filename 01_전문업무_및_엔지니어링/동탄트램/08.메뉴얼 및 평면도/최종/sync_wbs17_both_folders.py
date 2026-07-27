import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"

folder_with_space = os.path.join(base_dir, "17_[TCL] 궤광 및 철근 조립")
folder_no_space = os.path.join(base_dir, "17_[TCL] 궤광 및 철근조립")

os.makedirs(folder_no_space, exist_ok=True)

# File pairs to copy from folder_with_space to folder_no_space
subfolders = ["표준서", "수행지침", "체크리스트"]

for sub in subfolders:
    src_sub = os.path.join(folder_with_space, sub)
    dst_sub = os.path.join(folder_no_space, sub)
    os.makedirs(dst_sub, exist_ok=True)
    
    if os.path.exists(src_sub):
        for f in os.listdir(src_sub):
            src_file = os.path.join(src_sub, f)
            if os.path.isfile(src_file):
                # Copy as is
                dst_file1 = os.path.join(dst_sub, f)
                shutil.copy(src_file, dst_file1)
                print(f"📋 Synchronized: {dst_file1}")
                
                # Also copy with no-space filename version if needed
                no_space_f = f.replace("철근 조립", "철근조립")
                dst_file2 = os.path.join(dst_sub, no_space_f)
                shutil.copy(src_file, dst_file2)
                print(f"📋 Synchronized: {dst_file2}")

print("\n🎉 SUCCESSFULLY SYNCHRONIZED ALL WBS 17 MASTER FILES TO BOTH FOLDER PATHS!")
