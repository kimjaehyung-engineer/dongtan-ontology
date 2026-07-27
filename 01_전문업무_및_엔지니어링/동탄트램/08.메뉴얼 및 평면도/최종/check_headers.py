import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼 BODY (집행단계).xlsx"
wb = openpyxl.load_workbook(excel_path)
ws = wb['상부강화노반']

print("Headers in 상부강화노반:")
for i, cell in enumerate(ws[1]):
    print(f"Col {i+1} ({cell.coordinate}): {repr(cell.value)}")
