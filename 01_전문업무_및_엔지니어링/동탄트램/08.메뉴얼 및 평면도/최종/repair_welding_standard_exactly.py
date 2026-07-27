import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

backup_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\메일송부(0723)\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"
target_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"

# 1. First, restore the exact pristine original standard HTML files from backup (메일송부(0723))
std_filename = "레일 용접장 선정_표준서.html"
src_std = os.path.join(backup_base, "표준서", std_filename)
dst_std1 = os.path.join(target_base, "표준서", std_filename)
dst_std2 = os.path.join(target_base, "표준서", f"3_{std_filename}")

if os.path.exists(src_std):
    shutil.copy2(src_std, dst_std1)
    shutil.copy2(src_std, dst_std2)
    print(f"🎉 Restored pristine original standard HTML from backup to {dst_std1} and {dst_std2}")
else:
    print("❌ Backup standard HTML not found!")
    sys.exit(1)

# Minimal CSS and JS for interactive glossary popups - ZERO layout override
from patch_welding_surgical import minimal_glossary_style
from implement_welding_glossary_interactive import common_modal_html

def surgically_patch_standard_content(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Append styling to style section
    if "</style>" in html:
        html = html.replace("</style>", minimal_glossary_style + "\n    </style>")
        
    # Replace terms only once to avoid cluttering
    html = html.replace("정척레일 15본", '<span class="term-highlight" onclick="openGlossary(\'standard_rail\')">정척레일</span> 15본', 1)
    html = html.replace("정척레일(25m)", '<span class="term-highlight" onclick="openGlossary(\'standard_rail\')">정척레일(25m)</span>', 1)
    html = html.replace("장대레일 제작하는", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span> 제작하는', 1)
    html = html.replace("장대로 용접하는", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span>로 용접하는', 1)
    html = html.replace("테르밋 및", '<span class="term-highlight" onclick="openGlossary(\'thermit\')">테르밋</span> 및', 1)
    html = html.replace("가스압접 용접을", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접 용접</span>을', 1)
    html = html.replace("NDT 작업 공간", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">NDT(비파괴검사)</span> 작업 공간', 1)
    
    # Scene photo link (ONLY once)
    html = html.replace("레일 용접장 선정 정량적", '레일 용접장 선정 <span class="scene-link" onclick="openScene(\'yard\')">📸 용접장 전경 보기</span> 정량적', 1)
    
    # Inject Modal Div & JS right before </body>
    if "</body>" in html:
        html = html.replace("</body>", common_modal_html + "\n</body>")
        
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"🎉 Surgically patched standard file: {os.path.basename(fp)}")

surgically_patch_standard_content(dst_std1)
surgically_patch_standard_content(dst_std2)

print("\n🎉 Rail welding yard standard successfully repaired to the perfect original content and format!")
