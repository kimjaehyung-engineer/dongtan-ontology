import sys, openpyxl
sys.stdout.reconfigure(encoding='utf-8')

path1 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보\06_기술제안 1공구 예정공정표 Activity List_(주)천우씨엠_260806.xlsx'
wb = openpyxl.load_workbook(path1, data_only=True)
ws = wb.active
print("First 10 rows of 1공구 Activity List:")
for r in range(1, 15):
    vals = [str(ws.cell(row=r, column=c).value) for c in range(1, 8)]
    print(f"Row {r}: {vals}")
wb.close()
