import os, sys, pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보'

f1 = os.path.join(base_dir, '03_기술제안 1공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx')
f2 = os.path.join(base_dir, '03_기술제안 2공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx')

df1 = pd.read_excel(f1, header=None)
df2 = pd.read_excel(f2, header=None)

print("=== 1공구 구간 분할 데이터 추출 ===")
sec1_data = []
for idx in range(7, len(df1)):
    row = df1.iloc[idx]
    no = str(row[1]).strip()
    sec_name = str(row[2]).strip()
    start_sta = str(row[6]).strip()
    end_sta = str(row[7]).strip()
    dist_m = str(row[8]).strip()
    group_split = str(row[13]).strip() if len(row) > 13 else ''
    
    if sec_name and sec_name != 'nan' and '샘플' not in sec_name:
        sec1_data.append({
            'no': no,
            'section': sec_name,
            'start_sta': start_sta,
            'end_sta': end_sta,
            'dist_m': dist_m,
            'split_group': group_split if group_split != 'nan' else ''
        })

for d in sec1_data[:20]:
    print(d)

print("\n=== 2공구 구간 분할 데이터 추출 ===")
sec2_data = []
for idx in range(7, len(df2)):
    row = df2.iloc[idx]
    no = str(row[1]).strip()
    sec_name = str(row[2]).strip()
    start_sta = str(row[6]).strip()
    end_sta = str(row[7]).strip()
    dist_m = str(row[8]).strip()
    group_split = str(row[13]).strip() if len(row) > 13 else ''
    
    if sec_name and sec_name != 'nan' and '샘플' not in sec_name:
        sec2_data.append({
            'no': no,
            'section': sec_name,
            'start_sta': start_sta,
            'end_sta': end_sta,
            'dist_m': dist_m,
            'split_group': group_split if group_split != 'nan' else ''
        })

for d in sec2_data[:20]:
    print(d)
