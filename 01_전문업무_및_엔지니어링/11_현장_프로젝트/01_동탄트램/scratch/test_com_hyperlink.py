# -*- coding: utf-8 -*-
"""
Excel COM 자동화로 테스트 하이퍼링크 생성
- openpyxl이 아닌 Excel 자체 엔진으로 하이퍼링크 주입
- 이 방식이 되면 본 파일에도 동일 적용
"""
import win32com.client
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")

# Excel 인스턴스 생성
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

base = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)")
test_file = os.path.join(base, "링크테스트.xlsx")

# 기존 테스트 파일 삭제 후 새로 생성
if os.path.exists(test_file):
    os.remove(test_file)

wb = excel.Workbooks.Add()
ws = wb.Sheets(1)
ws.Name = "테스트"

# 컬럼 너비
ws.Columns("A:A").ColumnWidth = 70

# 실제 존재하는 HTML 경로
html_short = os.path.join(base, "test_link.html")
html_long = os.path.join(base, 
    "매뉴얼BODY(집행단계-첨부폴더)v8", "8.전기분야", 
    "1_설계적정성 검토", "표준서", "설계적정성 검토_표준서.html")

print(f"짧은 경로 존재: {os.path.exists(html_short)} -> {html_short}")
print(f"긴 경로 존재: {os.path.exists(html_long)} -> {html_long}")

# TEST 1: COM API Hyperlinks.Add - 짧은 경로
ws.Cells(1, 1).Value = "TEST1: COM Hyperlinks.Add - 짧은 절대경로"
cell1 = ws.Cells(2, 1)
ws.Hyperlinks.Add(Anchor=cell1, Address=html_short, TextToDisplay="[클릭] 짧은경로 HTML 열기")

# TEST 2: COM API Hyperlinks.Add - 긴 한글 경로  
ws.Cells(4, 1).Value = "TEST2: COM Hyperlinks.Add - 긴 한글 절대경로"
cell2 = ws.Cells(5, 1)
ws.Hyperlinks.Add(Anchor=cell2, Address=html_long, TextToDisplay="[클릭] 전기분야 표준서 열기")

# TEST 3: COM Formula - HYPERLINK 수식
ws.Cells(7, 1).Value = "TEST3: COM Formula =HYPERLINK()"
ws.Cells(8, 1).Formula = f'=HYPERLINK("{html_long}","[클릭] 수식방식 열기")'

# 저장 (xlOpenXMLWorkbook = 51)
wb.SaveAs(test_file, FileFormat=51)
wb.Close()
excel.Quit()

print(f"\n테스트 파일 저장 완료: {test_file}")
print("이 파일 열고 TEST1, TEST2, TEST3 각각 클릭해보세요!")
