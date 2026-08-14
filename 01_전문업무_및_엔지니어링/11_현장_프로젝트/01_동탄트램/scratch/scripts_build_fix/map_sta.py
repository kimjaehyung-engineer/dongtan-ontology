import sys
import os
import re
import json
import glob

sys.stdout.reconfigure(encoding='utf-8')

search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)

if not files:
    print("V1 HTML file not found!")
    sys.exit(1)

file_v1 = files[0]
print("Found V1 HTML:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    v1 = f.read()

# Load station nodes
nodes_pos = v1.find('const nodes =')
end_nodes = v1.find('};', nodes_pos)
nodes_raw = v1[nodes_pos:end_nodes]
nodes = {}
for m in re.finditer(r'"([^"]+)":\s*\{\s*"x":\s*([\d\.]+),\s*"y":\s*([\d\.]+)\s*\}', nodes_raw):
    nodes[m.group(1)] = {"x": float(m.group(2)), "y": float(m.group(3))}

# Helper to parse KM string into meters
def parse_km(km_str):
    km_str = str(km_str).replace('KP:', '').strip()
    # clean trailing text
    km_str = re.sub(r'\s*\([^)]*\)', '', km_str)
    if '+' in km_str:
        parts = km_str.split('+')
        try:
            return float(parts[0]) * 1000 + float(re.findall(r'[\d\.]+', parts[1])[0])
        except:
            return None
    else:
        try:
            val = float(re.findall(r'[\d\.]+', km_str)[0])
            return val * 1000 if val < 100 else val
        except:
            return None

# Extract stnDetail entries
stn_pos = v1.find('const stnDetail =')
end_stn = v1.find('};', stn_pos)
stn_raw = v1[stn_pos:end_stn]

station_sta = []
for stn_id, node in nodes.items():
    pos = stn_raw.find(f'"{stn_id}":')
    sta_m = None
    km_str = ""
    if pos != -1:
        snippet = stn_raw[pos:pos+300]
        km_match = re.search(r'km:\s*"([^"]+)"', snippet)
        if km_match:
            km_str = km_match.group(1)
            sta_m = parse_km(km_str)
            
    station_sta.append({"id": stn_id, "x": node["x"], "y": node["y"], "km_str": km_str, "sta_m": sta_m})

print(f"Total station nodes: {len(station_sta)}")
for s in station_sta:
    print(f"[{s['id']:15s}] (x:{s['x']:6.1f}, y:{s['y']:6.1f}) => KM: {s['km_str']:15s} | STA(m): {s['sta_m']}")
