# -*- coding: utf-8 -*-
import os
import sys
import win32com.client

os.system('taskkill /f /im excel.exe 2>nul')

excel = win32com.client.Dispatch('Excel.Application')
excel.Visible = False
excel.DisplayAlerts = False

test_p = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\test_diag.xlsx")
wb = excel.Workbooks.Add()
ws = wb.ActiveSheet

html_abs = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\4.상부강화노반\1_지반조사 상세검토\표준서\지반조사 상세검토_표준서.html")
html_url = "file:///" + html_abs.replace('\\', '/')

print("html_abs:", html_abs)
print("html_url:", html_url)
print("File exists:", os.path.exists(html_abs))

# 1. Formula with file:/// URL
ws.Range("A1").Formula = f'=HYPERLINK("{html_url}", "1. URL file:/// 방식")'

# 2. Formula with Absolute Path
ws.Range("A2").Formula = f'=HYPERLINK("{html_abs}", "2. 절대경로 방식")'

# 3. Native COM with file:/// URL
ws.Hyperlinks.Add(Anchor=ws.Range("A3"), Address=html_url, TextToDisplay="3. COM Native file:/// 방식")

# 4. Native COM with Absolute Path
ws.Hyperlinks.Add(Anchor=ws.Range("A4"), Address=html_abs, TextToDisplay="4. COM Native 절대경로 방식")

# Set Hyperlink Base property
wb.BuiltinDocumentProperties("Hyperlink base").Value = os.path.dirname(test_p)

if os.path.exists(test_p):
    os.remove(test_p)

wb.SaveAs(test_p)
wb.Close(False)
excel.Quit()

print("Saved test_diag.xlsx successfully!")
