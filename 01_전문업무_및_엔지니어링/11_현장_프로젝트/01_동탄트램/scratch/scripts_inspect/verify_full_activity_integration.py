import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print("HTML size:", len(text))
print("Contains activitiesDatabase:", 'activitiesDatabase' in text)
print("Contains renderActivityTree:", 'renderActivityTree' in text)
print("Contains focusActivityOnMap:", 'focusActivityOnMap' in text)
print("Contains 513개 Activity:", '513개 Activity' in text)

idx = text.find('function renderActivityTree(')
if idx != -1:
    print("\n=== renderActivityTree SNIPPET ===")
    print(text[idx:idx+900])
