import os, sys, pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보'

f1 = os.path.join(base_dir, '06_기술제안 1공구 예정공정표 Activity List_(주)천우씨엠_260806.xlsx')
f2 = os.path.join(base_dir, '06_기술제안 2공구 예정공정표 Activity List_(주)천우씨엠_260806_rev2_교차로 명칭 수정.xlsx')

df1 = pd.read_excel(f1).dropna(how='all')
df2 = pd.read_excel(f2).dropna(how='all')

print(f"=== 1공구 Activity List Sample (Total: {len(df1)}) ===")
print(df1[['ACODE', 'ADES', 'OG1', 'ED', 'ES', 'EF']].head(10))

print(f"\n=== 2공구 Activity List Sample (Total: {len(df2)}) ===")
print(df2[['ACODE', 'ADES', 'OG1', 'ED', 'ES', 'EF']].head(10))

print("\n=== Unique OG1 groups ===")
print("1공구 OG1:", df1['OG1'].unique()[:15])
print("2공구 OG1:", df2['OG1'].unique()[:15])
