import glob
import os

search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
htmls = glob.glob(os.path.join(search_dir, '**', '*.html'), recursive=True)

print(f"Total HTML files found: {len(htmls)}")
for h in htmls:
    try:
        with open(h, 'r', encoding='utf-8') as f:
            txt = f.read()
        has_btn = ('교차로 상세' in txt) or ('openIntersectionModal' in txt) or ('교차로' in txt and '도면' in txt)
        if has_btn:
            rel = os.path.relpath(h, search_dir)
            print(f"\nMATCH: {rel}")
            print(f"  - button text ('교차로 상세 확대 도면 보기'): {'교차로 상세 확대 도면 보기' in txt}")
            print(f"  - openIntersectionModal func: {'function openIntersectionModal' in txt}")
            print(f"  - openIntersectionModal call: {'openIntersectionModal(' in txt}")
            print(f"  - modal overlay container: {'intersectionModal' in txt or 'intersectionZoomModal' in txt or 'modal-overlay' in txt}")
    except Exception as e:
        pass
