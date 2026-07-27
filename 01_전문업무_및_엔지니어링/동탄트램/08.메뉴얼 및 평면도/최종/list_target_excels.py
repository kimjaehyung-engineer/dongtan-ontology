import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

dir_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종"

for f in os.listdir(dir_path):
    if f.endswith(('.xlsx', '.xls')):
        print(f"Excel File: {f}")
