import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Check all panTo references
print("=== ALL panTo references ===")
for m in re.finditer(r'panTo', text):
    start = max(0, m.start()-50)
    end = min(len(text), m.end()+100)
    print(text[start:end])
    print("-"*40)

# 2. Check focusCoordinates function
print("\n=== focusCoordinates function ===")
idx = text.find('function focusCoordinates(')
if idx != -1:
    print(text[idx:idx+400])

# 3. Check focusCoordinatesCustom function
print("\n=== focusCoordinatesCustom function ===")
idx2 = text.find('function focusCoordinatesCustom(')
if idx2 != -1:
    print(text[idx2:idx2+400])

# 4. Check selectStation function (the station quick nav uses this)
print("\n=== selectStation function ===")
idx3 = text.find('function selectStation(')
if idx3 != -1:
    print(text[idx3:idx3+500])
