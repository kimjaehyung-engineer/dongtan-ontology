import os, sys, pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보'

f1 = os.path.join(base_dir, '03_기술제안 1공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx')
f2 = os.path.join(base_dir, '03_기술제안 2공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx')

df1 = pd.read_excel(f1, header=None)
df2 = pd.read_excel(f2, header=None)

print("=== 1공구 Row 4~8 Headers ===")
print(df1.iloc[4:10, :10])

print("\n=== 2공구 Row 4~8 Headers ===")
print(df2.iloc[4:10, :10])
