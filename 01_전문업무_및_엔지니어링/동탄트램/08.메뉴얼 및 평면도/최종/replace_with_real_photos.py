import shutil
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Source real photo images from Antigravity Brain
src_yard = r"C:\Users\sskjh\.gemini\antigravity\brain\887aacfa-3165-4be1-8e89-29f90e47a298\rail_welding_yard_view_real_1784940360828.jpg"
src_close = r"C:\Users\sskjh\.gemini\antigravity\brain\887aacfa-3165-4be1-8e89-29f90e47a298\rail_welding_closeup_real_1784940372727.jpg"

# Destination directory
dst_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"

dst_yard = os.path.join(dst_dir, "rail_welding_yard_view.jpg")
dst_close = os.path.join(dst_dir, "rail_welding_closeup.jpg")

try:
    # Overwrite existing files
    shutil.copy2(src_yard, dst_yard)
    shutil.copy2(src_close, dst_close)
    print(f"🎉 Successfully replaced and overwrote images with photorealistic construction photos in {dst_dir}!")
except Exception as e:
    print(f"❌ Error replacing images: {e}")
