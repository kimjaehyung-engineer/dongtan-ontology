# -*- coding: utf-8 -*-
import os
import sys
import win32com.client

# Kill any stuck EXCEL processes
os.system('taskkill /f /im excel.exe 2>nul')

excel = win32com.client.Dispatch('Excel.Application')
excel.Visible = False
excel.DisplayAlerts = False

wb_test = excel.Workbooks.Add()
ws = wb_test.ActiveSheet

test_html = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\4.상부강화노반\1_지반조사 상세검토\표준서\지반조사 상세검토_표준서.html")
rel_path = r"매뉴얼BODY(집행단계-첨부폴더)v8\4.상부강화노반\1_지반조사 상세검토\표준서\지반조사 상세검토_표준서.html"

# 1. COM Native Relative Link
c1 = ws.Range("A1")
ws.Hyperlinks.Add(Anchor=c1, Address=rel_path, TextToDisplay="COM 상대경로 링크")

# 2. COM Native Absolute Link
c2 = ws.Range("A2")
ws.Hyperlinks.Add(Anchor=c2, Address=test_html, TextToDisplay="COM 절대경로 링크")

# 3. Formula Link
c3 = ws.Range("A3")
c3.Formula = f'=HYPERLINK("{rel_path}", "수식 상대경로 링크")'

test_save_path = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\test_link.xlsx")
if os.path.exists(test_save_path):
    os.remove(test_save_path)

wb_test.SaveAs(test_save_path)
wb_test.Close(False)
excel.Quit()

print("Test file created successfully at:", test_save_path)
