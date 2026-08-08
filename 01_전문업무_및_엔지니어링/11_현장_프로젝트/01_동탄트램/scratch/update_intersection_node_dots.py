import sys
import os
import glob
import re

sys.stdout.reconfigure(encoding='utf-8')

search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Updating V1 HTML file:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace cNode attributes in JS
old_cnode_code = """      const cNode = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      cNode.setAttribute("cx", item.x);
      cNode.setAttribute("cy", item.y);
      cNode.setAttribute("r", "2.2");
      cNode.setAttribute("fill", lineColor);
      cNode.setAttribute("stroke", "#ffffff");
      cNode.setAttribute("stroke-width", "0.8");"""

new_cnode_code = """      const cNode = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      cNode.setAttribute("cx", item.x);
      cNode.setAttribute("cy", item.y);
      cNode.setAttribute("r", "1.1");
      cNode.setAttribute("fill", "#111111");
      cNode.setAttribute("stroke", "#ffffff");
      cNode.setAttribute("stroke-width", "0.4");"""

if 'cNode.setAttribute("r", "2.2")' in content:
    content = content.replace(old_cnode_code, new_cnode_code)
    print("Updated intersection cNode radius (2.2 -> 1.1) and color to black (#111111)!")

with open(file_v1, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated V1 HTML!")
