import sys
import os
import glob
import re
import json

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

# Station KP mapping
stn_kp = {
    # pRW (병점선 ~ 동탄역)
    "301": 23.0,
    "302": 3210.0,
    "303": 3705.0,
    "304": 4663.0,
    "305": 5410.0,
    "306": 6290.0,
    "307": 7415.0,
    "동탄역": 8505.0,
    
    # pRE (동탄역 ~ 차량기지) - CORRECT MONOTONIC SEQUENCE: 205 -> 206 -> 207 -> 208 -> 209 -> 210 -> vehicle-depot
    "202": 9710.0,
    "203": 11127.0,
    "204": 12106.0,
    "205": 13310.0,
    "206": 13990.0,
    "207": 15253.0,
    "208": 16120.0,
    "209": 16884.0,
    "210": 17540.0,
    "vehicle-depot": 17818.31,
    
    # pBN (망포역 ~ 동탄역)
    "S01": 124.0,
    "S02": 839.0,
    "101": 1997.0,
    "102": 3207.0,
    "103": 4080.0,
    "104": 4798.0,
    "105": 5263.0,
    "106": 6046.0,
    "107": 7447.0,
    
    # pBS (동탄역 ~ 오산대역)
    "108": 8887.0,
    "109": 9933.0,
    "110": 10906.0,
    "111": 11556.0,
    "112": 12175.0,
    "113": 13185.0,
    "114": 14295.0,
    "115": 15322.0,
    "116": 16173.0,
    "117": 17220.0
}

# Sequences with correct monotonic station order
seq_routes = {
    "pRW": ["301", "302", "303", "304", "305", "306", "307", "동탄역"],
    "pRE": ["동탄역", "202", "203", "204", "205", "206", "207", "208", "209", "210", "vehicle-depot"],
    "pBN": ["S01", "S02", "101", "102", "103", "104", "105", "106", "107", "동탄역"],
    "pBS": ["동탄역", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117"]
}

def get_point_on_path(seq_key, target_sta):
    stn_list = seq_routes[seq_key]
    # Build list of valid stations with KP and coords
    valid = []
    for stn_id in stn_list:
        kp = stn_kp.get(stn_id)
        pt = nodes.get(stn_id)
        if kp is not None and pt is not None:
            valid.append({"id": stn_id, "kp": kp, "x": pt["x"], "y": pt["y"]})
            
    if not valid:
        return {"x": 0, "y": 0}
        
    if target_sta <= valid[0]["kp"]:
        return {"x": valid[0]["x"], "y": valid[0]["y"]}
    if target_sta >= valid[-1]["kp"]:
        return {"x": valid[-1]["x"], "y": valid[-1]["y"]}
        
    for i in range(len(valid) - 1):
        s1 = valid[i]
        s2 = valid[i+1]
        if s1["kp"] <= target_sta <= s2["kp"]:
            ratio = (target_sta - s1["kp"]) / (s2["kp"] - s1["kp"]) if s2["kp"] != s1["kp"] else 0
            ix = s1["x"] + (s2["x"] - s1["x"]) * ratio
            iy = s1["y"] + (s2["y"] - s1["y"]) * ratio
            return {"x": round(ix, 1), "y": round(iy, 1)}
            
    return {"x": valid[0]["x"], "y": valid[0]["y"]}

# Load intersections
with open(r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\intersections.json', 'r', encoding='utf-8') as f:
    intersections = json.load(f)

print(f"Loaded {len(intersections)} intersections.")

for item in intersections:
    tool = item["tool"]
    mid_sta = (item["startSta"] + item["endSta"]) / 2.0
    
    if tool == "1공구":
        seq_key = "pRW" if mid_sta <= 8500 else "pRE"
    else:
        seq_key = "pBN" if mid_sta <= 8500 else "pBS"
        
    p_start = get_point_on_path(seq_key, item["startSta"])
    p_end = get_point_on_path(seq_key, item["endSta"])
    p_mid = get_point_on_path(seq_key, mid_sta)
    
    item["x1"] = p_start["x"]
    item["y1"] = p_start["y"]
    item["x2"] = p_end["x"]
    item["y2"] = p_end["y"]
    item["x"] = p_mid["x"]
    item["y"] = p_mid["y"]

print("\n--- Inspect 1공구 #35~#45 after correct monotonic sequence fix ---")
for item in intersections:
    if item["tool"] == "1공구" and 35 <= item["no"] <= 45:
        print(f"1공구 #{item['no']:2d} | {item['name']:25s} | STA: {item['startSta']}~{item['endSta']}m => (x:{item['x']}, y:{item['y']}) [x1:{item['x1']}, y1:{item['y1']} -> x2:{item['x2']}, y2:{item['y2']}]")

# Save to temp JSON
with open(r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\intersections_segments_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(intersections, f, ensure_ascii=False, indent=2)

print("\nSaved intersections_segments_fixed.json")
