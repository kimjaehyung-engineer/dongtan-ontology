# -*- coding: utf-8 -*-
import fitz, openpyxl, re

f1 = r'01_SOURCE_DOCUMENTS\02_기본설계_기술제안\02_지반조사\기본설계 시추주상도(1공구)_45공.pdf'
doc1 = fitz.open(f1)

# Extract details per hole
hole_data = {}
for p in range(len(doc1)):
    t = doc1[p].get_text()
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    
    hole_no = ''
    coord_x, coord_y = '', ''
    gw = ''
    el = ''
    
    for i, l in enumerate(lines):
        if 'HOLE No' in l or 'HOLE NO' in l:
            if i+1 < len(lines):
                hole_no = lines[i+1].strip()
        if 'LOCATION' in l and i+1 < len(lines):
            cand = lines[i+1]
            m_x = re.search(r'X:\s*([0-9\.]+)', cand)
            m_y = re.search(r'Y:\s*([0-9\.]+)', cand)
            if m_x: coord_x = m_x.group(1)
            if m_y: coord_y = m_y.group(1)
        if 'GROUND WATER' in l:
            for j in range(1, 4):
                if i+j < len(lines) and re.match(r'^[0-9\.]+$', lines[i+j]):
                    gw = lines[i+j]
                    break
        if 'ELEVATION' in l and i+1 < len(lines):
            if re.match(r'^[0-9\.]+$', lines[i+1]):
                el = lines[i+1]
                
    if hole_no and (hole_no.startswith('NH-') or hole_no.startswith('GB-')):
        if hole_no not in hole_data:
            hole_data[hole_no] = {
                'x': coord_x,
                'y': coord_y,
                'gw': gw,
                'el': el
            }

# Update excel
excel_path = r'04_METADATA\borehole_register.xlsx'
wb = openpyxl.load_workbook(excel_path)
ws = wb.active

for row in ws.iter_rows(min_row=2):
    bh = str(row[0].value)
    if bh in hole_data:
        info = hole_data[bh]
        if info['x']: row[2].value = info['x']
        if info['y']: row[3].value = info['y']
        if info['el'] and not row[4].value: row[4].value = float(info['el'])
        if info['gw']: row[6].value = float(info['gw'])

wb.save(excel_path)
print("Enriched 1공구 & 차량기지 coordinates and groundwater levels in excel successfully.")
