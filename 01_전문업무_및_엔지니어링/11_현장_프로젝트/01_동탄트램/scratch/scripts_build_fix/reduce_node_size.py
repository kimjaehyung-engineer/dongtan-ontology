import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace radius (r) by 30% reduction and make stroke-width thinner (e.g. 0.4px ~ 0.5px)
old_circle_block = """    circle.setAttribute("r", isTransfer ? "4" : "2.8");
    circle.setAttribute("fill", "#facc15");
    circle.setAttribute("stroke", "#000000");
    circle.setAttribute("stroke-width", "1.2");"""

new_circle_block = """    circle.setAttribute("r", isTransfer ? "2.8" : "1.95");
    circle.setAttribute("fill", "#facc15");
    circle.setAttribute("stroke", "#000000");
    circle.setAttribute("stroke-width", "0.4");"""

if old_circle_block in text:
    text = text.replace(old_circle_block, new_circle_block, 1)
    print("✓ Reduced node radius by 30% (transfer: 2.8, regular: 1.95) and set stroke-width to thin 0.4px")
else:
    print("!! Could not find exact old_circle_block, using regex replacement...")
    text = re.sub(
        r'circle\.setAttribute\("r",\s*isTransfer\s*\?\s*"[^"]+"\s*:\s*"[^"]+"\);[\s\n]*circle\.setAttribute\("fill",\s*"#facc15"\);[\s\n]*circle\.setAttribute\("stroke",\s*"#000000"\);[\s\n]*circle\.setAttribute\("stroke-width",\s*"[^"]+"\);',
        'circle.setAttribute("r", isTransfer ? "2.8" : "1.95");\n    circle.setAttribute("fill", "#facc15");\n    circle.setAttribute("stroke", "#000000");\n    circle.setAttribute("stroke-width", "0.4");',
        text
    )

# Also update cNode stroke-width if present
text = text.replace('cNode.setAttribute("stroke-width", "0.4");', 'cNode.setAttribute("stroke-width", "0.35");')

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("✅ Station node size and border thickness update complete!")
