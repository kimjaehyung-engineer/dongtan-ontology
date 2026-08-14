# -*- coding: utf-8 -*-
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client

os.system('taskkill /f /im excel.exe 2>nul')

excel = win32com.client.Dispatch('Excel.Application')
excel.Visible = False
excel.DisplayAlerts = False

test_p = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\test_dynamic.xlsx")
if os.path.exists(test_p):
    os.remove(test_p)

wb = excel.Workbooks.Add()
ws = wb.ActiveSheet
wb.SaveAs(test_p)

rel_sub = r"매뉴얼BODY(집행단계-첨부폴더)v8\4.상부강화노반\1_지반조사 상세검토\표준서\지반조사 상세검토_표준서.html"

# 1. Dynamic Formula
ws.Range("A1").Formula = f'=HYPERLINK(LEFT(CELL("filename",A1),FIND("[",CELL("filename",A1))-1)&"{rel_sub}", "[클릭] 동적 표준서 열기")'

# 2. Direct Absolute Path Formula
full_path = os.path.abspath(os.path.join(os.path.dirname(test_p), rel_sub))
ws.Range("A2").Formula = f'=HYPERLINK("{full_path}", "[클릭] 절대경로 표준서 열기")'

wb.Save()

print("Cell A1 Formula:", ws.Range("A1").Formula)
print("Cell A1 Text:", ws.Range("A1").Text)
print("Cell A2 Formula:", ws.Range("A2").Formula)
print("Cell A2 Text:", ws.Range("A2").Text)

wb.Close(False)
excel.Quit()
print("Success!")
