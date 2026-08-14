import openpyxl

excel_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼 BODY (집행단계)v4.xlsx'

wb = openpyxl.load_workbook(excel_path, data_only=False)

print("=== 엑셀 v4 내 전체 시트 목록 ===")
for idx, s in enumerate(wb.sheetnames, 1):
    print(f"{idx:2d}. {s}")
