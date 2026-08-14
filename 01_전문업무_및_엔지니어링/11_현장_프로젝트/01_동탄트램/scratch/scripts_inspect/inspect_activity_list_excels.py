import sys, openpyxl
sys.stdout.reconfigure(encoding='utf-8')

path1 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보\06_기술제안 1공구 예정공정표 Activity List_(주)천우씨엠_260806.xlsx'
path2 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보\06_기술제안 2공구 예정공정표 Activity List_(주)천우씨엠_260806_rev2_교차로 명칭 수정.xlsx'

for label, p in [("1공구 Activity List", path1), ("2공구 Activity List", path2)]:
    print(f"\n========================================")
    print(f"=== {label} ===")
    print(f"========================================")
    wb = openpyxl.load_workbook(p, data_only=True)
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        print(f"\n--- Sheet: {sheet} (rows={ws.max_row}, cols={ws.max_column}) ---")
        for r in range(1, min(ws.max_row + 1, 40)):
            row_vals = []
            for c in range(1, min(ws.max_column + 1, 15)):
                val = ws.cell(row=r, column=c).value
                row_vals.append(str(val) if val is not None else "")
            if any(row_vals):
                print(f"  Row {r:3d}: {' | '.join(row_vals)}")
    wb.close()
