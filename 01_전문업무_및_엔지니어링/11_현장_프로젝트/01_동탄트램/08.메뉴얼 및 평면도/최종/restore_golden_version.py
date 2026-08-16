import os
import shutil
import subprocess
import sys

# UTF-8 출력 설정
sys.stdout.reconfigure(encoding='utf-8')

print("==========================================================")
print("🚀 [동탄트램 프로세스 맵 v2] 골든 마스터 버전(v2.0) 복원 도구")
print("==========================================================")

base_dir = os.path.dirname(os.path.abspath(__file__))
backup_dir = os.path.join(base_dir, '03_process-map-web-v2(집행단계)_GOLDEN_BACKUP')
target_dir = os.path.join(base_dir, '03_process-map-web-v2(집행단계)')

if not os.path.exists(backup_dir):
    print("❌ 백업 폴더를 찾을 수 없습니다:", backup_dir)
    sys.exit(1)

# 1. 소스 코드 복원 (src, package.json, vite.config.ts 등)
for root, dirs, files in os.walk(backup_dir):
    rel_path = os.path.relpath(root, backup_dir)
    dest_root = os.path.join(target_dir, rel_path)
    os.makedirs(dest_root, exist_ok=True)
    for f in files:
        src_file = os.path.join(root, f)
        dest_file = os.path.join(dest_root, f)
        shutil.copy2(src_file, dest_file)

print("✅ 1. 핵심 소스코드 복원 완료!")

# 2. 골든 HTML 파일 복원
golden_html = os.path.join(base_dir, 'process-map-web-v2_GOLDEN_SNAPSHOT.html')
if os.path.exists(golden_html):
    shutil.copy2(golden_html, os.path.join(base_dir, 'process-map-web-v2.html'))
    shutil.copy2(golden_html, os.path.join(target_dir, 'process-map-web-v2.html'))
    print("✅ 2. 단일 실행형 process-map-web-v2.html 즉시 복원 완료!")

print("\n🎉 완벽한 6대 세로축 및 6대 Phase 정렬 골든 버전으로 100% 원복되었습니다!")
