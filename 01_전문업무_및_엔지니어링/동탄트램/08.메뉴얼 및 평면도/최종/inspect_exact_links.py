import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼 BODY (집행단계).xlsx"
wb = openpyxl.load_workbook(excel_path)
ws = wb['사전토공사']

row2 = list(ws.iter_rows())[1] # row index 1 is row 2
col_std = row2[10] # 11th column
col_gui = row2[11] # 12th column
col_chk = row2[12] # 13th column

print("--- Row 2 표준서 ---")
print("Value:\n", repr(col_std.value))
print("Hyperlink target:", col_std.hyperlink.target if col_std.hyperlink else None)

print("\n--- Row 2 수행지침 ---")
print("Value:\n", repr(col_gui.value))
print("Hyperlink target:", col_gui.hyperlink.target if col_gui.hyperlink else None)

print("\n--- Row 2 체크리스트 ---")
print("Value:\n", repr(col_chk.value))
print("Hyperlink target:", col_chk.hyperlink.target if col_chk.hyperlink else None)
