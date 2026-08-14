import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print("HTML size:", len(text))
print("Contains btn-toggle-schedule:", 'id="btn-toggle-schedule"' in text)
print("Contains schedule-panel:", 'id="schedule-panel"' in text)
print("Contains initScheduleIntegration:", 'initScheduleIntegration' in text)
print("Contains renderScheduleTimeline:", 'renderScheduleTimeline' in text)

idx = text.find('function initScheduleIntegration()')
if idx != -1:
    print("\n=== initScheduleIntegration SNIPPET ===")
    print(text[idx:idx+800])
