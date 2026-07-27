import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

backup_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\메일송부(0723)\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"
target_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"

from patch_welding_surgical import minimal_glossary_style
from implement_welding_glossary_interactive import common_modal_html

# Re-read and rewrite clean guidelines WITHOUT the redundant "용접 과정 보기" button
src_gui = os.path.join(backup_base, "수행지침", "레일 용접장 선정_수행지침.html")
with open(src_gui, 'r', encoding='utf-8') as f:
    gui_raw = f.read()

# Apply patches exactly ONCE
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

# Scene links - EXCLUDED "용접 과정 보기" button
gui_raw = gui_raw.replace("용접장 입지 검토", '용접장 입지 검토 <span class="scene-link" onclick="openScene(\'yard\')">📸 용접장 전경 보기</span>', 1)
# REMOVED: gui_raw = gui_raw.replace("버(Burr) 전단", ...)
gui_raw = gui_raw.replace("장대레일 반출", '장대레일 반출 <span class="scene-link" onclick="openScene(\'launching\')">📸 인입(Launching) 보기</span>', 1)

if "</body>" in gui_raw:
    gui_raw = gui_raw.replace("</body>", common_modal_html + "\n</body>")

gui_fn1 = os.path.join(target_base, "수행지침", "레일 용접장 선정_수행지침.html")
gui_fn2 = os.path.join(target_base, "수행지침", "3_레일 용접장 선정_수행지침.html")

with open(gui_fn1, 'w', encoding='utf-8') as f:
    f.write(gui_raw)
with open(gui_fn2, 'w', encoding='utf-8') as f:
    f.write(gui_raw)

print("🎉 Successfully deleted '📸 용접 과정 보기' button from guideline files!")
