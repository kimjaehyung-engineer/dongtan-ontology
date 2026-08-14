import sys
sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\add_intersection_zoom_modal.py'

with open(f_path, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
print(f"Total lines: {len(lines)}")
for i in range(0, len(lines), 30):
    chunk = lines[i:i+30]
    print(f"--- Line {i+1} ---")
    print('\n'.join(chunk[:5]))
