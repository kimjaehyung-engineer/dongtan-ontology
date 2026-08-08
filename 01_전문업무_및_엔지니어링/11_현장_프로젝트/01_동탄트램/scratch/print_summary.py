import os, re

files = [
    r'08.메뉴얼 및 평면도\동탄트램_노선평면도.html',
    r'08.메뉴얼 및 평면도\동탄트램_노선평면도V1.html',
    r'08.메뉴얼 및 평면도\deploy\dongtan_dashboard.html'
]
base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'

for rel in files:
    path = os.path.join(base_dir, rel)
    if os.path.exists(path):
        print(f'FILE: {rel}')
        print(f'PATH: {path}')
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            print(f'Lines: {len(lines)}')
            head = "".join(lines[:30])
            title = re.search(r'<title>(.*?)</title>', head, re.I)
            if title:
                print(f'Title: {title.group(1)}')
        print('-'*60)
