import os

base_root = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)'

all_dirs = [d for d in os.listdir(base_root) if os.path.isdir(os.path.join(base_root, d))]

with open(r'scratch\all_attached_dirs.txt', 'w', encoding='utf-8') as f:
    f.write("매뉴얼BODY(집행단계-첨부폴더) 하위 전체 폴더:\n\n")
    for idx, d in enumerate(all_dirs, 1):
        f.write(f"{idx:2d}. {d}\n")

print("all_attached_dirs.txt 작성 완료!")
