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

target_box_signature = '<div class="bg-emerald-50 border border-emerald-200'

for fp in target_files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if target_box_signature in content:
        # Find start of block
        idx_start = content.find(target_box_signature)
        # Find closing </div> for this block
        idx_end = content.find('</div>', idx_start)
        if idx_end != -1:
            idx_end_full = idx_end + len('</div>')
            new_content = content[:idx_start] + content[idx_end_full:]
            
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"   ✓ [UNREALISTIC BOX REMOVED] -> {os.path.basename(fp)}")
        else:
            print(f"   ⚠️ Could not find closing div for {os.path.basename(fp)}")
    else:
        print(f"   ℹ️ Box not present in {os.path.basename(fp)}")

print("\n🎉 SUCCESSFULLY REMOVED UNREALISTIC APPROVAL SIGNATURE BOX FROM ALL STANDARD HTML FILES!")
