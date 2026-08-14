import openpyxl, os, sys

sys.stdout.reconfigure(encoding='utf-8')

f1 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\03_기술제안 1공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx'

wb = openpyxl.load_workbook(f1, data_only=True)
ws = wb.active

print(f"=== Inspecting Excel Sheet '{ws.title}' Columns & Headers ===")

for r in range(1, 15):
    row_vals = [ws.cell(r, c).value for c in range(1, 10)]
    if any(row_vals):
        print(f"Row {r:2d}: {row_vals}")
