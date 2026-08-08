import sys
import os
import glob
import re

sys.stdout.reconfigure(encoding='utf-8')

# Target V1 HTML file
search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Updating V1 HTML to replace avgLen with length:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Layer Panel Label Text
content = content.replace("교차로명 라벨 (단계별 평균연장)", "교차로명 라벨 (구간연장)")
content = content.replace("교차로 정보 (단계별 평균연장)", "교차로 정보 (구간연장)")

# 2. Update Map Badge textStr: `${item.avgLen}m` -> `${item.length}m`
content = content.replace("[${item.avgLen}m]", "[${item.length}m]")

# 3. Update Tooltip text: `<b>단계별 평균작업연장: ${item.avgLen}m</b>` -> `<b>구간 총 연장: ${item.length}m</b>`
content = content.replace("<b>단계별 평균작업연장: ${item.avgLen}m</b>", "<b>구간 총 연장: ${item.length}m</b>")

# 4. Update Drawer Active KPI Card
old_kpi_card = """<div style="font-size: 0.75rem; font-weight: 700; color: ${is1 ? '#c2410c' : '#1e40af'}; text-transform: uppercase;">단계별 평균작업연장</div>
          <div style="font-size: 1.8rem; font-weight: 900; color: ${is1 ? '#ea580c' : '#2563eb'}; margin-top: 0.2rem;">${item.avgLen} <span style="font-size: 1rem;">m</span></div>"""

new_kpi_card = """<div style="font-size: 0.75rem; font-weight: 700; color: ${is1 ? '#c2410c' : '#1e40af'}; text-transform: uppercase;">교차로 구간 연장</div>
          <div style="font-size: 1.8rem; font-weight: 900; color: ${is1 ? '#ea580c' : '#2563eb'}; margin-top: 0.2rem;">${item.length} <span style="font-size: 1rem;">m</span></div>"""

content = content.replace(old_kpi_card, new_kpi_card)

# 5. Update Drawer List Card metric
old_list_metric = """<div style="font-size: 0.68rem; color: var(--text-muted); font-weight: 600;">평균작업연장</div>
        <div style="font-size: 1.15rem; font-weight: 800; color: ${is1 ? '#ea580c' : '#2563eb'};">${item.avgLen}m</div>"""

new_list_metric = """<div style="font-size: 0.68rem; color: var(--text-muted); font-weight: 600;">구간연장</div>
        <div style="font-size: 1.15rem; font-weight: 800; color: ${is1 ? '#ea580c' : '#2563eb'};">${item.length}m</div>"""

content = content.replace(old_list_metric, new_list_metric)

# 6. Check for any remaining avgLen references in UI text
content = content.replace("단계별 평균작업연장", "교차로 구간연장")
content = content.replace("평균작업연장", "구간연장")

with open(file_v1, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully replaced all avgLen metrics with section length (item.length) in V1 HTML!")
