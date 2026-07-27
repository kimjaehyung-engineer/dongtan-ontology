import shutil
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_file = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\1_설계적정성 검토\체크리스트\1_설계적정성 검토_체크리스트.html"
dst_file = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\1_설계적정성 검토\체크리스트\설계적정성 검토_체크리스트.html"

try:
    shutil.copy2(src_file, dst_file)
    print(f"🎉 Successfully copied updated checklist to target path: {dst_file}")
except Exception as e:
    print(f"❌ Error copying file: {e}")
