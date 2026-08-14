import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Check nodes keys in JS
m_nodes = re.search(r'const nodes = (\{[\s\S]*?\});', text)
if m_nodes:
    print("Found nodes definition in JS")

# Check selectStation function
m_sel = re.search(r'function selectStation[\s\S]*?renderStationTargetOverlay[\s\S]*?\n\}', text)
if m_sel:
    print("Found selectStation function:")
    print(m_sel.group(0)[:500])

# Check renderStationTargetOverlay function
m_render = re.search(r'function renderStationTargetOverlay[\s\S]*?\n\}', text)
if m_render:
    print("Found renderStationTargetOverlay function:")
    print(m_render.group(0)[:600])

# Check SVG layer order in HTML
m_svg = re.search(r'<svg id="map-svg"[\s\S]*?</svg>', text)
if m_svg:
    print("\nSVG Layer Structure:")
    lines = m_svg.group(0).split('\n')
    for line in lines:
        if '<g' in line or '</svg>' in line:
            print("  ", line.strip())
