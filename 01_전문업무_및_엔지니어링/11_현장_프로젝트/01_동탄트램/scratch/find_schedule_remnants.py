import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Find remaining schedule CSS
for keyword in ['schedule-panel', 'btn-open-schedule-panel', 'sch-tree', 'sch-badge', 'sch-act', 'act-focus-pulse', 'act-pulse']:
    positions = [m.start() for m in re.finditer(re.escape(keyword), text)]
    if positions:
        for p in positions:
            ctx = text[max(0,p-100):p+200]
            print(f"\n--- '{keyword}' at {p} ---")
            print(ctx)
