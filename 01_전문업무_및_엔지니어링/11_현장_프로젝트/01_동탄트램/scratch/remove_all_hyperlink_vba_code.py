# -*- coding: utf-8 -*-
"""
매뉴얼 BODY (집행단계)v8.xlsm 및 v8.xlsx 내 모든 하이퍼링크 관련 VBA 매크로 코드 완전 삭제 스크립트
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client
import pythoncom

XLSM_PATH = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼 BODY (집행단계)v8.xlsm")
XLSX_PATH = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼 BODY (집행단계)v8.xlsx")

print("1. Excel COM API를 가동하여 v8.xlsm 내 모든 VBA 매크로 코드 삭제 시작...")

pythoncom.CoInitialize()
excel = win32com.client.DispatchEx("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

wb = excel.Workbooks.Open(XLSM_PATH)

try:
    vb_proj = wb.VBProject
    print(f"VBA 프로젝트: {vb_proj.Name}")

    # 1. 표준 모듈 (LinkOpener 등) 삭제
    for comp in list(vb_proj.VBComponents):
        if comp.Type == 1:  # vbext_ct_StdModule
            print(f"표준 모듈 삭제: {comp.Name}")
            vb_proj.VBComponents.Remove(comp)
        elif comp.Type in [100, 2]:  # Sheet, ThisWorkbook, Class
            code_mod = comp.CodeModule
            cnt = code_mod.CountOfLines
            if cnt > 0:
                print(f"시트/통합문서 내 매크로 코드 전면 삭제: {comp.Name} ({cnt} 줄 삭제)")
                code_mod.DeleteLines(1, cnt)

    wb.Save()
    print("✓ v8.xlsm 내 모든 VBA 매크로 코드 100% 완전 삭제 완료!")

    # 2. 순수 XLSX로도 내보내기 (매크로 완전 제거 포맷 51)
    wb.SaveAs(XLSX_PATH, FileFormat=51)
    print("✓ v8.xlsx (매크로 없는 순수 엑셀) 동기화 완료!")

except Exception as e:
    print(f"오류 발생: {e}")
finally:
    wb.Close(SaveChanges=True)
    excel.Quit()
    pythoncom.CoUninitialize()

print("\n=======================================================")
print("엑셀 하이퍼링크 관련 모든 VBA 코드 완전 삭제 완료!")
print("=======================================================")
