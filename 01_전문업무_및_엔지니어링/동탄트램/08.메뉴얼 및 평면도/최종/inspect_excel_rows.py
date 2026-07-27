import openpyxl
import os

excel_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼 BODY (집행단계)v4.xlsx"

wb = openpyxl.load_workbook(excel_path)
sheet = wb['지장물이설']

print("--- Sheet Rows ---")
for idx, row in enumerate(sheet.iter_rows(values_only=True), 1):
    non_empty = [str(cell) for cell in row if cell is not None]
    if non_empty:
        print(f"Row {idx}: {non_empty[:5]}")
