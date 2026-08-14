import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

html_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Extract intersectionData
m = re.search(r'const intersectionData = (\[.*?\]);', html, re.DOTALL)
idata = json.loads(m.group(1))

# Extract stnDetail - it's more complex, let's grab manually
m2 = re.search(r'const stnDetail = (\{.*?\});', html, re.DOTALL)
stn_text = m2.group(1)

# Build a STA lookup from intersectionData
# Each intersection has startSta, endSta, and corresponding stnA/stnB/ratio pairs
# We need to build a sorted STA-to-station mapping for each tool

# Build ordered STA references from intersectionData
for tool in ["1공구", "2공구"]:
    items = [i for i in idata if i['tool'] == tool]
    items.sort(key=lambda x: x['startSta'])
    print(f"\n=== {tool} STA reference points ===")
    for item in items:
        print(f"  STA {item['startSta']:10.1f} -> stnA={item['startStnA']} stnB={item['startStnB']} ratio={item['startRatio']:.4f}")
        print(f"  STA {item['endSta']:10.1f} -> stnA={item['endStnA']} stnB={item['endStnB']} ratio={item['endRatio']:.4f}")

# Now let's look at the node sequence paths for each tool
# 1공구 path uses sequences pRW/pRE, 2공구 uses pBN/pBS
m_seq = re.search(r'const sequences = (\{.*?\});', html, re.DOTALL)
if m_seq:
    seqs = json.loads(m_seq.group(1))
    print("\n=== sequences keys ===")
    for k, v in seqs.items():
        print(f"  {k}: {len(v)} nodes -> {v[:5]}...{v[-5:]}")
