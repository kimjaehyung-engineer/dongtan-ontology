import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼 BODY (집행단계).xlsx"
wb = openpyxl.load_workbook(excel_path)

sheets = ['상부강화노반', '콘크리트도상', '건축', '신호분야', '통신분야', '전기분야']

for sheet_name in sheets:
    ws = wb[sheet_name]
    rows = list(ws.iter_rows())
    header_vals = [str(c.value).strip() if c.value else "" for c in rows[0]]
    
    col_map = {h: i for i, h in enumerate(header_vals)}
    print(f"\n=== Sheet: {sheet_name} (Total rows: {len(rows)}) ===")
    
    # Print sample row 2 (first data row)
    r2 = rows[1]
    std_val = r2[col_map.get('표준서 (Standard)\n[정량적 절대 기술 기준]', 10)].value
    gui_val = r2[col_map.get('수행지침 (Guideline)\n[작업 절차 및 주의사항]', 11)].value
    chk_val = r2[col_map.get('체크리스트 (Checklist)\n[완료 검측 표준]', 12)].value
    
    print("  Row 2 표준서:\n", repr(std_val)[:150])
    print("  Row 2 수행지침:\n", repr(gui_val)[:150])
    print("  Row 2 체크리스트:\n", repr(chk_val)[:150])
