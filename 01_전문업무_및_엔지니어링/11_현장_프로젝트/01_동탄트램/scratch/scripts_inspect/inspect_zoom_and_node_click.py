import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Inspect focusCoordinates function
m_focus = re.search(r'function focusCoordinates[\s\S]*?\n\}', text)
if m_focus:
    print("focusCoordinates implementation:")
    print(m_focus.group(0))

# 2. Inspect node circle click event in renderInteractiveElements
m_node_click = re.search(r'circle\.addEventListener\("click"[\s\S]*?\n\s*\}\);', text)
if m_node_click:
    print("\nNode circle click event:")
    print(m_node_click.group(0))

# 3. Inspect SVG inner zoom group container
m_viewport = re.search(r'<svg[\s\S]*?<g id="([^"]+)"', text)
if m_viewport:
    print(f"\nFirst inner <g> container in SVG: id='{m_viewport.group(1)}'")

# Check where intersection-pulse-overlay is added
m_pulse = re.search(r'document\.getElementById\("intersection-pulse-overlay"[\s\S]*?appendChild\([^)]+\);', text)
if m_pulse:
    print("\nintersection-pulse-overlay parent container:")
    print(m_pulse.group(0))
