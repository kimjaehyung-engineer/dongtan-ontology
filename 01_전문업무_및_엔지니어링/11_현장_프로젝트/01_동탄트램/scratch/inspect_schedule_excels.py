import os, sys, pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\교차로 정보'

files = [
    '03_기술제안 1공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx',
    '03_기술제안 2공구 본선구간 공기산출 근거_(주)천우씨엠.xlsx',
    '06_기술제안 1공구 예정공정표 Activity List_(주)천우씨엠_260806.xlsx',
    '06_기술제안 2공구 예정공정표 Activity List_(주)천우씨엠_260806_rev2_교차로 명칭 수정.xlsx'
]

for fname in files:
    fp = os.path.join(base_dir, fname)
    print(f"\n==========================================")
    print(f"File: {fname}")
    print(f"==========================================")
    try:
        xl = pd.ExcelFile(fp)
        print(f"Sheet names: {xl.sheet_names}")
        for sname in xl.sheet_names:
            df = xl.parse(sname)
            print(f"\n--- Sheet: {sname} (Shape: {df.shape}) ---")
            print("Columns:", list(df.columns))
            print("First 3 rows:\n", df.head(3))
    except Exception as e:
        print("Error reading excel:", e)
