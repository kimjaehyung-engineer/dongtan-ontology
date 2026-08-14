import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

file_v1 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램_노선평면도V1.html'

with open(file_v1, 'r', encoding='utf-8') as f:
    v1 = f.read()

# Inspect stnDetail definition
stn_detail_pos = v1.find('const stnDetail =')
end_stn = v1.find('};', stn_detail_pos)
stn_block = v1[stn_detail_pos:end_stn+2]

# Find all station keys and their km values
print("=== All Stations KP (km chainage) status in V1 HTML ===")

# Parse station blocks in stnDetail
stn_matches = re.findall(r'"([^"]+)":\s*\{([^}]+)\}', stn_block)

kp_dict = {}
for stn_id, content in stn_matches:
    km_match = re.search(r'km:\s*"([^"]+)"', content)
    name_match = re.search(r'name:\s*"([^"]+)"', content)
    
    stn_name = name_match.group(1) if name_match else stn_id
    km_val = km_match.group(1) if km_match else "미상/누락"
    kp_dict[stn_id] = (stn_name, km_val)

# Also check nodes list
nodes_pos = v1.find('const nodes =')
end_nodes = v1.find('};', nodes_pos)
nodes_block = v1[nodes_pos:end_nodes]
all_nodes = re.findall(r'"([^"]+)":\s*\{', nodes_block)

print(f"Total Nodes: {len(all_nodes)}")
print(f"Mapped in stnDetail: {len(kp_dict)}")

print("\n--- Detailed Station KP List ---")
for stn_id in all_nodes:
    if stn_id in kp_dict:
        name, km = kp_dict[stn_id]
        print(f"[{stn_id}] {name} => KP: {km}")
    else:
        print(f"[{stn_id}] => KP: 미설정")
