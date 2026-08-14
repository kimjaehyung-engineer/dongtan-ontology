# -*- coding: utf-8 -*-
"""
동탄트램 첨부폴더 8대 공종 HTML 파일과 엑셀 v8.xlsx 및 v8.xlsm 전 공종 1:1 단순 네이티브 하이퍼링크 일괄 연동 스크립트
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import glob
import re
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

BASE_EXCEL_DIR = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)")
XLSX_PATH = os.path.join(BASE_EXCEL_DIR, "매뉴얼 BODY (집행단계)v8.xlsx")
XLSM_PATH = os.path.join(BASE_EXCEL_DIR, "매뉴얼 BODY (집행단계)v8.xlsm")
ATTACH_BASE_REL = "매뉴얼BODY(집행단계-첨부폴더)v8"
ATTACH_BASE_ABS = os.path.join(BASE_EXCEL_DIR, ATTACH_BASE_REL)

# 8대 공종 시트명 및 첨부폴더 매핑
DISCIPLINES = [
    ("사전토공사", "2.사전토공사", "9000-5"),
    ("지장물이설", "3.지장물이설", "2000-1"),
    ("상부강화노반", "4.상부강화노반", "9000-7"),
    ("콘크리트도상", "5.콘크리트도상", "9000-6"),
    ("건축", "6.건축", "9000-4"),
    ("신호", "7.신호분야", "9000-1"),
    ("전기", "8.전기분야", "9000-3"),
    ("통신", "9.통신분야", "9000-2")
]

print("=== 8대 공종 폴더 및 HTML 파일 매핑 인덱싱 시작 ===")

disc_data = {}

for sheet_name, folder_name, wbs_prefix in DISCIPLINES:
    folder_abs = os.path.join(ATTACH_BASE_ABS, folder_name)
    subdirs = [d for d in os.listdir(folder_abs) if os.path.isdir(os.path.join(folder_abs, d))]
    
    task_map = {}
    for d in subdirs:
        # Get task number prefix (e.g. '1_...', '2_...', '36_...')
        m = re.match(r'^(\d+)[._\s]+(.+)$', d)
        t_num = int(m.group(1)) if m else None
        clean_name = m.group(2).strip() if m else d.strip()
        
        d_path = os.path.join(folder_abs, d)
        htmls = glob.glob(os.path.join(d_path, '**', '*.html'), recursive=True)
        
        std_file = next((f for f in htmls if '표준서' in f), None)
        guide_file = next((f for f in htmls if '수행지침' in f), None)
        chk_file = next((f for f in htmls if '체크리스트' in f), None)
        
        task_map[d] = {
            'num': t_num,
            'name': clean_name,
            'folder': d,
            'std': os.path.relpath(std_file, BASE_EXCEL_DIR) if std_file else None,
            'guide': os.path.relpath(guide_file, BASE_EXCEL_DIR) if guide_file else None,
            'chk': os.path.relpath(chk_file, BASE_EXCEL_DIR) if chk_file else None
        }
    
    disc_data[sheet_name] = {
        'folder_name': folder_name,
        'wbs_prefix': wbs_prefix,
        'tasks': task_map
    }
    print(f"[{sheet_name}] ({folder_name}): {len(task_map)}개 액티비티 폴더 인덱싱 완료")

# 이제 win32com을 통해 Excel 네이티브 하이퍼링크 직접 주입
print("\n=== Excel COM API(win32com) 가동하여 v8.xlsx / v8.xlsm 네이티브 하이퍼링크 직접 주입 ===")
import win32com.client
import pythoncom

pythoncom.CoInitialize()
excel = win32com.client.DispatchEx("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

for file_path, is_xlsm in [(XLSX_PATH, False), (XLSM_PATH, True)]:
    if not os.path.exists(file_path):
        continue
    print(f"\n처리 중인 파일: {os.path.basename(file_path)}")
    wb = excel.Workbooks.Open(file_path)
    
    for sheet_name, folder_name, wbs_prefix in DISCIPLINES:
        try:
            ws = wb.Sheets(sheet_name)
        except Exception:
            print(f"시트 없음: {sheet_name}")
            continue
        
        t_data = disc_data[sheet_name]['tasks']
        task_list = list(t_data.values())
        task_list.sort(key=lambda x: (x['num'] if x['num'] is not None else 999, x['name']))
        
        # Determine column positions for 표준서, 수행지침, 체크리스트
        col_std = None
        col_guide = None
        col_chk = None
        
        for c in range(1, ws.UsedRange.Columns.Count + 1):
            hdr = str(ws.Cells(1, c).Value or "")
            if "표준서" in hdr and ("파일" in hdr or "열기" in hdr or "클릭" in hdr):
                col_std = c
            elif "수행지침" in hdr and ("파일" in hdr or "열기" in hdr or "클릭" in hdr):
                col_guide = c
            elif "체크리스트" in hdr and ("파일" in hdr or "열기" in hdr or "클릭" in hdr):
                col_chk = c

        # Fallback to standard columns O(15), Q(17), S(19) or N(14), P(16), R(18)
        if not col_std and not col_guide and not col_chk:
            col_std = 15
            col_guide = 17
            col_chk = 19
        elif not col_std:
            col_std = 15
        if not col_guide:
            col_guide = 17
        if not col_chk:
            col_chk = 19

        print(f"[{sheet_name}] 링크 대상 열: 표준서=Col {col_std}, 수행지침=Col {col_guide}, 체크리스트=Col {col_chk}")
        
        # 헤더 라벨 보정
        ws.Cells(1, col_std).Value = "표준서 파일 (HTML)"
        ws.Cells(1, col_guide).Value = "수행지침 파일 (HTML)"
        ws.Cells(1, col_chk).Value = "체크리스트 파일 (HTML)"
        
        row_count = ws.UsedRange.Rows.Count
        linked_count = 0
        
        for r in range(2, row_count + 1):
            # Row match finding
            wbs_val = str(ws.Cells(r, 4).Value or "")
            act_val = str(ws.Cells(r, 5).Value or "") + " " + str(ws.Cells(r, 6).Value or "") + " " + str(ws.Cells(r, 7).Value or "")
            
            # Match by task index or name
            t_idx = r - 2
            matched_task = None
            
            if t_idx < len(task_list):
                matched_task = task_list[t_idx]
            
            if matched_task:
                # 1. 표준서 링크
                if matched_task['std']:
                    cell = ws.Cells(r, col_std)
                    ws.Hyperlinks.Add(Anchor=cell, Address=matched_task['std'], TextToDisplay="👉 [클릭] 표준서 열기 📄")
                
                # 2. 수행지침 링크
                if matched_task['guide']:
                    cell = ws.Cells(r, col_guide)
                    ws.Hyperlinks.Add(Anchor=cell, Address=matched_task['guide'], TextToDisplay="👉 [클릭] 수행지침 열기 📄")
                
                # 3. 체크리스트 링크
                if matched_task['chk']:
                    cell = ws.Cells(r, col_chk)
                    ws.Hyperlinks.Add(Anchor=cell, Address=matched_task['chk'], TextToDisplay="👉 [클릭] 체크리스트 열기 📄")
                
                linked_count += 1

        print(f"  ✓ {sheet_name} 총 {linked_count}개 행 하이퍼링크 주입 완료")

    wb.Save()
    wb.Close(SaveChanges=True)
    print(f"✓ {os.path.basename(file_path)} 저장 및 닫기 완료!")

excel.Quit()
pythoncom.CoUninitialize()

print("\n=======================================================")
print("8대 공종 전체 엑셀 단순 하이퍼링크 연동 100% 완료!")
print("=======================================================")
