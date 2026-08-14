import sys
import os
import glob

sys.stdout.reconfigure(encoding='utf-8')

search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Target V1 HTML file:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add toggle-nodes checkbox in layer panel
checkbox_nodes = '<label class="layer-item">\n      <input type="checkbox" id="toggle-nodes" checked> 정거장 노드 마커\n    </label>'
target_labels_checkbox = '<label class="layer-item">\n      <input type="checkbox" id="toggle-labels" checked> 정거장 명칭\n    </label>'

if 'toggle-nodes' not in content:
    content = content.replace(target_labels_checkbox, checkbox_nodes + '\n    ' + target_labels_checkbox)
    print("Added toggle-nodes checkbox to layer panel.")

# 2. Add event listener for toggle-nodes
listener_nodes = 'document.getElementById("toggle-nodes").addEventListener("change", (e) => {\n  document.getElementById("nodes-group").style.display = e.target.checked ? "block" : "none";\n});'
target_labels_listener = 'document.getElementById("toggle-labels").addEventListener("change", (e) => {'

if 'toggle-nodes' in content and 'document.getElementById("toggle-nodes").addEventListener' not in content:
    content = content.replace(target_labels_listener, listener_nodes + '\n' + target_labels_listener)
    print("Added toggle-nodes event listener.")

# Write back to V1 HTML
with open(file_v1, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated V1 HTML with toggle-nodes layer functionality!")
