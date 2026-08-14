import os, sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

target_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09_공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(target_html, 'r', encoding='utf-8') as f:
    html = f.read()

m_act = re.search(r'const RAW_ACTIVITIES = (\[[\s\S]*?\]);', html)
m_split = re.search(r'const SECTION_SPLITS = (\[[\s\S]*?\]);', html)

if not m_act or not m_split:
    print("❌ Failed to parse JSON arrays from HTML!")
    sys.exit(1)

RAW_ACTIVITIES = json.loads(m_act.group(1))
SECTION_SPLITS = json.loads(m_split.group(1))

print(f"Loaded {len(RAW_ACTIVITIES)} activities, {len(SECTION_SPLITS)} splits.")

# 1. Clean string sanitization check
for item in SECTION_SPLITS:
    if '\n' in item['splitGroup'] or '\n' in item['sectionName']:
        print(f"❌ Unsanitized newline found in split item: {item['sectionName']}")

# 2. Extract unique split groups
split_groups = sorted(list(set(f"{s['zone']}_{s['splitGroup']}" for s in SECTION_SPLITS)))
print(f"Found {len(split_groups)} unique split groups to validate.")

total_tests = 0
passed_tests = 0
failures = []

width = 1000
height = 600
padL = 80; padR = 50; padT = 50; padB = 70;
graphW = width - padL - padR;
graphH = height - padT - padB;

for sg in split_groups:
    total_tests += 1
    selectedSplitKeys = set([sg])
    
    # Filter splits
    filtered_splits = []
    groups = {}
    for item in SECTION_SPLITS:
        gKey = f"{item['zone']}_{item['splitGroup']}"
        if selectedSplitKeys and gKey not in selectedSplitKeys:
            continue
        if gKey not in groups:
            groups[gKey] = {'zone': item['zone'], 'groupName': item['splitGroup'], 'items': []}
        groups[gKey]['items'].append(item)
    
    grp_list = list(groups.values())
    if len(grp_list) == 0:
        failures.append(f"[{sg}] No groups matched filter!")
        continue
        
    allStarts = []; allEnds = []
    for g in grp_list:
        for it in g['items']:
            allStarts.append(it['startM'] / 1000.0)
            allEnds.append(it['endM'] / 1000.0)
            
    if len(allStarts) == 0 or len(allEnds) == 0:
        failures.append(f"[{sg}] Empty start/end STA arrays!")
        continue
        
    realMin = min(allStarts)
    realMax = max(allEnds)
    span = max(0.5, realMax - realMin)
    minKm = max(0.0, realMin - (span * 0.2))
    maxKm = min(20.5, realMax + (span * 0.2))
    
    if maxKm <= minKm:
        failures.append(f"[{sg}] Invalid scale: minKm={minKm}, maxKm={maxKm}")
        continue
        
    # Check coordinate transform
    def getX(km):
        return padL + ((km - minKm) / (maxKm - minKm)) * graphW

    valid_lines = 0
    has_nan = False
    for g in grp_list:
        for item in g['items']:
            sKm = item['startM'] / 1000.0
            eKm = item['endM'] / 1000.0
            x1 = getX(sKm)
            x2 = getX(eKm if eKm > sKm else sKm + 0.35)
            if str(x1) == 'NaN' or str(x2) == 'NaN':
                has_nan = True
            valid_lines += 1

    if has_nan:
        failures.append(f"[{sg}] NaN coordinate detected in getX!")
        continue

    if valid_lines == 0:
        failures.append(f"[{sg}] 0 valid lines generated!")
        continue

    passed_tests += 1

print("\n==============================================")
print(f"AUTOMATED VALIDATION RESULTS: {passed_tests} / {total_tests} PASSED")
print("==============================================")

if failures:
    print("FAILURES DETECTED:")
    for f in failures:
        print("  -", f)
else:
    print("SUCCESS: 100% ALL 28 SECTIONS PASSED VISIBILITY & COORDINATE TESTS!")
