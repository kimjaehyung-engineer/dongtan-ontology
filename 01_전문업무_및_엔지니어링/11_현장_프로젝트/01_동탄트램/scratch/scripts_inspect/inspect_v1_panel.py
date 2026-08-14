import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Check CSS for .drawer-item-card
idx_css = text.find('.drawer-item-card {')
if idx_css != -1:
    print("=== CSS FOR DRAWER CARD ===")
    print(text[idx_css:idx_css+400])

# Check renderIntersections
idx_ri = text.find('function renderIntersections()')
if idx_ri != -1:
    print("\n=== renderIntersections START ===")
    print(text[idx_ri:idx_ri+400])

# Check drawer-controls HTML
idx_dc = text.find('<div class="drawer-controls">')
if idx_dc != -1:
    print("\n=== DRAWER CONTROLS HTML ===")
    print(text[idx_dc:idx_dc+400])
