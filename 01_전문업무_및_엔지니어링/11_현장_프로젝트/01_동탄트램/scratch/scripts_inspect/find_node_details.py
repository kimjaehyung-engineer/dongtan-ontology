import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Search for station node circle generation or CSS
print("=== Searching for node elements in SVG / HTML / CSS / JS ===")

# Search CSS selectors for nodes
css_nodes = re.findall(r'(\.[a-zA-Z0-9_-]*node[a-zA-Z0-9_-]*\s*\{[^}]*\})', text, re.IGNORECASE)
print("\nCSS rules matching node:")
for c in css_nodes[:10]:
    print(" ", c)

# Search JS circle creation
js_circles = re.findall(r'<circle[^>]*>', text)
print(f"\nDirect SVG <circle> tags in HTML: {len(js_circles)}")
for circle in js_circles[:10]:
    print(" ", circle)

# Search JS code rendering circles inside nodes-group
nodes_grp_idx = text.find('nodes-group')
while nodes_grp_idx != -1:
    print(f"\n--- nodes-group occurrence at {nodes_grp_idx} ---")
    print(text[max(0, nodes_grp_idx-100):nodes_grp_idx+400])
    nodes_grp_idx = text.find('nodes-group', nodes_grp_idx + 1)
