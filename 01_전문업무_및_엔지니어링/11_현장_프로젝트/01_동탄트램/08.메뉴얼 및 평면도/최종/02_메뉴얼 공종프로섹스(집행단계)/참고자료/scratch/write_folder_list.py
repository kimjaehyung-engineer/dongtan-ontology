import os

base_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\상부강화노반'

actual_folders = sorted([d for d in os.listdir(base_root) if os.path.isdir(os.path.join(base_root, d))])

with open(r'scratch\actual_folder_list.txt', 'w', encoding='utf-8') as f:
    f.write(f"총 실제 폴더 개수: {len(actual_folders)}\n\n")
    for idx, d in enumerate(actual_folders, 1):
        f.write(f"{idx:2d}. {d}\n")

print("actual_folder_list.txt 작성 완료!")
