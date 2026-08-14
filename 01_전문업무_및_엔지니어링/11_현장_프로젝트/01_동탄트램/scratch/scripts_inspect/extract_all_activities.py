import os, sys, json, pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보'

f1 = os.path.join(base_dir, '06_기술제안 1공구 예정공정표 Activity List_(주)천우씨엠_260806.xlsx')
f2 = os.path.join(base_dir, '06_기술제안 2공구 예정공정표 Activity List_(주)천우씨엠_260806_rev2_교차로 명칭 수정.xlsx')

df1 = pd.read_excel(f1).dropna(how='all')
df2 = pd.read_excel(f2).dropna(how='all')

# Clean columns
def clean_df(df, zone_name):
    activities = []
    for _, row in df.iterrows():
        acode = str(row.get('ACODE', '')).strip()
        ades = str(row.get('ADES', '')).strip()
        og1 = str(row.get('OG1', '')).strip()
        ed = row.get('ED', 0)
        es = str(row.get('ES', '')).strip()[:10]
        ef = str(row.get('EF', '')).strip()[:10]
        
        if acode and acode != 'nan' and ades and ades != 'nan':
            try:
                ed_val = int(ed) if pd.notnull(ed) else 0
            except:
                ed_val = 0
                
            activities.append({
                'zone': zone_name,
                'acode': acode,
                'ades': ades,
                'og1': og1 if og1 != 'nan' else '기타',
                'ed': ed_val,
                'es': es if es != 'nan' else '',
                'ef': ef if ef != 'nan' else ''
            })
    return activities

act1 = clean_df(df1, '1공구')
act2 = clean_df(df2, '2공구')

all_activities = act1 + act2

print(f"✓ Extracted {len(act1)} activities from 1공구")
print(f"✓ Extracted {len(act2)} activities from 2공구")
print(f"✓ Total Activities: {len(all_activities)}")

# Save to scratch json
out_json = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\parsed_activities.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(all_activities, f, ensure_ascii=False, indent=2)

print(f"Saved to {out_json}")
