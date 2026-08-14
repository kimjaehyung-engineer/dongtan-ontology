import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix: Replace panTo(posX, posY) with focusCoordinates(posX, posY) in selectIntersection
old = "  panTo(posX, posY);"
new = "  focusCoordinates(posX, posY);"

count = text.count(old)
print(f"Found {count} occurrence(s) of panTo(posX, posY)")

text = text.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed: panTo -> focusCoordinates")
