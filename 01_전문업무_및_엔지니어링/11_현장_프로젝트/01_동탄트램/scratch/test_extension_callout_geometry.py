import sys, json, math, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

m_cdata = re.search(r'const constructionSections = (\[.*?\]);', text, re.DOTALL)
cdata = json.loads(m_cdata.group(1))

print(f"Total construction sections: {len(cdata)}")

# Test calculating extension callout points for a section
for sec in cdata[:5]:
    # We have startStnA, startStnB, startRatio, endStnA, endStnB, endRatio
    print(f"[{sec['tool']}] {sec['section']}: {sec['startStnA']}~{sec['startStnB']} ({sec['startRatio']}) -> {sec['endStnA']}~{sec['endStnB']} ({sec['endRatio']})")
