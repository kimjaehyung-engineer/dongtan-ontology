import os, sys, openpyxl

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보'

f1 = os.path.join(base_dir, '03_기술제안 1공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx')
f2 = os.path.join(base_dir, '03_기술제안 2공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx')

wb1 = openpyxl.load_workbook(f1, data_only=True)
ws1 = wb1.active

print("=== OpenPyXL 1공구 Merged & Unmerged Cells Inspection ===")
for r in range(11, 43):
    sec = ws1.cell(row=r, column=3).value
    split13 = ws1.cell(row=r, column=14).value
    split14 = ws1.cell(row=r, column=15).value
    split15 = ws1.cell(row=r, column=16).value
    split16 = ws1.cell(row=r, column=17).value
    print(f"Row {r:2d}: sec={str(sec):<25} col14={split13} col15={split14} col16={split15} col17={split16}")
