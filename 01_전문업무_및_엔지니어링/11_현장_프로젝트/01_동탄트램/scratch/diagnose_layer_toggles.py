import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Find ALL toggle listener code
print("=== ALL toggle-bg listener contexts ===")
for m in re.finditer(r'toggle-bg', text):
    pos = m.start()
    ctx = text[max(0,pos-80):pos+200]
    print(f"\n--- Position {pos} ---")
    print(ctx)

# 2. Check SVG group IDs that layers target
print("\n\n=== SVG Group IDs ===")
svg_groups = ['bg-map', 'routes-group', 'nodes-group', 'labels-group', 'distances-group', 'turnouts-group', 'intersection-lines-group', 'intersection-labels-group', 'construction-sections-group']
for gid in svg_groups:
    count = text.count(f'id="{gid}"')
    print(f"  id=\"{gid}\": {count} occurrences")

# 3. Check if layer listeners are inside or outside DOMContentLoaded
script_start = text.find('<script>')
script_end = text.find('</script>')
js_block = text[script_start:script_end]

# Find the layer toggle code position relative to DOMContentLoaded
toggle_pos = js_block.find('"toggle-bg"')
dom_positions = [m.start() for m in re.finditer(r'DOMContentLoaded', js_block)]
print(f"\n=== Layer toggle position vs DOMContentLoaded ===")
print(f"  toggle-bg at JS offset: {toggle_pos}")
print(f"  DOMContentLoaded positions: {dom_positions}")

# Check if toggle code is OUTSIDE any function (top-level)
# Find the function scope around toggle-bg
before_toggle = js_block[max(0,toggle_pos-500):toggle_pos]
print(f"\n=== 500 chars before toggle-bg ===")
print(before_toggle)
