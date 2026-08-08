import os, sys, pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보'

f1 = os.path.join(base_dir, '03_기술제안 1공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx')
f2 = os.path.join(base_dir, '03_기술제안 2공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx')

xl1 = pd.ExcelFile(f1)
xl2 = pd.ExcelFile(f2)

for sname in xl1.sheet_names:
    df = xl1.parse(sname, header=None)
    for r_idx in range(len(df)):
        row_str = ' | '.join([str(val) for val in df.iloc[r_idx] if pd.notnull(val)])
        if '구간' in row_str or '부지' in row_str or '일반' in row_str:
            if '샘플' not in row_str and len(row_str) < 300:
                print(f"Sheet 1 [{sname}] R{r_idx}: {row_str}")

print("\n--- Sheet 2 ---")
for sname in xl2.sheet_names:
    df = xl2.parse(sname, header=None)
    for r_idx in range(len(df)):
        row_str = ' | '.join([str(val) for val in df.iloc[r_idx] if pd.notnull(val)])
        if '구간' in row_str or '부지' in row_str or '일반' in row_str:
            if '샘플' not in row_str and len(row_str) < 300:
                print(f"Sheet 2 [{sname}] R{r_idx}: {row_str}")
