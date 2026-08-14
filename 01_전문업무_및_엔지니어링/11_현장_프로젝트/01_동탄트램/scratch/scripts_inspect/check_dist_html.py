import os

dist_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\index.html'

if os.path.exists(dist_html):
    print(f"✓ Found dist/index.html (size: {os.path.getsize(dist_html)} bytes)")
    with open(dist_html, 'r', encoding='utf-8') as f:
        print(f.read())
else:
    print("!! dist/index.html NOT found")
