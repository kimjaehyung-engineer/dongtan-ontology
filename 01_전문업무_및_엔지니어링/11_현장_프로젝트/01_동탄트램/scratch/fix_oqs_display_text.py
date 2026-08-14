# -*- coding: utf-8 -*-
"""
Excel COM을 사용하여 매뉴얼 BODY (집행단계)v8.xlsm 및 v8.xlsx의
사전토공사 시트 O열, Q열, S열에 셀 텍스트와 네이티브 하이퍼링크를 완벽하게 주입하여
화면에 '👉 [클릭] 표준서 열기 📄'가 즉시 파란색 링크로 보이도록 수정합니다.
"""

import os
import sys
import win32com.client

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)")
V8_ATTACH_DIR = os.path.join(BASE_DIR, "매뉴얼BODY(집행단계-첨부폴더)v8")
EARTH_ATTACH_DIR = os.path.join(V8_ATTACH_DIR, "2.사전토공사")
TARGET_XLSM = os.path.join(BASE_DIR, "매뉴얼 BODY (집행단계)v8.xlsm")
TARGET_XLSX = os.path.join(BASE_DIR, "매뉴얼 BODY (집행단계)v8.xlsx")

# 1. HTML 파일 인덱싱
earth_htmls = []
for root, dirs, files in os.walk(EARTH_ATTACH_DIR):
    for f in files:
        if f.lower().endswith(".html"):
            earth_htmls.append(os.path.join(root, f))

def normalize(s):
    if not s:
        return ""
    return str(s).strip().replace(" ", "").replace("_", "").replace("-", "").replace("/", "").replace("(", "").replace(")", "").lower()

def find_earth_html(act_name, doc_type, l4_code=""):
    n_act = normalize(act_name)
    n_l4 = normalize(l4_code)
    
    for sub in os.listdir(EARTH_ATTACH_DIR):
        sub_p = os.path.join(EARTH_ATTACH_DIR, sub)
        if os.path.isdir(sub_p):
            n_sub = normalize(sub)
            if n_act and (n_act in n_sub or n_sub in n_act or n_act[:4] in n_sub):
                doc_sub = os.path.join(sub_p, doc_type)
                if os.path.exists(doc_sub):
                    for f in os.listdir(doc_sub):
                        if f.lower().endswith(".html") and doc_type in f:
                            return os.path.join(doc_sub, f)
                for f in os.listdir(sub_p):
                    if f.lower().endswith(".html") and doc_type in f:
                        return os.path.join(sub_p, f)

    for p in earth_htmls:
        if doc_type in os.path.basename(p):
            n_p = normalize(p)
            if n_act and (n_act in n_p or n_act[:4] in n_p):
                return p

    for p in earth_htmls:
        if doc_type in os.path.basename(p):
            return p

    return None

def process_file_with_excel(excel_path):
    print(f"\n처리 중: {os.path.basename(excel_path)}")
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    excel.ScreenUpdating = False

    try:
        wb = excel.Workbooks.Open(excel_path)
        ws = wb.Sheets("사전토공사")
        
        max_row = ws.UsedRange.Rows.Count
        print(f"  - 사전토공사 행 수: {max_row}")

        count = 0
        for r in range(2, max_row + 1):
            act_name = str(ws.Cells(r, 8).Value or "").strip()
            l4_code = str(ws.Cells(r, 4).Value or "").strip()

            std_p = find_earth_html(act_name, "표준서", l4_code)
            guide_p = find_earth_html(act_name, "수행지침", l4_code)
            chk_p = find_earth_html(act_name, "체크리스트", l4_code)

            # O열 (Col 15) - 표준서
            cell_o = ws.Cells(r, 15)
            cell_o.ClearContents()
            if std_p and os.path.exists(std_p):
                ws.Hyperlinks.Add(Anchor=cell_o, Address=std_p, TextToDisplay="👉 [클릭] 표준서 열기 📄")
            else:
                cell_o.Value = "-"
            cell_o.Font.Name = "맑은 고딕"
            cell_o.Font.Size = 9
            cell_o.Font.Bold = True
            cell_o.Font.Color = 0xFF0000 # Blue
            cell_o.Font.Underline = 2
            cell_o.HorizontalAlignment = -4108 # Center

            # Q열 (Col 17) - 수행지침
            cell_q = ws.Cells(r, 17)
            cell_q.ClearContents()
            if guide_p and os.path.exists(guide_p):
                ws.Hyperlinks.Add(Anchor=cell_q, Address=guide_p, TextToDisplay="👉 [클릭] 수행지침 열기 📄")
            else:
                cell_q.Value = "-"
            cell_q.Font.Name = "맑은 고딕"
            cell_q.Font.Size = 9
            cell_q.Font.Bold = True
            cell_q.Font.Color = 0xFF0000
            cell_q.Font.Underline = 2
            cell_q.HorizontalAlignment = -4108

            # S열 (Col 19) - 체크리스트
            cell_s = ws.Cells(r, 19)
            cell_s.ClearContents()
            if chk_p and os.path.exists(chk_p):
                ws.Hyperlinks.Add(Anchor=cell_s, Address=chk_p, TextToDisplay="👉 [클릭] 체크리스트 열기 📄")
            else:
                cell_s.Value = "-"
            cell_s.Font.Name = "맑은 고딕"
            cell_s.Font.Size = 9
            cell_s.Font.Bold = True
            cell_s.Font.Color = 0xFF0000
            cell_s.Font.Underline = 2
            cell_s.HorizontalAlignment = -4108

            count += 1

        # 전체 계산 및 저장
        excel.Calculate()
        wb.Save()
        wb.Close()
        print(f"  -> 완료: {count}개 행에 대해 O열/Q열/S열 텍스트 및 하이퍼링크 주입 완료!")

    except Exception as e:
        print(f"에러: {e}")
        try:
            wb.Close(SaveChanges=False)
        except:
            pass
    finally:
        excel.Quit()

process_file_with_excel(TARGET_XLSM)
process_file_with_excel(TARGET_XLSX)

print("\n=== 모든 파일 갱신 완료 ===")
