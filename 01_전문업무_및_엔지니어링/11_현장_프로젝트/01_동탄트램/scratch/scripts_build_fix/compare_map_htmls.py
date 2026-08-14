import os

f1 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램_노선평면도.html'
f2 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

for path in [f1, f2]:
    print("="*60)
    print("FILE:", path)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            txt = f.read()
        print(f"Size: {len(txt)} bytes")
        print(f"Contains '교차로 상세 확대 도면 보기': {'교차로 상세 확대 도면 보기' in txt}")
        print(f"Contains 'function openIntersectionModal': {'function openIntersectionModal' in txt}")
        print(f"Contains 'id=\"intersectionZoomModal\"' or 'id=\"intersectionModal\"': {'intersectionZoomModal' in txt or 'intersectionModal' in txt}")
    else:
        print("DOES NOT EXIST")
