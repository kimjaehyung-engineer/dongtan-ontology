# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

rebuild_script_path_brain = r'C:\Users\sskjh\.gemini\antigravity-ide\brain\ad01f031-2691-448a-a014-b07293f68fcf\scratch\rebuild_manual.py'

with open(rebuild_script_path_brain, 'r', encoding='utf-8') as f:
    content = f.read()

# 2개 카드 제거 로직 삽입 대상 지정
target_line = "# 밋밋한 표 치환"

insertion_code = """# 궤도 인터랙티브 대시보드 내의 중복 카드(1공구/2공구 상세 제원) 제거
    card_start_str = '<!-- Section 1 Details -->'
    idx_card_start = ch6_content.find(card_start_str)
    if idx_card_start != -1:
        # 2공구 상세 제원의 끝 </div> 를 찾음
        idx_card2_header = ch6_content.find('2공구 상세 제원', idx_card_start)
        if idx_card2_header != -1:
            idx_card2_table_end = ch6_content.find('</table>', idx_card2_header)
            if idx_card2_table_end != -1:
                # table 뒤에 오는 </div> 닫기 2개를 건너뜀
                idx_card2_div_end = ch6_content.find('</div>', idx_card2_table_end) + len('</div>') # space-y-4 끝
                idx_card2_card_end = ch6_content.find('</div>', idx_card2_div_end) + len('</div>') # card 끝
                
                # 해당 영역을 완전히 제거
                ch6_content = ch6_content[:idx_card_start] + ch6_content[idx_card2_card_end:]
                print("Duplicate orbital spec cards removed from dashboard successfully!")
            else:
                print("[ERROR] 2공구 table end not found!")
        else:
            print("[ERROR] 2공구 header not found!")
    else:
        print("[WARNING] Section 1 Details not found in dashboard!")
"""

patched_content = content.replace(target_line, insertion_code + "\n    " + target_line)

with open(rebuild_script_path_brain, 'w', encoding='utf-8') as f:
    f.write(patched_content)

print("Patching duplicate cards removal logic complete!")
