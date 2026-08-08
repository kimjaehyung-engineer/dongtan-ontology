import sys, openpyxl, json, re
sys.stdout.reconfigure(encoding='utf-8')

# File paths
p_sec1 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보\03_기술제안 1공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx'
p_sec2 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보\03_기술제안 2공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx'

p_act1 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보\06_기술제안 1공구 예정공정표 Activity List_(주)천우씨엠_260806.xlsx'
p_act2 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보\06_기술제안 2공구 예정공정표 Activity List_(주)천우씨엠_260806_rev2_교차로 명칭 수정.xlsx'

# 1. Parse Section mapping from 03 files
def parse_sections(path, tool_name):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    sections = []
    current_master = ""
    for r in range(4, ws.max_row + 1):
        v_sub = str(ws.cell(row=r, column=1).value or '').strip()
        v_master = str(ws.cell(row=r, column=12).value or '').strip()
        st_start = str(ws.cell(row=r, column=5).value or '').strip()
        st_end = str(ws.cell(row=r, column=6).value or '').strip()
        len_sub = ws.cell(row=r, column=7).value
        
        if v_master and v_master != 'None':
            current_master = v_master
            
        if v_sub and v_sub != 'None' and '구간' not in v_sub and '공사기간' not in v_sub:
            sections.append({
                "subSection": v_sub,
                "masterSection": current_master or "기타구간",
                "startStaStr": st_start,
                "endStaStr": st_end,
                "length": len_sub,
                "tool": tool_name
            })
    wb.close()
    return sections

sec_1 = parse_sections(p_sec1, "1공구")
sec_2 = parse_sections(p_sec2, "2공구")
all_sections = sec_1 + sec_2

print(f"Parsed Sub-Sections: 1공구={len(sec_1)}, 2공구={len(sec_2)}")

# 2. Parse 06 Activity List files
def parse_activities(path, tool_name):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    acts = []
    for r in range(2, ws.max_row + 1):
        acode = str(ws.cell(row=r, column=2).value or '').strip()
        adesc = str(ws.cell(row=r, column=3).value or '').strip()
        og1 = str(ws.cell(row=r, column=4).value or '').strip()
        ed = ws.cell(row=r, column=5).value
        es = str(ws.cell(row=r, column=6).value or '').split()[0]
        ef = str(ws.cell(row=r, column=7).value or '').split()[0]
        
        if acode and adesc and acode != 'None' and acode != 'ACODE':
            # Classify work type (공종)
            category = "기타/준비"
            if '노반' in adesc:
                category = "노반공"
            elif '궤도' in adesc:
                category = "궤도공"
            elif '포장' in adesc:
                category = "포장공"
            elif '정거장' in adesc:
                category = "정거장공"
            elif any(k in adesc for k in ['착공', '지장물', '시험운행', '협의', '시스템']):
                category = "준비/지장물/시험"

            # Match to master section / sub section
            matched_master = "전체/기타"
            matched_sub = adesc
            
            # Extract section prefix like (본)1-2, (기교)1-7/8, (본)2-26, etc.
            m = re.search(r'\((본|기교|기타)\)[\d\-]+[A-Za-z\(\)\d/]*', adesc)
            clean_sub = m.group(0) if m else adesc
            
            # Find matching sub-section in all_sections
            for s in all_sections:
                if s['tool'] == tool_name and (clean_sub in s['subSection'] or s['subSection'] in adesc):
                    matched_master = s['masterSection']
                    matched_sub = s['subSection']
                    break
            
            acts.append({
                "acode": acode,
                "adesc": adesc,
                "cleanSub": clean_sub,
                "og1": og1,
                "ed": ed or 0,
                "es": es if es != 'None' else '',
                "ef": ef if ef != 'None' else '',
                "category": category,
                "tool": tool_name,
                "masterSection": matched_master,
                "matchedSub": matched_sub
            })
    wb.close()
    return acts

acts_1 = parse_activities(p_act1, "1공구")
acts_2 = parse_activities(p_act2, "2공구")
all_activities = acts_1 + acts_2

print(f"Parsed Activities: 1공구={len(acts_1)}, 2공구={len(acts_2)}, Total={len(all_activities)}")

out_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\activities_db.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(all_activities, f, ensure_ascii=False, indent=2)

print(f"Saved activities_db.json successfully! ({len(all_activities)} items)")
