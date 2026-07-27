import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

excel_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종"

rel_path = r"매뉴얼BODY(집행단계-첨부폴더)\상부강화노반\1_지반조사 상세검토\표준서\지반조사 상세검토_표준서.html"

full_path = os.path.join(excel_dir, rel_path)

print("Testing path resolution:")
print("Relative path:", rel_path)
print("Resolved full path:", full_path)
print("File exists on disk:", os.path.exists(full_path))
