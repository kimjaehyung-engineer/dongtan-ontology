import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

checks = [
    ('SVG layer group', 'id="construction-sections-group"'),
    ('Layer toggle checkbox', 'toggle-construction-sections'),
    ('Header quick nav', 'id="section-quick-nav"'),
    ('constructionSections data', 'const constructionSections = '),
    ('renderConstructionSections function', 'function renderConstructionSections()'),
    ('renderConstructionSections init call', 'renderConstructionSections();'),
    ('Toggle event listener', 'toggle-construction-sections'),
    ('Section quick nav listener', 'sectionQuickNavEl'),
]

all_ok = True
for name, pattern in checks:
    found = pattern in html
    status = '✅' if found else '❌'
    if not found:
        all_ok = False
    print(f'  {status} {name}')

print(f'\nFile size: {len(html)} bytes')
print('Overall:', '✅ ALL CHECKS PASSED' if all_ok else '❌ SOME CHECKS FAILED')
