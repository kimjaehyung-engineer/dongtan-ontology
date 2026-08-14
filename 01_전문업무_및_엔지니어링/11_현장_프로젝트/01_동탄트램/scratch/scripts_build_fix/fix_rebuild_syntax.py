# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

rebuild_script_path_brain = r'C:\Users\sskjh\.gemini\antigravity-ide\brain\ad01f031-2691-448a-a014-b07293f68fcf\scratch\rebuild_manual.py'

with open(rebuild_script_path_brain, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 856~857라인의 줄바꿈 에러 수정
bad_replace_block = """    "const descText = document.getElementById('sim-desc-text');
    if (!tram) return;\""""

good_replace_block = '    "const descText = document.getElementById(\'sim-desc-text\');\\n    if (!tram) return;"'

if bad_replace_block in content:
    content = content.replace(bad_replace_block, good_replace_block)
    print("Fixed simulator safety guard string literal.")
else:
    # 혹시 정확히 매치가 안 되는 경우를 대비한 유연한 치환
    print("[WARNING] bad_replace_block exact match failed, trying regex or raw replace...")
    content = content.replace('"const descText = document.getElementById(\'sim-desc-text\');\n    if (!tram) return;"', good_replace_block)

# 2. 1085~1086라인의 join 개행 에러 수정
bad_join_block = """main_content = "\\
".join(ordered_sections)"""

good_join_block = 'main_content = "\\n".join(ordered_sections)'

if bad_join_block in content:
    content = content.replace(bad_join_block, good_join_block)
    print("Fixed main_content join string literal.")
else:
    print("[WARNING] bad_join_block exact match failed, trying raw replace...")
    # 혹시 문자열이 다르게 깨졌을 수 있음
    content = content.replace('main_content = "\\\n".join(ordered_sections)', good_join_block)
    content = content.replace('main_content = "\\n".join(ordered_sections)', good_join_block)

with open(rebuild_script_path_brain, 'w', encoding='utf-8') as f:
    f.write(content)

print("Syntax fix complete!")
