import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print("HTML size:", len(text))
print("Contains floating-trigger-group:", 'floating-trigger-group' in text)
print("Contains btn-open-drawer-panel:", 'btn-open-drawer-panel' in text)
print("Contains btn-open-schedule-panel:", 'btn-open-schedule-panel' in text)

idx = text.find('class="floating-trigger-group"')
if idx != -1:
    print("\n=== floating-trigger-group HTML SNIPPET ===")
    print(text[idx-50:idx+450])
