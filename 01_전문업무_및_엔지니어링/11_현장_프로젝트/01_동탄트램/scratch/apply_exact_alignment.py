import sys
import os
import glob
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load exact fixed JSON
with open(r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\intersections_segments_fixed.json', 'r', encoding='utf-8') as f:
    intersections = json.load(f)

# 2. Find V1 HTML file
search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Applying exact alignment to V1 HTML:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

# 3. Replace JS dataset in HTML
js_dataset = json.dumps(intersections, ensure_ascii=False)

start_js_pos = content.find("const intersectionData =")
end_js_pos = content.find("let currentFilterTool = \"all\";", start_js_pos)

if start_js_pos != -1 and end_js_pos != -1:
    content = content[:start_js_pos] + "const intersectionData = " + js_dataset + ";\n\n" + content[end_js_pos:]
    print("Replaced intersectionData dataset in V1 HTML successfully!")

with open(file_v1, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished applying exact route alignment to V1 HTML!")
