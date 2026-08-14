import os, sys, openpyxl, json, pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보'

f1 = os.path.join(base_dir, '03_기술제안 1공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx')
f2 = os.path.join(base_dir, '03_기술제안 2공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx')

wb1 = openpyxl.load_workbook(f1, data_only=True)
ws1 = wb1.active

wb2 = openpyxl.load_workbook(f2, data_only=True)
ws2 = wb2.active

# Build cell value map for merged ranges
def get_merged_val_map(ws):
    val_map = {}
    for m in ws.merged_cells.ranges:
        val = ws.cell(row=m.min_row, column=m.min_col).value
        if val is not None:
            val_str = str(val).strip()
            for r in range(m.min_row, m.max_row + 1):
                for c in range(m.min_col, m.max_col + 1):
                    val_map[(r, c)] = val_str
    return val_map

map1 = get_merged_val_map(ws1)
map2 = get_merged_val_map(ws2)

def extract_section_splits(ws, val_map, zone_name):
    splits = []
    current_split = None
    
    for r in range(11, ws.max_row + 1):
        sec = ws.cell(row=r, column=3).value
        start_sta = ws.cell(row=r, column=7).value
        end_sta = ws.cell(row=r, column=8).value
        dist = ws.cell(row=r, column=9).value
        
        # Check column 12 (L) or merged map for section split name
        split_name = val_map.get((r, 12)) or ws.cell(row=r, column=12).value
        
        if sec and str(sec).strip() and '샘플' not in str(sec):
            sec_clean = str(sec).strip()
            split_clean = str(split_name).strip() if split_name else ''
            
            if split_clean and ('부지' in split_clean or '구간' in split_clean):
                current_split = split_clean.replace('\n', ' ')
            
            grp_name = current_split if current_split else f"{zone_name} 주요구간"
            
            try:
                start_m = float(str(start_sta).replace('km', '').replace('m', '').strip()) if start_sta is not None else 0.0
                end_m = float(str(end_sta).replace('km', '').replace('m', '').strip()) if end_sta is not None else 0.0
            except:
                start_m = 0.0
                end_m = 0.0
                
            splits.append({
                'zone': zone_name,
                'splitGroup': grp_name,
                'sectionName': sec_clean,
                'startM': start_m,
                'endM': end_m,
                'distM': float(dist) if dist and isinstance(dist, (int, float)) else 0.0
            })
    return splits

splits1 = extract_section_splits(ws1, map1, '1공구')
splits2 = extract_section_splits(ws2, map2, '2공구')

all_splits = splits1 + splits2

print(f"✓ Extracted {len(splits1)} section splits from 1공구")
print(f"✓ Extracted {len(splits2)} section splits from 2공구")
print(f"✓ Total Section Splits: {len(all_splits)}")

# Print unique split groups
grp1 = sorted(list(set(s['splitGroup'] for s in splits1)))
grp2 = sorted(list(set(s['splitGroup'] for s in splits2)))

print("\n=== 1공구 시공구간 분할 그룹 목록 ===")
for g in grp1:
    count = len([s for s in splits1 if s['splitGroup'] == g])
    print(f"  - {g} ({count}개 세부구간)")

print("\n=== 2공구 시공구간 분할 그룹 목록 ===")
for g in grp2:
    count = len([s for s in splits2 if s['splitGroup'] == g])
    print(f"  - {g} ({count}개 세부구간)")

# Save to json
out_json = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\section_splits.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(all_splits, f, ensure_ascii=False, indent=2)

print(f"\nSaved section splits to {out_json}")
