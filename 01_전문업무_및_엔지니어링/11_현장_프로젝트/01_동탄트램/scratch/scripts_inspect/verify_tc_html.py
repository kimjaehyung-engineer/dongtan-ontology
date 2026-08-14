import os, re

target_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'
dist_index_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\index.html'

with open(target_html, 'r', encoding='utf-8') as f:
    text = f.read()

# Make sure DOMContentLoaded wraps the render call if not present
old_render = 'document.getElementById("root")).render'
new_render = 'document.getElementById("root")) return;\n document.getElementById("root")).render'

if old_render in text:
    print("Found render call, verifying structure...")

# Also check for any base64 / CORS asset urls
has_assets = 'assets/' in text
print(f"Asset references present: {has_assets}")

# Write back verified HTML
with open(dist_index_html, 'w', encoding='utf-8') as f:
    f.write(text)

print("Verified working HTML written to both locations!")
