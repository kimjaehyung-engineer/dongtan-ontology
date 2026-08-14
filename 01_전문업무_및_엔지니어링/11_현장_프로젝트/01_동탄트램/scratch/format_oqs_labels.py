# -*- coding: utf-8 -*-
"""
사전토공사 시트 O열, Q열, S열에
'👉 [클릭] 표준서 열기 📄', '👉 [클릭] 수행지침 열기 📄', '👉 [클릭] 체크리스트 열기 📄'
텍스트와 파란색 밑줄 하이퍼링크를 완벽하게 주입합니다.
"""

import os, sys, win32com.client

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)")
V8_ATTACH_DIR = os.path.join(BASE_DIR, "매뉴얼BODY(집행단계-첨부폴더)v8")
EARTH_ATTACH_DIR = os.path.join(V8_ATTACH_DIR, "2.사전토공사")
TARGET_XLSM = os.path.join(BASE_DIR, "매뉴얼 BODY (집행단계)v8.xlsm")
TARGET_XLSX = os.path.join(BASE_DIR, "매뉴얼 BODY (집행단계)v8.xlsx")

earth_htmls = []
for root, dirs, files in os.walk(EARTH_ATTACH_DIR):
    for f in files:
        if f.lower().endswith(".html"):
            earth_htmls.append(os.path.join(root, f))

def normalize(s):
    if not s: return ""
    return str(s).strip().replace(" ", "").replace("_", "").replace("-", "").replace("/", "").replace("(", "").replace(")", "").lower()

def find_earth_html(act_name, doc_type, l4_code=""):
    n_act = normalize(act_name)
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

excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False
excel.ScreenUpdating = False

try:
    wb = excel.Workbooks.Open(TARGET_XLSM)
    ws = wb.Sheets("사전토공사")
    max_row = ws.UsedRange.Rows.Count
    print(f"사전토공사 행 수: {max_row}")

    for r in range(2, max_row + 1):
        act_name = str(ws.Cells(r, 8).Value or "").strip()
        l4_code = str(ws.Cells(r, 4).Value or "").strip()

        std_p = find_earth_html(act_name, "표준서", l4_code)
        guide_p = find_earth_html(act_name, "수행지침", l4_code)
        chk_p = find_earth_html(act_name, "체크리스트", l4_code)

        # O열 (Col 15)
        cell_o = ws.Cells(r, 15)
        cell_o.Clear()
        if std_p and os.path.exists(std_p):
            ws.Hyperlinks.Add(Anchor=cell_o, Address=std_p, TextToDisplay="👉 [클릭] 표준서 열기 📄")
        else:
            cell_o.Value = "-"
        cell_o.Font.Name = "맑은 고딕"
        cell_o.Font.Size = 9
        cell_o.Font.Bold = True
        cell_o.Font.Color = 0xFF0000
        cell_o.Font.Underline = 2
        cell_o.HorizontalAlignment = -4108

        # Q열 (Col 17)
        cell_q = ws.Cells(r, 17)
        cell_q.Clear()
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

        # S열 (Col 19)
        cell_s = ws.Cells(r, 19)
        cell_s.Clear()
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

    # 열 너비 자동 보정
    ws.Columns("O:O").ColumnWidth = 24
    ws.Columns("Q:Q").ColumnWidth = 24
    ws.Columns("S:S").ColumnWidth = 24

    wb.Save()
    print("v8.xlsm 저장 완료!")

    # v8.xlsx로도 깨끗하게 내보내기
    if os.path.exists(TARGET_XLSX):
        os.remove(TARGET_XLSX)
    wb.SaveAs(TARGET_XLSX, FileFormat=51)
    wb.Close()
    print("v8.xlsx 저장 완료!")

finally:
    excel.Quit()

print("=== 모든 작업 성공 ===")
