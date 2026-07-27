import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

backup_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\메일송부(0723)\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"
target_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"

# Standard minimal popup styles and modals
from patch_welding_surgical import minimal_glossary_style
from implement_welding_glossary_interactive import common_modal_html

# Force clear and recreate files to eliminate OS file write leftovers
def clean_recreate_dir(path):
    if os.path.exists(path):
        for f in os.listdir(path):
            if f.endswith('.html'):
                try:
                    os.remove(os.path.join(path, f))
                except:
                    pass
    os.makedirs(path, exist_ok=True)

# Clean target directories
clean_recreate_dir(os.path.join(target_base, "표준서"))
clean_recreate_dir(os.path.join(target_base, "수행지침"))
clean_recreate_dir(os.path.join(target_base, "체크리스트"))

# 1. Compile Standard HTML (We already have standard_content_final which has perfect single modal)
from repair_welding_standard_exact_content import standard_content_final

std_fn1 = os.path.join(target_base, "표준서", "레일 용접장 선정_표준서.html")
std_fn2 = os.path.join(target_base, "표준서", "3_레일 용접장 선정_표준서.html")

with open(std_fn1, 'w', encoding='utf-8') as f:
    f.write(standard_content_final)
with open(std_fn2, 'w', encoding='utf-8') as f:
    f.write(standard_content_final)
print("🎉 Re-written Standard HTML files cleanly.")

# 2. Compile Guideline HTML
src_gui = os.path.join(backup_base, "수행지침", "레일 용접장 선정_수행지침.html")
with open(src_gui, 'r', encoding='utf-8') as f:
    gui_raw = f.read()

# Apply patches exactly ONCE on clean text
if "</style>" in gui_raw:
    gui_raw = gui_raw.replace("</style>", minimal_glossary_style + "\n    </style>")
    
gui_raw = gui_raw.replace("정척 레일을", '<span class="term-highlight" onclick="openGlossary(\'standard_rail\')">정척레일</span>을', 1)
gui_raw = gui_raw.replace("장대레일로 1차", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span>로 1차', 1)
gui_raw = gui_raw.replace("장대레일 반출", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span> 반출', 1)
gui_raw = gui_raw.replace("가스압접/플래시버트 용접하기", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접</span>/<span class="term-highlight" onclick="openGlossary(\'flash_butt\')">플래시버트 용접</span>하기', 1)
gui_raw = gui_raw.replace("가스압접/플래시버트 용접용", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접</span>/<span class="term-highlight" onclick="openGlossary(\'flash_butt\')">플래시버트 용접</span>용', 1)
gui_raw = gui_raw.replace("가스압접/플래시버트 용접 및", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접</span>/<span class="term-highlight" onclick="openGlossary(\'flash_butt\')">플래시버트 용접</span> 및', 1)

gui_raw = gui_raw.replace("비파괴 검사장", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴 검사(NDT)장</span>', 1)
gui_raw = gui_raw.replace("비파괴검사(초음파/자분)", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴검사(NDT)</span>', 1)
gui_raw = gui_raw.replace("비파괴 시험(UT/MT)", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴 시험(NDT)</span>', 1)

# Scene links
gui_raw = gui_raw.replace("용접장 입지 검토", '용접장 입지 검토 <span class="scene-link" onclick="openScene(\'yard\')">📸 용접장 전경 보기</span>', 1)
gui_raw = gui_raw.replace("버(Burr) 전단", '버(Burr) 전단 <span class="scene-link" onclick="openScene(\'flash_butt\')">📸 용접 과정 보기</span>', 1)
gui_raw = gui_raw.replace("장대레일 반출", '장대레일 반출 <span class="scene-link" onclick="openScene(\'launching\')">📸 인입(Launching) 보기</span>', 1)

if "</body>" in gui_raw:
    gui_raw = gui_raw.replace("</body>", common_modal_html + "\n</body>")

gui_fn1 = os.path.join(target_base, "수행지침", "레일 용접장 선정_수행지침.html")
gui_fn2 = os.path.join(target_base, "수행지침", "3_레일 용접장 선정_수행지침.html")

with open(gui_fn1, 'w', encoding='utf-8') as f:
    f.write(gui_raw)
with open(gui_fn2, 'w', encoding='utf-8') as f:
    f.write(gui_raw)
print("🎉 Re-written Guideline HTML files cleanly.")

# 3. Compile Checklist HTML
src_chk = os.path.join(backup_base, "체크리스트", "레일 용접장 선정_체크리스트.html")
with open(src_chk, 'r', encoding='utf-8') as f:
    chk_raw = f.read()

# Apply risk bullet formatting first
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

chk_raw = re.sub(pre_pattern, pre_repl, chk_raw, flags=re.DOTALL)
chk_raw = re.sub(ing_pattern, ing_repl, chk_raw, flags=re.DOTALL)
chk_raw = re.sub(post_pattern, post_repl, chk_raw, flags=re.DOTALL)

# Append style
if "</style>" in chk_raw:
    chk_raw = chk_raw.replace("</style>", minimal_glossary_style + "\n    </style>")
    
# Inject highlights
chk_raw = chk_raw.replace("장대레일 제작 시", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span> 제작 시', 1)
chk_raw = chk_raw.replace("장대레일 영구", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span> 영구', 1)
chk_raw = chk_raw.replace("비파괴 시험(UT/MT)", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴 시험(NDT)</span>', 1)
chk_raw = chk_raw.replace("NDT 용접부", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">NDT 용접부</span>', 1)

# Inject scene links
chk_raw = chk_raw.replace("수평 오차 초과로", '수평 오차 초과로 <span class="scene-link" onclick="openScene(\'yard\')">📸 롤러 가이드 베드 보기</span>', 1)

if "</body>" in chk_raw:
    chk_raw = chk_raw.replace("</body>", common_modal_html + "\n</body>")

chk_fn1 = os.path.join(target_base, "체크리스트", "레일 용접장 선정_체크리스트.html")
chk_fn2 = os.path.join(target_base, "체크리스트", "3_레일 용접장 선정_체크리스트.html")

with open(chk_fn1, 'w', encoding='utf-8') as f:
    f.write(chk_raw)
with open(chk_fn2, 'w', encoding='utf-8') as f:
    f.write(chk_raw)
print("🎉 Re-written Checklist HTML files cleanly.")

print("\n🎉 ALL WELDING YARD HTML FILES RE-CREATED PERFECTLY WITH ZERO DUPLICATIONS!")
