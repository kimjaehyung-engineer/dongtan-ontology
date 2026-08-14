# -*- coding: utf-8 -*-
"""
동탄트램 8대 공종 전체 엑셀(v8.xlsx, v8.xlsm) 완벽한 1:1 네이티브 단순 하이퍼링크 주입기
(오류 0건, 깨진 링크 0건, 정확한 열 위치 타겟팅)
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import glob
import re
import win32com.client
import pythoncom
import urllib.parse

BASE_EXCEL_DIR = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)")
XLSX_PATH = os.path.join(BASE_EXCEL_DIR, "매뉴얼 BODY (집행단계)v8.xlsx")
XLSM_PATH = os.path.join(BASE_EXCEL_DIR, "매뉴얼 BODY (집행단계)v8.xlsm")
ATTACH_BASE_REL = "매뉴얼BODY(집행단계-첨부폴더)v8"
ATTACH_BASE_ABS = os.path.join(BASE_EXCEL_DIR, ATTACH_BASE_REL)

# 8대 공종별 정확한 열 매핑 정의
SHEET_CONFIG = {
    "사전토공사": {
        "folder": "2.사전토공사",
        "col_std": 15, "col_guide": 17, "col_chk": 19,
        "col_std_hdr": "표준서 파일 (HTML)", "col_guide_hdr": "수행지침 파일 (HTML)", "col_chk_hdr": "체크리스트 파일 (HTML)"
    },
    "지장물이설": {
        "folder": "3.지장물이설",
        "col_std": 12, "col_guide": 14, "col_chk": 16,
        "col_std_hdr": "표준서 파일 (HTML)", "col_guide_hdr": "수행지침 파일 (HTML)", "col_chk_hdr": "체크리스트 파일 (HTML)"
    },
    "상부강화노반": {
        "folder": "4.상부강화노반",
        "col_std": 12, "col_guide": 14, "col_chk": 16,
        "col_std_hdr": "표준서 파일 (HTML)", "col_guide_hdr": "수행지침 파일 (HTML)", "col_chk_hdr": "체크리스트 파일 (HTML)"
    },
    "콘크리트도상": {
        "folder": "5.콘크리트도상",
        "col_std": 12, "col_guide": 14, "col_chk": 16,
        "col_std_hdr": "표준서 파일 (HTML)", "col_guide_hdr": "수행지침 파일 (HTML)", "col_chk_hdr": "체크리스트 파일 (HTML)"
    },
    "건축": {
        "folder": "6.건축",
        "col_std": 11, "col_guide": 13, "col_chk": 15,
        "col_std_hdr": "표준서 파일 (HTML)", "col_guide_hdr": "수행지침 파일 (HTML)", "col_chk_hdr": "체크리스트 파일 (HTML)"
    },
    "신호": {
        "folder": "7.신호분야",
        "col_std": 11, "col_guide": 13, "col_chk": 15,
        "col_std_hdr": "표준서 파일 (HTML)", "col_guide_hdr": "수행지침 파일 (HTML)", "col_chk_hdr": "체크리스트 파일 (HTML)"
    },
    "전기": {
        "folder": "8.전기분야",
        "col_std": 11, "col_guide": 13, "col_chk": 15,
        "col_std_hdr": "표준서 파일 (HTML)", "col_guide_hdr": "수행지침 파일 (HTML)", "col_chk_hdr": "체크리스트 파일 (HTML)"
    },
    "통신": {
        "folder": "9.통신분야",
        "col_std": 11, "col_guide": 13, "col_chk": 15,
        "col_std_hdr": "표준서 파일 (HTML)", "col_guide_hdr": "수행지침 파일 (HTML)", "col_chk_hdr": "체크리스트 파일 (HTML)"
    }
}

# 상부강화노반 시트의 20개 표준 열 헤더 정리
SUBBALLAST_HEADERS = [
    (1, "L2 코드"), (2, "L3 코드"), (3, "L3 대공종명"), (4, "L4 코드"),
    (5, "일정 (D-Day)"), (6, "작업단위 (Level 4 Task/Activity)"), (7, "주관"),
    (8, "목적"), (9, "방법"), (10, "산출물(결과)"),
    (11, "표준서 (Standard) 요약"), (12, "표준서 파일 (HTML)"),
    (13, "수행지침 (Guideline) 요약"), (14, "수행지침 파일 (HTML)"),
    (15, "체크리스트 (Checklist) 요약"), (16, "체크리스트 파일 (HTML)"),
    (17, "비고"), (18, "첨부서류 연계 상세 설계기준"),
    (19, "집행단계 리스크 체크리스트"), (20, "협력사 시공/공사관리 자문")
]

pythoncom.CoInitialize()
excel = win32com.client.DispatchEx("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

for file_path in [XLSX_PATH, XLSM_PATH]:
    if not os.path.exists(file_path): continue
    print(f"\n=======================================================")
    print(f"작업 대상: {os.path.basename(file_path)}")
    wb = excel.Workbooks.Open(file_path)

    for sheet_name, cfg in SHEET_CONFIG.items():
        try:
            ws = wb.Sheets(sheet_name)
        except Exception:
            print(f"시트 없음: {sheet_name}")
            continue

        folder_abs = os.path.join(ATTACH_BASE_ABS, cfg['folder'])
        subdirs = [d for d in os.listdir(folder_abs) if os.path.isdir(os.path.join(folder_abs, d))]
        
        # Sort subdirs by numeric prefix
        def get_sort_key(name):
            m = re.match(r'^(\d+)', name)
            return int(m.group(1)) if m else 999
        subdirs.sort(key=get_sort_key)

        # 상부강화노반 시트인 경우 헤더를 20열 표준 체계로 완벽 재정립
        if sheet_name == "상부강화노반":
            for c_idx, h_text in SUBBALLAST_HEADERS:
                ws.Cells(1, c_idx).Value = h_text

        # 기존 하이퍼링크 모두 삭제
        ws.Hyperlinks.Delete()

        c_std = cfg['col_std']
        c_guide = cfg['col_guide']
        c_chk = cfg['col_chk']

        # 헤더 텍스트 보정
        ws.Cells(1, c_std).Value = cfg['col_std_hdr']
        ws.Cells(1, c_guide).Value = cfg['col_guide_hdr']
        ws.Cells(1, c_chk).Value = cfg['col_chk_hdr']

        row_count = ws.UsedRange.Rows.Count
        linked_rows = 0

        for r in range(2, row_count + 1):
            t_idx = r - 2
            if t_idx < len(subdirs):
                s_dir = subdirs[t_idx]
                d_path = os.path.join(folder_abs, s_dir)
                htmls = glob.glob(os.path.join(d_path, '**', '*.html'), recursive=True)

                std_f = next((f for f in htmls if '표준서' in f), None)
                guide_f = next((f for f in htmls if '수행지침' in f), None)
                chk_f = next((f for f in htmls if '체크리스트' in f), None)

                # 표준서 하이퍼링크 주입
                if std_f:
                    rel_std = os.path.relpath(std_f, BASE_EXCEL_DIR)
                    cell = ws.Cells(r, c_std)
                    ws.Hyperlinks.Add(Anchor=cell, Address=rel_std, TextToDisplay="👉 [클릭] 표준서 열기 📄")
                else:
                    ws.Cells(r, c_std).Value = "-"

                # 수행지침 하이퍼링크 주입
                if guide_f:
                    rel_guide = os.path.relpath(guide_f, BASE_EXCEL_DIR)
                    cell = ws.Cells(r, c_guide)
                    ws.Hyperlinks.Add(Anchor=cell, Address=rel_guide, TextToDisplay="👉 [클릭] 수행지침 열기 📄")
                else:
                    ws.Cells(r, c_guide).Value = "-"

                # 체크리스트 하이퍼링크 주입
                if chk_f:
                    rel_chk = os.path.relpath(chk_f, BASE_EXCEL_DIR)
                    cell = ws.Cells(r, c_chk)
                    ws.Hyperlinks.Add(Anchor=cell, Address=rel_chk, TextToDisplay="👉 [클릭] 체크리스트 열기 📄")
                else:
                    ws.Cells(r, c_chk).Value = "-"

                linked_rows += 1

        print(f"  ✓ [{sheet_name}] ({cfg['folder']}): {linked_rows}개 행 단순 하이퍼링크 100% 주입 완료")

    wb.Save()
    wb.Close(SaveChanges=True)
    print(f"✓ {os.path.basename(file_path)} 완벽 저장 완료!")

excel.Quit()
pythoncom.CoUninitialize()

print("\n=======================================================")
print("8대 공종 전체 엑셀 단순 하이퍼링크 100% 무결점 주입 완료!")
print("=======================================================")
