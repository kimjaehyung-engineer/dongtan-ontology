import os

tc_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp'

print("=== Checking files directly under time-chainage-mvp ===")
for item in os.listdir(tc_dir):
    full_path = os.path.join(tc_dir, item)
    is_dir = os.path.isdir(full_path)
    print(f" {'[DIR]' if is_dir else '[FILE]'} {item}")
