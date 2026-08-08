import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Extract intersectionData
m_idata = re.search(r'const intersectionData = (\[.*?\]);', text, re.DOTALL)
idata = json.loads(m_idata.group(1))

# Extract constructionSections
m_cdata = re.search(r'const constructionSections = (\[.*?\]);', text, re.DOTALL)
cdata = json.loads(m_cdata.group(1))

print(f"Intersection items: {len(idata)}")
print(f"Construction section items: {len(cdata)}")

# For each construction section, find matching intersections
for sec in cdata[:8]:
    sec_tool = sec['tool']
    s_start = sec['startSta']
    s_end = sec['endSta']
    
    # Matching intersections in same tool where STA overlaps
    matches = []
    for item in idata:
        if item['tool'] == sec_tool:
            # Overlap check or inside check
            if not (item['endSta'] < s_start or item['startSta'] > s_end):
                matches.append(item)
                
    print(f"\n========================================")
    print(f"[{sec['tool']}] {sec['section']} (STA {s_start}~{s_end}m, len={sec['length']}m)")
    print(f"  Matching Intersections ({len(matches)}개):")
    for m in matches:
        print(f"    - [{m['tool']} #{m['no']}] {m['name']} (STA {m['startSta']}~{m['endSta']}m)")
