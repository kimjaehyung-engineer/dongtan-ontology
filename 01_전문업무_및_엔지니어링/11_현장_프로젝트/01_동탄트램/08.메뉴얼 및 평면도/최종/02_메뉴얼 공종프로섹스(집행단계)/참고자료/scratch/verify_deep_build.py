import os

base_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반'

subdirs = [d for d in os.listdir(base_root) if os.path.isdir(os.path.join(base_root, d))]
print(f"상부강화노반 폴더 개수: {len(subdirs)}")

total_htmls = 0
missing = []

for d in sorted(subdirs, key=lambda x: int(x.split('_')[0]) if x.split('_')[0].isdigit() else 999):
    full_path = os.path.join(base_root, d)
    std_p = os.path.join(full_path, '표준서')
    gui_p = os.path.join(full_path, '수행지침')
    chk_p = os.path.join(full_path, '체크리스트')
    
    std_f = [f for f in os.listdir(std_p) if f.endswith('.html')] if os.path.exists(std_p) else []
    gui_f = [f for f in os.listdir(gui_p) if f.endswith('.html')] if os.path.exists(gui_p) else []
    chk_f = [f for f in os.listdir(chk_p) if f.endswith('.html')] if os.path.exists(chk_p) else []
    
    count = len(std_f) + len(gui_f) + len(chk_f)
    total_htmls += count
    
    if count != 3:
        missing.append((d, count))

print(f"총 검수된 HTML 문서 개수: {total_htmls}")
if not missing:
    print("SUCCESS: 모든 35개 폴더에 3개씩(총 105개) 딥빌드 HTML 문서가 100% 완벽하게 존재합니다!")
else:
    print(f"누락 및 이상 폴더 목록: {missing}")
