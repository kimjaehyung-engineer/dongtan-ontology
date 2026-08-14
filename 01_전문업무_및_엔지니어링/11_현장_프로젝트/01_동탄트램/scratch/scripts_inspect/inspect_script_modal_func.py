import sys
sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\add_intersection_zoom_modal.py'

with open(f_path, 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function openIntersectionModal')
if idx != -1:
    print("Found openIntersectionModal in python script:")
    print(text[idx:idx+3500])
