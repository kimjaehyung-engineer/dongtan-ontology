import sys
sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\test_full_dashboard.js'

with open(f_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in test_full_dashboard.js: {len(lines)}")
for i in range(max(0, 770), min(len(lines), 810)):
    print(f"Line {i+1}: {lines[i]}", end='')
