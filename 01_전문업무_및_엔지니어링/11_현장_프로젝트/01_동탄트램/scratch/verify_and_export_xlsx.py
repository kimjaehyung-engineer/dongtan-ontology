# -*- coding: utf-8 -*-
import os, sys, win32com.client

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)")
TARGET_XLSM = os.path.join(BASE_DIR, "매뉴얼 BODY (집행단계)v8.xlsm")
TARGET_XLSX = os.path.join(BASE_DIR, "매뉴얼 BODY (집행단계)v8.xlsx")

excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

try:
    wb = excel.Workbooks.Open(TARGET_XLSM)
    ws = wb.Sheets("사전토공사")
    print("=== v8.xlsm 사전토공사 O, Q, S열 텍스트 및 링크 확인 ===")
    for r in range(2, 6):
        h = ws.Cells(r, 8).Value
        o_txt = ws.Cells(r, 15).Text
        q_txt = ws.Cells(r, 17).Text
        s_txt = ws.Cells(r, 19).Text
        print(f"Row {r} [{h}]:")
        print(f"  O열 Text: '{o_txt}'")
        print(f"  Q열 Text: '{q_txt}'")
        print(f"  S열 Text: '{s_txt}'")
        
    # v8.xlsx로도 깨끗하게 저장 (xlOpenXMLWorkbook = 51)
    if os.path.exists(TARGET_XLSX):
        os.remove(TARGET_XLSX)
    wb.SaveCopyAs(TARGET_XLSX) # or SaveAs with format 51
    wb.Close(SaveChanges=False)

    wb_x = excel.Workbooks.Open(TARGET_XLSM)
    wb_x.SaveAs(TARGET_XLSX, FileFormat=51) # 51 = xlsx
    wb_x.Close()
    print("v8.xlsx 변환 저장 완료!")

finally:
    excel.Quit()
