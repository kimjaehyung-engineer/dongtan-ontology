import glob
import os
import shutil

f_main = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

targets = [
    r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\restored_dashboard.html'
]

for t in targets:
    if os.path.exists(t):
        shutil.copy2(f_main, t)
        print(f"Copied updated V1 HTML to {t}")
