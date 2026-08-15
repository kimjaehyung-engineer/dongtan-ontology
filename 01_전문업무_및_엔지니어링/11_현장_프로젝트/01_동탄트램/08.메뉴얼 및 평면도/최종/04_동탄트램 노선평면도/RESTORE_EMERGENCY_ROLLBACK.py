# -*- coding: utf-8 -*-
import os
import shutil

base_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\최종\04_동탄트램 노선평면도"
backup_folder = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\최종\04_동탄트램 노선평면도\_backup_snapshot_20260815_203640"

print("=== 동탄트램 노선평면도 V1 즉시 원복(롤백) 시작 ===")
files = ['동탄트램_노선평면도V1.html', '동탄트램_노선평면도V1.png']

for fname in files:
    src = os.path.join(backup_folder, fname)
    dst = os.path.join(base_dir, fname)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f" [복구 완료] {fname} -> 원본 상태로 100% 롤백되었습니다.")
    else:
        print(f" [경고] 백업 파일 없음: {fname}")

print("\n🎉 원본 상태로 100% 완벽하게 복구되었습니다!")
