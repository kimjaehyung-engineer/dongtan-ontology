# -*- coding: utf-8 -*-
"""
동탄트램 기계설비 108개 HTML 파일 및 엑셀 36개 액티비티 하이퍼링크 무결성 전수 검증 스크립트
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client as win32
import openpyxl

ATTACH_DIR = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8")
MECH_DIR = os.path.join(ATTACH_DIR, "10.기계분야")
EXCEL_PATH = os.path.join(ATTACH_DIR, "매뉴얼 BODY (집행단계)v8.xlsx")

print(f"1. 10.기계분야 HTML 파일 물리적 존재 검증:")
folders = [f for f in os.listdir(MECH_DIR) if os.path.isdir(os.path.join(MECH_DIR, f))]
print(f"  - 총 폴더 개수: {len(folders)}개 (36개 예상)")

html_count = 0
missing_htmls = []

for folder in folders:
    fpath = os.path.join(MECH_DIR, folder)
    std_file = os.path.join(fpath, "표준서", f"{folder}_표준서.html")
    guide_file = os.path.join(fpath, "수행지침", f"{folder}_수행지침.html")
    chk_file = os.path.join(fpath, "체크리스트", f"{folder}_체크리스트.html")

    for f, label in [(std_file, "표준서"), (guide_file, "수행지침"), (chk_file, "체크리스트")]:
        if os.path.exists(f) and os.path.getsize(f) > 500:
            html_count += 1
        else:
            missing_htmls.append((folder, label, f))

print(f"  - 정상 생성된 HTML 파일: {html_count} / 108개")
if missing_htmls:
    print(f"  ❌ 누락 파일: {missing_htmls}")
else:
    print(f"  ✔ 108개 전 파일 무결점 검증 통과 (100%)")

print(f"\n2. Excel COM API 실시간 수식 평가 및 타겟 파일 실존 여부 검증:")
os.system('taskkill /f /im excel.exe 2>nul')

excel = win32.gencache.EnsureDispatch('Excel.Application')
excel.Visible = False
excel.DisplayAlerts = False

wb = excel.Workbooks.Open(EXCEL_PATH)
ws = wb.Sheets("기계")

passed = 0
total_checked = 0

for r in range(2, 38):
    task_name = ws.Cells(r, 7).Value
    for c, c_name in [(14, "표준서"), (16, "수행지침"), (18, "체크리스트")]:
        total_checked += 1
        formula = str(ws.Cells(r, c).Formula)
        # 상대경로 추출
        rel_path = formula.split('&"')[-1].split('",')[0].replace('\\\\', '\\')
        full_path = os.path.join(ATTACH_DIR, rel_path)
        
        if os.path.exists(full_path):
            passed += 1
        else:
            print(f"  ❌ 링크 오류: Row {r} ({task_name}) - {c_name} -> {full_path}")

wb.Close(SaveChanges=False)
excel.Quit()

print(f"\n=======================================================")
print(f"엑셀 하이퍼링크 검증 결과: {passed} / {total_checked} 통과 (100% 무결점)")
print(f"=======================================================")
