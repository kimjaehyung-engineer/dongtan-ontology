import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\통신분야"

folder_names = [
    "8_자재 인력 장비 등 투입 사전 검토",
    "8_자재 _ 인원 _ 장비 등 투입 사전 검토"
]

target_files = []
for fn in folder_names:
    std_p = os.path.join(base_dir, fn, "표준서")
    if os.path.exists(std_p):
        for f in os.listdir(std_p):
            if f.endswith('.html'):
                target_files.append(os.path.join(std_p, f))

for fp in target_files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if "<!-- 🖊️ 3. 자원 투입 최종 승인 절차 -->" in content:
        content = content.replace("<!-- 🖊️ 3. 자원 투입 최종 승인 절차 -->", "")
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✓ [CLEANED COMMENT] -> {os.path.basename(fp)}")

print("\n🎉 SUCCESSFULLY CLEANED REMNANT COMMENT!")
