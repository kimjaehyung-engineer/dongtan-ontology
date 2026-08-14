# -*- coding: utf-8 -*-
"""
Excel COM (win32com)을 이용하여 매뉴얼 BODY (집행단계)v8.xlsx 단일 파일에
모든 표준서, 수행지침, 체크리스트 열에 TEST2 방식(ws.Hyperlinks.Add)으로 하이퍼링크를 전수 주입합니다.
"""

import os
import sys
import win32com.client

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)")
V8_ATTACH_DIR = os.path.join(BASE_DIR, "매뉴얼BODY(집행단계-첨부폴더)v8")
TARGET_EXCEL = os.path.join(BASE_DIR, "매뉴얼 BODY (집행단계)v8.xlsx")

SHEET_FOLDER_MAP = {
    "지반조사": "1.지반조사",
    "지반조사(원본서식)": "1.지반조사",
    "사전토공사": "2.사전토공사",
    "지장물이설": "3.지장물이설",
    "상부강화노반": "4.상부강화노반",
    "콘크리트도상": "5.콘크리트도상",
    "건축": "6.건축",
    "신호": "7.신호분야",
    "신호분야": "7.신호분야",
    "전기": "8.전기분야",
    "전기분야": "8.전기분야",
    "통신": "9.통신분야",
    "통신분야": "9.통신분야",
    "기계": "10.기계분야",
    "기계분야": "10.기계분야",
    "철도종합시운전": "11.철도종합시운전",
}

# 첨부폴더 내 모든 HTML 파일 인덱싱
all_html_files = []
for root, dirs, files in os.walk(V8_ATTACH_DIR):
    for f in files:
        if f.lower().endswith(".html"):
            all_html_files.append(os.path.join(root, f))

print(f"총 발견된 첨부폴더 HTML 파일 수: {len(all_html_files)}개")

def clean_name(s):
    if not s:
        return ""
    return str(s).strip().replace(" ", "").replace("_", "").replace("-", "").lower()

def find_matching_html(sheet_name, activity_name, doc_type):
    category_folder = SHEET_FOLDER_MAP.get(sheet_name, sheet_name)
    target_dir = os.path.join(V8_ATTACH_DIR, category_folder)
    
    if not os.path.exists(target_dir):
        return None

    c_act = clean_name(activity_name)
    
    # 1. 하위 폴더 매칭
    for sub in os.listdir(target_dir):
        sub_p = os.path.join(target_dir, sub)
        if os.path.isdir(sub_p):
            c_sub = clean_name(sub)
            if c_act and (c_act in c_sub or c_sub in c_act or c_act.replace("1", "").replace("2", "") in c_sub):
                doc_sub = os.path.join(sub_p, doc_type)
                if os.path.exists(doc_sub):
                    for f in os.listdir(doc_sub):
                        if f.lower().endswith(".html") and doc_type in f:
                            return os.path.join(doc_sub, f)
                for f in os.listdir(sub_p):
                    if f.lower().endswith(".html") and doc_type in f:
                        return os.path.join(sub_p, f)
                        
    # 2. 전체 디렉토리 탐색
    for p in all_html_files:
        if category_folder in p and doc_type in os.path.basename(p):
            c_p = clean_name(p)
            if c_act and (c_act in c_p or c_act[:4] in c_p):
                return p
                
    return None

def process_v8_only():
    print(f"\n==========================================")
    print(f"Excel COM으로 처리 중: {os.path.basename(TARGET_EXCEL)}")
    print(f"==========================================")

    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    try:
        wb = excel.Workbooks.Open(TARGET_EXCEL)
        total_links = 0

        for sheet_idx in range(1, wb.Sheets.Count + 1):
            ws = wb.Sheets(sheet_idx)
            sname = ws.Name
            
            if sname in ["대시보드", "공정매뉴얼", "GUIDE"]:
                continue
                
            max_col = ws.UsedRange.Columns.Count
            max_row = ws.UsedRange.Rows.Count
            
            col_act = None
            col_std = None
            col_guide = None
            col_chk = None
            
            for c in range(1, max_col + 1):
                val = str(ws.Cells(1, c).Value or "").strip()
                if "작업단위" in val or "액티비티" in val or "세부작업명" in val:
                    col_act = c
                elif "표준서 파일" in val or ("표준서" in val and "파일" in val):
                    col_std = c
                elif "수행지침 파일" in val or ("수행지침" in val and "파일" in val):
                    col_guide = c
                elif "체크리스트 파일" in val or ("체크리스트" in val and "파일" in val):
                    col_chk = c

            if not col_act:
                col_act = 6

            sheet_links = 0
            
            for r in range(2, max_row + 1):
                act_name = str(ws.Cells(r, col_act).Value or "").strip()
                if not act_name:
                    continue

                targets = [
                    (col_std, "표준서", "👉 [클릭] 표준서 열기 📄"),
                    (col_guide, "수행지침", "👉 [클릭] 수행지침 열기 📄"),
                    (col_chk, "체크리스트", "👉 [클릭] 체크리스트 열기 📄"),
                ]

                for col_idx, doc_type, label in targets:
                    if not col_idx:
                        continue
                    
                    html_file = find_matching_html(sname, act_name, doc_type)
                    
                    if html_file and os.path.exists(html_file):
                        cell = ws.Cells(r, col_idx)
                        cell.ClearContents()
                        ws.Hyperlinks.Add(
                            Anchor=cell,
                            Address=html_file,
                            TextToDisplay=label
                        )
                        cell.Font.Name = "맑은 고딕"
                        cell.Font.Size = 9
                        cell.Font.Bold = True
                        cell.Font.Color = 0xFF0000
                        cell.Font.Underline = 2
                        
                        sheet_links += 1
                        total_links += 1

            print(f"  - 시트 [{sname}]: {sheet_links}개 하이퍼링크 주입 완료")

        wb.Save()
        wb.Close()
        print(f"\n>> [성공] v8 엑셀에 총 {total_links}개 네이티브 하이퍼링크 완벽 저장됨!")

    except Exception as e:
        print(f"에러 발생: {e}")
        try:
            wb.Close(SaveChanges=False)
        except:
            pass
    finally:
        excel.Quit()

if __name__ == "__main__":
    process_v8_only()
