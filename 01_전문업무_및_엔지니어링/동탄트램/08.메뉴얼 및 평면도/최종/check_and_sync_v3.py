import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종"

print("Listing all .xlsx files in destination folder:")
for f in os.listdir(base_dir):
    if f.endswith('.xlsx') and not f.startswith('~$'):
        print(f" - {f}")

# Target file to update: '매뉴얼 BODY (집행단계)v3.xlsx' or similar
source_file = None
for f in os.listdir(base_dir):
    if "최종업그레이드" in f and f.endswith('.xlsx'):
        source_file = os.path.join(base_dir, f)
        break

if not source_file:
    # Fallback to any recent v3 file
    for f in sorted(os.listdir(base_dir), reverse=True):
        if "v3" in f and f.endswith('.xlsx') and not f.startswith('~$'):
            source_file = os.path.join(base_dir, f)
            break

target_file = os.path.join(base_dir, "매뉴얼 BODY (집행단계)v3.xlsx")

print(f"\nSource file selected: {source_file}")
print(f"Target file selected: {target_file}")

if source_file and os.path.exists(source_file):
    try:
        shutil.copy2(source_file, target_file)
        print(f"🎉 Successfully linked and overwritten '{target_file}' with latest upgraded content!")
    except Exception as e:
        print(f"⚠️ Copy failed: {e}")
