import os

base_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반'

removed_count = 0

for root, dirs, files in os.walk(base_root):
    for f in files:
        if f.endswith('.html'):
            # 파일명이 숫자로 시작하는 구버전 찌꺼기 파일 (예: 1_..., 10_..., 23_...)
            if f[0].isdigit():
                full_path = os.path.join(root, f)
                try:
                    os.remove(full_path)
                    removed_count += 1
                except Exception as e:
                    print(f"Error removing {f}: {e}")

print(f"SUCCESS: 총 {removed_count}개의 구버전 찌꺼기 HTML 파일(숫자 접두사 파일)을 삭제 정리하였습니다.")
