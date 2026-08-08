import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

m_idata = re.search(r'const intersectionData = (\[.*?\]);', text, re.DOTALL)
idata = json.loads(m_idata.group(1))

m_cdata = re.search(r'const constructionSections = (\[.*?\]);', text, re.DOTALL)
cdata = json.loads(m_cdata.group(1))

total_matches = 0
for sec in cdata:
    sec_tool = sec['tool']
    s_start = sec['startSta']
    s_end = sec['endSta']
    
    matches = [i for i in idata if i['tool'] == sec_tool and not (i['endSta'] < s_start or i['startSta'] > s_end)]
    total_matches += len(matches)
    print(f"[{sec['tool']}] {sec['section']} (STA {s_start}~{s_end}m) -> {len(matches)} intersections")

print(f"\nTotal intersection matches across 28 sections: {total_matches}")
