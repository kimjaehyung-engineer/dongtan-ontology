import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('renderInteractiveElements')
if pos != -1:
    print("=== renderInteractiveElements node setup ===")
    print(text[pos+200:pos+1000])

# Check for #facc15 and #000000 stroke in circle creation
has_yellow = '#facc15' in text
has_black_stroke = 'circle.setAttribute("stroke", "#000000")' in text
print(f"\nYellow fill (#facc15): {has_yellow}")
print(f"Black stroke (#000000): {has_black_stroke}")
