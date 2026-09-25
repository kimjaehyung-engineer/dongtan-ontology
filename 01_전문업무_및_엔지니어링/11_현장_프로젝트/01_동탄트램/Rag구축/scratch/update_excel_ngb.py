import sqlite3
import pandas as pd
from pathlib import Path

db_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\geotech_data.db")
excel_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\동탄_지반조사_전수_데이터_장부.xlsx")

conn = sqlite3.connect(str(db_path))

df_boreholes = pd.read_sql_query("SELECT * FROM boreholes ORDER BY id", conn)
df_spt = pd.read_sql_query("SELECT * FROM spt_records ORDER BY id", conn)
df_strata = pd.read_sql_query("SELECT * FROM strata_layers ORDER BY id", conn)

with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df_boreholes.to_excel(writer, sheet_name="시추공_마스터(77공)", index=False)
    df_spt.to_excel(writer, sheet_name="SPT_표준관입시험(838건)", index=False)
    df_strata.to_excel(writer, sheet_name="지층구성(241개)", index=False)

conn.close()
print("Excel Ledger Updated Successfully with NGB!")
print("Boreholes:", len(df_boreholes))
print("SPT:", len(df_spt))
print("Strata:", len(df_strata))
