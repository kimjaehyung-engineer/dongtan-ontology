import openpyxl
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼 BODY (집행단계).xlsx"
wb = openpyxl.load_workbook(excel_path, data_only=True)

ws = wb['상부강화노반']
rows = list(ws.iter_rows(values_only=True))

headers = [str(h).strip() if h is not None else "" for h in rows[0]]
row1 = list(rows[1])

data = {}
for h, val in zip(headers, row1):
    data[h] = str(val) if val is not None else ""

print(json.dumps(data, ensure_ascii=False, indent=2))
