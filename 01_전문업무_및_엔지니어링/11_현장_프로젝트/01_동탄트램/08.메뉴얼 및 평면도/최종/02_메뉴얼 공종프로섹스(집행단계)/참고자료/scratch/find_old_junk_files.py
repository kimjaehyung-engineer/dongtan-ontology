import os

base_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반'

old_junk_files = []

for root, dirs, files in os.walk(base_root):
    for f in files:
        if f.endswith('.html'):
            # 파일명이 숫자로 시작하는 구버전 파일 체크 (예: 1_..., 10_..., 23_...)
            if f[0].isdigit():
                full_path = os.path.join(root, f)
                size = os.path.getsize(full_path)
                mtime = os.path.getmtime(full_path)
                old_junk_files.append((full_path, f, size))

print(f"발견된 구버전 찌꺼기 HTML 파일 개수: {len(old_junk_files)}")
print("\n--- 구버전 찌꺼기 파일 샘플 (상위 10개) ---")
for path, name, sz in old_junk_files[:10]:
    print(f"구버전 파일: {name} (크기: {sz} bytes)")
