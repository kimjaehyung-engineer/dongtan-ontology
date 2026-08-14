import sys, openpyxl, json
sys.stdout.reconfigure(encoding='utf-8')

path1 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보\06_기술제안 1공구 예정공정표 Activity List_(주)천우씨엠_260806.xlsx'
path2 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보\06_기술제안 2공구 예정공정표 Activity List_(주)천우씨엠_260806_rev2_교차로 명칭 수정.xlsx'

def parse_wb(path, tool_label):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    rows = []
    for r in range(2, ws.max_row + 1):
        acode = str(ws.cell(row=r, column=2).value or '').strip()
        adesc = str(ws.cell(row=r, column=3).value or '').strip()
        og1 = str(ws.cell(row=r, column=4).value or '').strip()
        ed = ws.cell(row=r, column=5).value
        es = str(ws.cell(row=r, column=6).value or '').split()[0]
        ef = str(ws.cell(row=r, column=7).value or '').split()[0]
        
        if acode and adesc and acode != 'None' and acode != 'ACODE':
            rows.append({
                "acode": acode,
                "adesc": adesc,
                "og1": og1,
                "ed": ed,
                "es": es,
                "ef": ef,
                "tool": tool_label
            })
    wb.close()
    return rows

acts_1 = parse_wb(path1, "1공구")
acts_2 = parse_wb(path2, "2공구")

print(f"Total 1공구 Activities: {len(acts_1)}")
print(f"Total 2공구 Activities: {len(acts_2)}")
print(f"Grand Total Activities: {len(acts_1) + len(acts_2)}")

subgrade = [a for a in acts_1 + acts_2 if '노반' in a['adesc']]
track = [a for a in acts_1 + acts_2 if '궤도' in a['adesc']]
pavement = [a for a in acts_1 + acts_2 if '포장' in a['adesc']]
station = [a for a in acts_1 + acts_2 if '정거장' in a['adesc']]
preliminary = [a for a in acts_1 + acts_2 if any(k in a['adesc'] for k in ['착공', '지장물', '시험운행', '협의'])]

print(f"\nActivity Breakdown:")
print(f"  - 노반 (Subgrade): {len(subgrade)}")
print(f"  - 궤도 (Trackwork): {len(track)}")
print(f"  - 포장 (Pavement): {len(pavement)}")
print(f"  - 정거장 (Station): {len(station)}")
print(f"  - 준비/지장물/시험운행: {len(preliminary)}")
print(f"  - 기타/교차로/교량: {len(acts_1) + len(acts_2) - len(subgrade) - len(track) - len(pavement) - len(station) - len(preliminary)}")

dates = [a['es'] for a in acts_1 + acts_2 if a['es'] and a['es'] != 'None'] + [a['ef'] for a in acts_1 + acts_2 if a['ef'] and a['ef'] != 'None']
print(f"\nOverall Project Date Range: {min(dates)} ~ {max(dates)}")

print("\nSample 1공구 Activities:")
for a in acts_1[:8]:
    print(f"  [{a['acode']}] {a['adesc']} | {a['ed']}일 | {a['es']} ~ {a['ef']}")

print("\nSample 2공구 Activities:")
for a in acts_2[:8]:
    print(f"  [{a['acode']}] {a['adesc']} | {a['ed']}일 | {a['es']} ~ {a['ef']}")
