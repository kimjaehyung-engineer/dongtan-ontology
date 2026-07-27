import os
import shutil
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

backup_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\메일송부(0723)\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"
target_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트on_track\3_레일 용접장 선정"
# Corrected target path using actual system folder
target_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"

# Ensure we clean the target and copy pristine backup first
def restore_pristine(sub_folder, filename):
    src = os.path.join(backup_base, sub_folder, filename)
    dst_normal = os.path.join(target_base, sub_folder, filename)
    dst_prefixed = os.path.join(target_base, sub_folder, f"3_{filename}")
    
    if os.path.exists(src):
        shutil.copy2(src, dst_normal)
        shutil.copy2(src, dst_prefixed)
        print(f"🔄 Restored pristine {sub_folder}/{filename} from backup.")
        return dst_normal, dst_prefixed
    else:
        print(f"❌ Backup not found: {src}")
        return None, None

# Run restore
std_normal, std_pref = restore_pristine("표준서", "레일 용접장 선정_표준서.html")
gui_normal, gui_pref = restore_pristine("수행지침", "레일 용접장 선정_수행지침.html")
chk_normal, chk_pref = restore_pristine("체크리스트", "레일 용접장 선정_체크리스트.html")

# Define styles and modals to inject
from patch_welding_surgical import minimal_glossary_style
from implement_welding_glossary_interactive import common_modal_html

# 1. Patch Standard HTML
def patch_standard_html(fp):
    if not fp or not os.path.exists(fp): return
    # Standard content has been restored correctly in repair_welding_standard_exact_content.py
    # But let's run it robustly here to ensure correct single injection
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # We will build the correct Standard content to prevent any duplicate imports
    from repair_welding_standard_exact_content import standard_content_final
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(standard_content_final)
    print(f"🎉 Checked Standard content layout: {os.path.basename(fp)}")

# 2. Patch Guideline HTML
def patch_guideline_html(fp):
    if not fp or not os.path.exists(fp): return
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Append minimal style
    if "</style>" in html:
        # Check if already has glossary modal styling
        if ".term-highlight" not in html:
            html = html.replace("</style>", minimal_glossary_style + "\n    </style>")
            
    # Inject highlights inside body - LIMIT 1 (idempotent checks)
    if 'class="term-highlight"' not in html:
        html = html.replace("정척 레일을", '<span class="term-highlight" onclick="openGlossary(\'standard_rail\')">정척레일</span>을', 1)
        html = html.replace("장대레일로 1차", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span>로 1차', 1)
        html = html.replace("장대레일 반출", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span> 반출', 1)
        html = html.replace("가스압접/플래시버트 용접하기", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접</span>/<span class="term-highlight" onclick="openGlossary(\'flash_butt\')">플래시버트 용접</span>하기', 1)
        html = html.replace("가스압접/플래시버트 용접용", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접</span>/<span class="term-highlight" onclick="openGlossary(\'flash_butt\')">플래시버트 용접</span>용', 1)
        html = html.replace("가스압접/플래시버트 용접 및", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접</span>/<span class="term-highlight" onclick="openGlossary(\'flash_butt\')">플래시버트 용접</span> 및', 1)
        
        html = html.replace("비파괴 검사장", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴 검사(NDT)장</span>', 1)
        html = html.replace("비파괴검사(초음파/자분)", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴검사(NDT)</span>', 1)
        html = html.replace("비파괴 시험(UT/MT)", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴 시험(NDT)</span>', 1)
        
    # Inject scene view buttons - ONLY ONCE
    if 'class="scene-link"' not in html:
        html = html.replace("용접장 입지 검토", '용접장 입지 검토 <span class="scene-link" onclick="openScene(\'yard\')">📸 용접장 전경 보기</span>', 1)
        html = html.replace("버(Burr) 전단", '버(Burr) 전단 <span class="scene-link" onclick="openScene(\'flash_butt\')">📸 용접 과정 보기</span>', 1)
        html = html.replace("장대레일 반출", '장대레일 반출 <span class="scene-link" onclick="openScene(\'launching\')">📸 인입(Launching) 보기</span>', 1)
        
    # Inject Modal Div & JS right before </body>
    if "glossaryModal" not in html and "</body>" in html:
        html = html.replace("</body>", common_modal_html + "\n</body>")
        
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"🎉 Surgically patched Guideline: {os.path.basename(fp)}")

# 3. Patch Checklist HTML
def patch_checklist_html(fp):
    if not fp or not os.path.exists(fp): return
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Re-apply risk checklist formatting
    from format_kom_checklists import format_risk_checklist_text
    
    pre_pattern = r'(<tr class="pre-row">.*?<td class="category">.*?</td>\s*<td>)(.*?)(</td>)'
    def pre_repl(match):
        return f"{match.group(1)}\n{format_risk_checklist_text(match.group(2))}                {match.group(3)}"
    ing_pattern = r'(<tr class="ing-row">.*?<td class="category">.*?</td>\s*<td>)(.*?)(</td>)'
    def ing_repl(match):
        return f"{match.group(1)}\n{format_risk_checklist_text(match.group(2))}                {match.group(3)}"
    post_pattern = r'(<tr class="post-row">.*?<td class="category">.*?</td>\s*<td>)(.*?)(</td>)'
    def post_repl(match):
        return f"{match.group(1)}\n{format_risk_checklist_text(match.group(2))}                {match.group(3)}"

    html = re.sub(pre_pattern, pre_repl, html, flags=re.DOTALL)
    html = re.sub(ing_pattern, ing_repl, html, flags=re.DOTALL)
    html = re.sub(post_pattern, post_repl, html, flags=re.DOTALL)
    
    # Append minimal style
    if "</style>" in html and ".term-highlight" not in html:
        html = html.replace("</style>", minimal_glossary_style + "\n    </style>")
        
    # Inject highlights inside body - LIMIT 1
    if 'class="term-highlight"' not in html:
        html = html.replace("장대레일 제작 시", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span> 제작 시', 1)
        html = html.replace("장대레일 영구", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span> 영구', 1)
        html = html.replace("비파괴 시험(UT/MT)", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴 시험(NDT)</span>', 1)
        html = html.replace("NDT 용접부", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">NDT 용접부</span>', 1)
        
    # Inject scene link inside risk checkbox list - LIMIT 1
    if 'class="scene-link"' not in html:
        html = html.replace("수평 오차 초과로", '수평 오차 초과로 <span class="scene-link" onclick="openScene(\'yard\')">📸 롤러 가이드 베드 보기</span>', 1)
        
    # Inject Modal Div & JS right before </body>
    if "glossaryModal" not in html and "</body>" in html:
        html = html.replace("</body>", common_modal_html + "\n</body>")
        
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"🎉 Surgically patched Checklist: {os.path.basename(fp)}")

# Run patch processes
patch_standard_html(std_normal)
patch_standard_html(std_pref)

patch_guideline_html(gui_normal)
patch_guideline_html(gui_pref)

patch_checklist_html(chk_normal)
patch_checklist_html(chk_pref)

print("\n🎉 Idempotent repair complete! All duplicate buttons removed and styled perfectly!")
