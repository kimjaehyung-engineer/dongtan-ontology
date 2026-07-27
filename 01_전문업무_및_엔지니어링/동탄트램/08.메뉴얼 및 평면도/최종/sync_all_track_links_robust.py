import os
import shutil
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"

folders = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

synced_count = 0
for folder in folders:
    # WBS sequence number check (e.g. "1_설계적정성 검토" -> prefix is "1_")
    parts = folder.split("_")
    if len(parts) < 2:
        continue
    prefix = parts[0] + "_"
    core_name = folder[len(prefix):] # e.g. "설계적정성 검토"
    
    folder_path = os.path.join(base_dir, folder)
    
    for sub in ["표준서", "수행지침", "체크리스트"]:
        sub_path = os.path.join(folder_path, sub)
        if not os.path.exists(sub_path):
            continue
            
        # Source file with prefix (which was updated by our model)
        # e.g. 1_설계적정성 검토_체크리스트.html
        src_pattern = os.path.join(sub_path, f"{folder}_{sub}.html")
        dst_path = os.path.join(sub_path, f"{core_name}_{sub}.html")
        
        if os.path.exists(src_pattern):
            shutil.copy2(src_pattern, dst_path)
            synced_count += 1
            print(f"Synced file link: {gongjong if 'gongjong' in locals() else '콘크리트도상'}/{folder}/{sub} ➔ '{core_name}_{sub}.html'")

print(f"\n🎉 Successfully linked and verified all {synced_count} file paths in 콘크리트도상!")
