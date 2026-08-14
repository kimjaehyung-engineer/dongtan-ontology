import sys
import os
import glob
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

# Load V1 HTML
search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]

with open(file_v1, 'r', encoding='utf-8') as f:
    v1 = f.read()

# Load stnDetail
stn_pos = v1.find('const stnDetail =')
end_stn = v1.find('};', stn_pos)
stn_raw = v1[stn_pos:end_stn]

# Load nodes
nodes_pos = v1.find('const nodes =')
end_nodes = v1.find('};', nodes_pos)
nodes_raw = v1[nodes_pos:end_nodes]
nodes = {}
for m in re.finditer(r'"([^"]+)":\s*\{\s*"x":\s*([\d\.]+),\s*"y":\s*([\d\.]+)\s*\}', nodes_raw):
    nodes[m.group(1)] = {"x": float(m.group(2)), "y": float(m.group(3))}

print("=== Nodes ===")
for k, v in nodes.items():
    print(f"[{k:15s}] x:{v['x']:6.1f}, y:{v['y']:6.1f}")

# Check segmentDistances in HTML if any
pos_dist = v1.find('const segmentDistances =')
if pos_dist != -1:
    end_d = v1.find('};', pos_dist)
    print("\n=== segmentDistances ===")
    print(v1[pos_dist:end_d+2])
