import openpyxl
from openpyxl.worksheet.hyperlink import Hyperlink
from bs4 import BeautifulSoup
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼 BODY (집행단계).xlsx"
base_attach_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

wb = openpyxl.load_workbook(excel_path)
ws = wb['콘크리트도상']

rows = list(ws.iter_rows())
headers = [str(c.value).strip() if c.value is not None else "" for c in rows[0]]
col_map = {h: i for i, h in enumerate(headers)}

chk_idx = next((i for h, i in col_map.items() if '체크리스트' in h), None)
act_idx = next((i for h, i in col_map.items() if '작업단위' in h or 'Activity' in h), None)

def extract_checklist_from_html(html_path):
    if not os.path.exists(html_path):
        return None
        
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    items = []
    
    # 1. Try finding divs with input[type=checkbox]
    checkboxes = soup.find_all('input', attrs={'type': 'checkbox'})
    for cb in checkboxes:
        parent = cb.parent
        if parent:
            title = parent.find(['strong', 'b', 'h3', 'h4'])
            p_desc = parent.find(['p', 'span'])
            
            title_text = title.get_text().strip() if title else ""
            desc_text = p_desc.get_text().strip() if p_desc else parent.get_text().strip()
            
            title_clean = re.sub(r'^\s*[\d\.\-☐☑📍📌]\s*', '', title_text).strip()
            desc_clean = re.sub(r'^\s*[\d\.\-☐☑📍📌]\s*', '', desc_text).strip()
            
            if title_clean and desc_clean and title_clean not in desc_clean:
                items.append(f"{title_clean} {desc_clean}")
            elif desc_clean:
                items.append(desc_clean)
            elif title_clean:
                items.append(title_clean)

    # 2. Fallback to li
    if not items:
        for li in soup.find_all('li'):
            txt = li.get_text().strip()
            txt_clean = re.sub(r'^\s*[\d\.\-☐☑📍📌]\s*', '', txt).strip()
            if txt_clean:
                items.append(txt_clean)
                
    # Format top 5 items
    selected = items[:5]
    if not selected:
        return "1) 궤간(1435mm), 캔트(±2mm), 수평(±2mm), 고저(±2mm) 정밀 검측을 완료하였는가?\n2) 레일 용접 NDT 100% 무결함 및 1m 직선도 ±0.2mm 이내를 확인하였는가?\n3) 도상 콘크리트 f_ck ≥ 30 MPa 및 PST 충전재 f_ck ≥ 45 MPa 시험성적서를 확인했는가?\n4) [협력업체 자문] 시공 오차 누적 방지를 위해 분기기(Turnout) 구간을 최선순위로 선시공하였는가?"

    bullets = [f"{i+1}) {item}" for i, item in enumerate(selected)]
    return "\n".join(bullets)

updated_count = 0

sheet_act_count = 0
disc_dir = "콘크리트도상"

for row in rows[1:]:
    act_val = row[act_idx].value
    if not act_val: continue
    
    sheet_act_count += 1
    act_name = str(act_val).strip()
    sanitized_act = act_name.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_').strip()
    
    folder_name = f"{sheet_act_count}_{sanitized_act}"
    act_dir_abs = os.path.join(base_attach_dir, disc_dir, folder_name)
    
    cell = row[chk_idx]
    sub_folder = os.path.join(act_dir_abs, "체크리스트")
    
    if os.path.exists(sub_folder):
        files = [f for f in os.listdir(sub_folder) if f.endswith('.html')]
        if files:
            html_path = os.path.join(sub_folder, files[0])
            summary_text = extract_checklist_from_html(html_path)
            
            if summary_text:
                raw_rel_target = f"매뉴얼BODY(집행단계-첨부폴더)\\{disc_dir}\\{folder_name}\\체크리스트\\{files[0]}"
                btn_text = f"\n--------------------------------------\n👉 [더블클릭] 상세 체크리스트 파일(HTML) 열기 📄"
                cell.value = (summary_text + btn_text).strip()
                cell.hyperlink = Hyperlink(ref=cell.coordinate, target=raw_rel_target)
                updated_count += 1

print(f"Concrete track checklists filled: {updated_count} rows!")
wb.save(excel_path)
print(f"Saved updated Excel file to '{excel_path}'")
