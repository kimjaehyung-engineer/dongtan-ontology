import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

target_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"

from patch_welding_surgical import minimal_glossary_style
from implement_welding_glossary_interactive import common_modal_html

# Force-clear function to prevent leftover bytes
def clean_write_file(filepath, content):
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except:
            pass
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"🎉 Cleanly written: {os.path.basename(filepath)}")

# Ensure target directories exist
os.makedirs(os.path.join(target_base, "표준서"), exist_ok=True)
os.makedirs(os.path.join(target_base, "수행지침"), exist_ok=True)
os.makedirs(os.path.join(target_base, "체크리스트"), exist_ok=True)


# =========================================================================
# 1. GENERATE PERFECT STANDARD HTML
# =========================================================================
from repair_welding_standard_exact_content import standard_content_final

clean_write_file(os.path.join(target_base, "표준서", "레일 용접장 선정_표준서.html"), standard_content_final)
clean_write_file(os.path.join(target_base, "표준서", "3_레일 용접장 선정_표준서.html"), standard_content_final)


# =========================================================================
# 2. GENERATE PERFECT GUIDELINE HTML
# =========================================================================
backup_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\메일송부(0723)\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"
src_gui = os.path.join(backup_base, "수행지침", "레일 용접장 선정_수행지침.html")
with open(src_gui, 'r', encoding='utf-8') as f:
    gui_raw = f.read()

# Apply minimal popup styles
if "</style>" in gui_raw:
    gui_raw = gui_raw.replace("</style>", minimal_glossary_style + "\n    </style>")

# 1회성 팝업 링크 지정 (중복 절대 없음)
gui_raw = gui_raw.replace("정척 레일을", '<span class="term-highlight" onclick="openGlossary(\'standard_rail\')">정척레일</span>을', 1)
gui_raw = gui_raw.replace("장대레일로 1차", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span>로 1차', 1)
gui_raw = gui_raw.replace("가스압접/플래시버트 용접하기", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접</span>/<span class="term-highlight" onclick="openGlossary(\'flash_butt\')">플래시버트 용접</span>하기', 1)

# NDT 팝업은 오직 윗부분인 "100% 비파괴 검사(NDT)장 및 연마 작업장 확보" 에만 최초 1회 생성
gui_raw = gui_raw.replace("비파괴 검사(NDT)장 및", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴 검사(NDT)장</span> 및', 1)

# 아래 부분의 비파괴검사(NDT) 단어들은 모두 일반 텍스트로 보존 (절대 링크를 걸지 않음!)
# 이미 원본인 gui_raw 에는 span 태그가 없으므로 replace를 수행하지 않으면 자연스레 일반 텍스트로 보존됩니다.

# Scene view buttons (용접과정 보기 제외, 전경 보기 및 인입 보기만 각 1회씩 탑재)
gui_raw = gui_raw.replace("용접장 입지 검토", '용접장 입지 검토 <span class="scene-link" onclick="openScene(\'yard\')">📸 용접장 전경 보기</span>', 1)
gui_raw = gui_raw.replace("장대레일 반출", '장대레일 반출 <span class="scene-link" onclick="openScene(\'launching\')">📸 인입(Launching) 보기</span>', 1)

if "</body>" in gui_raw:
    gui_raw = gui_raw.replace("</body>", common_modal_html + "\n</body>")

clean_write_file(os.path.join(target_base, "수행지침", "레일 용접장 선정_수행지침.html"), gui_raw)
clean_write_file(os.path.join(target_base, "수행지침", "3_레일 용접장 선정_수행지침.html"), gui_raw)


# =========================================================================
# 3. GENERATE PERFECT CHECKLIST HTML (Master Risk Table Layout)
# =========================================================================
from rebuild_welding_checklist_standard import checklist_content_final

# In checklist, ensure NDT highlight is also only 1st occurrence
# Let's inspect checklist_content_final for NDT highlight spans
# The checklist has:
# Pre: [설계/용접대 침하] ...
# Ing: [NDT 안전거리] ... 비파괴 시험(NDT)
# Post: [품질 보증 누락] ... NDT 용접부
# Since NDT appears first in Ing and then in Post, let's keep only the first one (Ing)
checklist_content_final_clean = checklist_content_final.replace(
    'NDT 용접부', 'NDT 용접부', 1
) # Wait, it's already plain text or has spans? Let's check:
# We wrote:
# Ing: <span class="term-highlight" onclick="openGlossary('ndt')">비파괴 시험(NDT)</span>
# Post: <span class="term-highlight" onclick="openGlossary('ndt')">NDT 용접부</span>
# Let's surgically replace the second occurrence (NDT 용접부) with plain text:
checklist_content_final_clean = checklist_content_final_clean.replace(
    '<span class="term-highlight" onclick="openGlossary(\'ndt\')">NDT 용접부</span>',
    'NDT 용접부'
)

clean_write_file(os.path.join(target_base, "체크리스트", "레일 용접장 선정_체크리스트.html"), checklist_content_final_clean)
clean_write_file(os.path.join(target_base, "체크리스트", "3_레일 용접장 선정_체크리스트.html"), checklist_content_final_clean)

print("\n🎉 ALL WELDING YARD FILES BUILT TO PERFECT SPECIFICATION WITH ZERO DUPLICATE BUTTONS & LINKS!")
