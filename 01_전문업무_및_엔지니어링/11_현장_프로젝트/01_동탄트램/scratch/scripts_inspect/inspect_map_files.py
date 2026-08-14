import re, os

files = ['동탄트램_노선평면도.html', '동탄트램_노선평면도V1.html', '동탄도시철도_시스템_실시간_시뮬레이터.html']
base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도'

for filename in files:
    path = os.path.join(base_dir, filename)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    print(f'=== {filename} ===')
    matches = re.findall(r'.{0,30}(?:1공구|2공구|공구).{0,30}', content)
    for m in matches[:10]:
        print('  [공구 언급]:', m.replace('\n', ' ').strip())
    
    onclicks = re.findall(r'onclick=["\'](.*?)["\']', content)
    print(f'  [Onclick count]: {len(onclicks)}')
    print('  [Sample onclicks]:', onclicks[:5])
    
    # Check station click modals
    if 'openModal' in content or 'modal' in content:
        print('  [Interactive Modal]: Yes! (Station click opens detailed modal/popup)')
    print()
