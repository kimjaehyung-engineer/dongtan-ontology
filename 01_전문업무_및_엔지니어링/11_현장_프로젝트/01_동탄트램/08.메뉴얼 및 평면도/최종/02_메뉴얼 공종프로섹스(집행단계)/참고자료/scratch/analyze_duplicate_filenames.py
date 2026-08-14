import os

base_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반'

subdirs = [d for d in os.listdir(base_root) if os.path.isdir(os.path.join(base_root, d))]

print("=== 상부강화노반 폴더 내 파일명 패턴 분석 ===")
double_files = []

for d in sorted(subdirs):
    full_p = os.path.join(base_root, d)
    gui_p = os.path.join(full_p, '수행지침')
    if os.path.exists(gui_p):
        files = [f for f in os.listdir(gui_p) if f.endswith('.html')]
        if len(files) > 1:
            double_files.append((d, files))

print(f"2개 이상의 유사 파일명이 존재하는 폴더 개수: {len(double_files)}")
for d, fs in double_files[:10]:
    print(f"폴더 [{d}]:")
    for f in fs:
        fp = os.path.join(base_root, d, '수행지침', f)
        mtime = os.path.getmtime(fp)
        size = os.path.getsize(fp)
        print(f"  - {f} (크기: {size} bytes, 시간: {mtime})")
