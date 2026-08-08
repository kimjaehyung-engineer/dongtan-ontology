import sys
import os
import re
import json
import glob

sys.stdout.reconfigure(encoding='utf-8')

search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]

with open(file_v1, 'r', encoding='utf-8') as f:
    v1 = f.read()

# Load station nodes
nodes_pos = v1.find('const nodes =')
end_nodes = v1.find('};', nodes_pos)
nodes_raw = v1[nodes_pos:end_nodes]
nodes = {}
for m in re.finditer(r'"([^"]+)":\s*\{\s*"x":\s*([\d\.]+),\s*"y":\s*([\d\.]+)\s*\}', nodes_raw):
    nodes[m.group(1)] = {"x": float(m.group(2)), "y": float(m.group(3))}

# Parse KM helper
def parse_km(km_str):
    km_str = str(km_str).replace('KP:', '').strip()
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

stn_pos = v1.find('const stnDetail =')
end_stn = v1.find('};', stn_pos)
stn_raw = v1[stn_pos:end_stn]

# Build routes sequence
sequences = {
    "1공구_서측": ["301", "302", "303", "304", "305", "306", "307", "동탄역"],
    "1공구_동측": ["동탄역", "202", "203", "204", "205", "208", "207", "206", "209", "210", "vehicle-depot"],
    "2공구_북측": ["S01", "S02", "101", "102", "103", "104", "105", "106", "107", "동탄역"],
    "2공구_남측": ["동탄역", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117"]
}

# Map stations per sequence with STA
sequence_stations = {}
for seq_name, stn_ids in sequences.items():
    stn_list = []
    for stn_id in stn_ids:
        pos = stn_raw.find(f'"{stn_id}":')
        sta_m = None
        if pos != -1:
            snippet = stn_raw[pos:pos+300]
            km_match = re.search(r'km:\s*"([^"]+)"', snippet)
            if km_match:
                sta_m = parse_km(km_match.group(1))
        node = nodes.get(stn_id, {"x": 0, "y": 0})
        stn_list.append({"id": stn_id, "x": node["x"], "y": node["y"], "sta": sta_m})
    sequence_stations[seq_name] = stn_list

# Interpolate function for given STA in a sequence
def interpolate_sta(seq_name, target_sta):
    stns = sequence_stations[seq_name]
    # Filter valid STA stations
    valid_stns = [s for s in stns if s["sta"] is not None]
    if not valid_stns:
        return {"x": 0, "y": 0}
        
    # Check bounds
    if target_sta <= valid_stns[0]["sta"]:
        return {"x": valid_stns[0]["x"], "y": valid_stns[0]["y"]}
    if target_sta >= valid_stns[-1]["sta"]:
        return {"x": valid_stns[-1]["x"], "y": valid_stns[-1]["y"]}
        
    # Find segment
    for i in range(len(valid_stns) - 1):
        s1 = valid_stns[i]
        s2 = valid_stns[i+1]
        if s1["sta"] <= target_sta <= s2["sta"]:
            ratio = (target_sta - s1["sta"]) / (s2["sta"] - s1["sta"]) if s2["sta"] != s1["sta"] else 0
            ix = s1["x"] + (s2["x"] - s1["x"]) * ratio
            iy = s1["y"] + (s2["y"] - s1["y"]) * ratio
            return {"x": round(ix, 1), "y": round(iy, 1)}
            
    return {"x": valid_stns[0]["x"], "y": valid_stns[0]["y"]}

# Load intersections
with open(r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\intersections.json', 'r', encoding='utf-8') as f:
    intersections = json.load(f)

# Calculate x, y for each intersection
for item in intersections:
    mid_sta = (item["startSta"] + item["endSta"]) / 2.0
    tool = item["tool"]
    
    # Decide which sequence to use
    if tool == "1공구":
        # Check if mid_sta is in 1공구 서측 (병점선 ~ 7500) or 동측 (동탄역 이후 7500+)
        if mid_sta <= 7500:
            seq = "1공구_서측"
        else:
            seq = "1공구_동측"
    else: # 2공구
        if mid_sta <= 8500:
            seq = "2공구_북측"
        else:
            seq = "2공구_남측"
            
    pt = interpolate_sta(seq, mid_sta)
    item["x"] = pt["x"]
    item["y"] = pt["y"]

print(f"Interpolated coordinates for all {len(intersections)} intersections!")

# Print first 10
for item in intersections[:10]:
    print(f"[{item['tool']} #{item['no']:2d}] {item['name']:25s} | STA: {item['startSta']}~{item['endSta']} (Mid: {(item['startSta']+item['endSta'])/2:.1f}m) => x:{item['x']}, y:{item['y']} | AvgLen: {item['avgLen']}m")

# Save complete dataset back to JSON
with open(r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\intersections_mapped.json', 'w', encoding='utf-8') as f:
    json.dump(intersections, f, ensure_ascii=False, indent=2)

print("Saved mapped intersections to intersections_mapped.json")
