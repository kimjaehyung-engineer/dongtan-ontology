import os, sys, shutil

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\최종'
src_dir = os.path.join(base_dir, '매뉴얼BODY(집행단계-첨부폴더)')
v6_dir = os.path.join(base_dir, '매뉴얼BODY(집행단계-첨부폴더)v6')

sectors = ['전기분야', '통신분야']

for sec in sectors:
    s_path = os.path.join(src_dir, sec)
    d_path = os.path.join(v6_dir, sec)
    if os.path.exists(s_path):
        if os.path.exists(d_path):
            shutil.rmtree(d_path)
        shutil.copytree(s_path, d_path)
        print(f"✓ Restored '{sec}' to v6 folder successfully!")
