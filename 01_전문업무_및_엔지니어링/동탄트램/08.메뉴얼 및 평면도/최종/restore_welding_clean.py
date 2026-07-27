import shutil
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

backup_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\메일송부(0723)\매뉴얼BODY(집행단계-첨부폴더)"
target_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

gongjong = "콘크리트도상"
folder = "3_레일 용접장 선정"

src_dir = os.path.join(backup_base, gongjong, folder)
dst_dir = os.path.join(target_base, gongjong, folder)

restored_count = 0
if os.path.exists(src_dir):
    for sub in ['표준서', '수행지침', '체크리스트']:
        src_sub = os.path.join(src_dir, sub)
        dst_sub = os.path.join(dst_dir, sub)
        
        if os.path.exists(src_sub):
            # Clean dst directory files first to avoid duplicates
            if os.path.exists(dst_sub):
                for f in os.listdir(dst_sub):
                    if f.endswith('.html'):
                        os.remove(os.path.join(dst_sub, f))
            os.makedirs(dst_sub, exist_ok=True)
            for f in os.listdir(src_sub):
                src_file = os.path.join(src_sub, f)
                dst_file = os.path.join(dst_sub, f)
                shutil.copy2(src_file, dst_file)
                restored_count += 1
                print(f"Restored clean original: {gongjong}/{folder}/{sub}/{f}")
                
print(f"\n🎉 Successfully restored {restored_count} clean original files for 레일 용접장 선정!")
