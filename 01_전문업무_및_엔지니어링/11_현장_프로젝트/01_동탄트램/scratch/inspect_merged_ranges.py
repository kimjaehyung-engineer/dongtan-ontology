import os, sys, openpyxl

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보'

f1 = os.path.join(base_dir, '03_기술제안 1공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx')

wb1 = openpyxl.load_workbook(f1, data_only=True)
ws1 = wb1.active

print("=== Merged Cell Ranges and Values in 1공구 Sheet ===")
for m_range in ws1.merged_cells.ranges:
    top_left = ws1.cell(row=m_range.min_row, column=m_range.min_col)
    val = top_left.value
    if val and ('구간' in str(val) or '부지' in str(val)):
        print(f"Range: {m_range.coord:<12} Value: {str(val).strip()}")
