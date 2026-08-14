import os

deploy_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\deploy\index.html'

if os.path.exists(deploy_html):
    print(f"Found deploy/index.html (size: {os.path.getsize(deploy_html)} bytes)")
    with open(deploy_html, 'r', encoding='utf-8', errors='ignore') as f:
        print(f.read()[:1500])
else:
    print("!! deploy/index.html not found")
