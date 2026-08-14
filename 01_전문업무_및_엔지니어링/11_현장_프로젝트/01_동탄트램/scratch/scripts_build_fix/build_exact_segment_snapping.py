import sys
import os
import glob
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

# Station KP mapping with explicit station pairs for each route segment
stn_kp = {
    # 1공구 서측 (pRW)
    "301": 23.0, "302": 3210.0, "303": 3705.0, "304": 4663.0, "305": 5410.0, "306": 6290.0, "307": 7415.0, "동탄역": 8505.0,
    # 1공구 동측 (pRE)
    "202": 9710.0, "203": 11127.0, "204": 12106.0, "205": 13310.0, "206": 13990.0, "207": 15253.0, "208": 16120.0, "209": 16884.0, "210": 17540.0, "vehicle-depot": 17818.31,
    # 2공구 북측 (pBN)
    "S01": 124.0, "S02": 839.0, "101": 1997.0, "102": 3207.0, "103": 4080.0, "104": 4798.0, "105": 5263.0, "106": 6046.0, "107": 7447.0,
    # 2공구 남측 (pBS)
    "108": 8887.0, "109": 9933.0, "110": 10906.0, "111": 11556.0, "112": 12175.0, "113": 13185.0, "114": 14295.0, "115": 15322.0, "116": 16173.0, "117": 17220.0
}

# Monotonic station sequences
sequences = {
    "1공구_서측": ["301", "302", "303", "304", "305", "306", "307", "동탄역"],
    "1공구_동측": ["동탄역", "202", "203", "204", "205", "206", "207", "208", "209", "210", "vehicle-depot"],
    "2공구_북측": ["S01", "S02", "101", "102", "103", "104", "105", "106", "107", "동탄역"],
    "2공구_남측": ["동탄역", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117"]
}

# Pre-calculate station pairs for each intersection
with open(r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\intersections.json', 'r', encoding='utf-8') as f:
    intersections = json.load(f)

def find_segment_pair(tool, sta):
    if tool == "1공구":
        seq_key = "1공구_서측" if sta <= 8505 else "1공구_동측"
    else:
        seq_key = "2공구_북측" if sta <= 8505 else "2공구_남측"
        
    seq = sequences[seq_key]
    
    # Check bounds
    if sta <= stn_kp[seq[0]]:
        return seq[0], seq[0], 0.0
    if sta >= stn_kp[seq[-1]]:
        return seq[-1], seq[-1], 0.0
        
    for i in range(len(seq) - 1):
        stn1 = seq[i]
        stn2 = seq[i+1]
        kp1 = stn_kp[stn1]
        kp2 = stn_kp[stn2]
        if kp1 <= sta <= kp2:
            ratio = (sta - kp1) / (kp2 - kp1) if kp2 != kp1 else 0.0
            return stn1, stn2, ratio
            
    return seq[0], seq[0], 0.0

mapped_intersections = []
for item in intersections:
    s1, s2, r = find_segment_pair(item["tool"], (item["startSta"] + item["endSta"]) / 2.0)
    st1, st2, rt = find_segment_pair(item["tool"], item["startSta"])
    et1, et2, et = find_segment_pair(item["tool"], item["endSta"])
    
    newItem = dict(item)
    newItem["stnA"] = s1
    newItem["stnB"] = s2
    newItem["ratio"] = round(r, 4)
    
    newItem["startStnA"] = st1
    newItem["startStnB"] = st2
    newItem["startRatio"] = round(rt, 4)
    
    newItem["endStnA"] = et1
    newItem["endStnB"] = et2
    newItem["endRatio"] = round(et, 4)
    
    mapped_intersections.append(newItem)

print(f"Mapped {len(mapped_intersections)} intersections with segment pairs.")

# Save to JSON
with open(r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\intersections_dynamic_pairs.json', 'w', encoding='utf-8') as f:
    json.dump(mapped_intersections, f, ensure_ascii=False, indent=2)

print("Saved intersections_dynamic_pairs.json")
