import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Search for nodes rendering logic or CSS styles for station nodes
matches = re.findall(r'.*node.*', text, re.IGNORECASE)
print("Matches containing 'node':", len(matches))

# Look for node circle rendering in JS
node_draw_idx = text.find('nodes-group')
if node_draw_idx != -1:
    print("\n=== Context around 'nodes-group' ===")
    print(text[node_draw_idx-200:node_draw_idx+800])
