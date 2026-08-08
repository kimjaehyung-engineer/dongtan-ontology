import os, sys

sys.stdout.reconfigure(encoding='utf-8')

dir_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표'

for f in os.listdir(dir_path):
    print(" -", f)
