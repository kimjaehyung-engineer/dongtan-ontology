import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace station node circle attributes
# Replace fill and stroke in renderInteractiveElements
old_circle_block = """    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", pt.x);
    circle.setAttribute("cy", pt.y);
    circle.setAttribute("r", isTransfer ? "4" : "2.5");
    circle.setAttribute("fill", isTransfer ? "#a855f7" : color);
    circle.setAttribute("stroke", "#ffffff");
    circle.setAttribute("stroke-width", "1");"""

new_circle_block = """    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", pt.x);
    circle.setAttribute("cy", pt.y);
    circle.setAttribute("r", isTransfer ? "4" : "2.8");
    circle.setAttribute("fill", "#facc15");
    circle.setAttribute("stroke", "#000000");
    circle.setAttribute("stroke-width", "1.2");"""

if old_circle_block in text:
    text = text.replace(old_circle_block, new_circle_block, 1)
    print("✓ Updated station node fill to yellow (#facc15) and stroke to black (#000000)")
else:
    print("!! Could not find exact old_circle_block, using regex replacement...")
    text = re.sub(
        r'circle\.setAttribute\("fill",\s*isTransfer\s*\?\s*"[^"]+"\s*:\s*color\);[\s\n]*circle\.setAttribute\("stroke",\s*"#ffffff"\);[\s\n]*circle\.setAttribute\("stroke-width",\s*"1"\);',
        'circle.setAttribute("fill", "#facc15");\n    circle.setAttribute("stroke", "#000000");\n    circle.setAttribute("stroke-width", "1.2");',
        text
    )

# Also update cNode (construction section anchor node circles) if present
old_cnode = 'cNode.setAttribute("stroke", "#ffffff");'
new_cnode = 'cNode.setAttribute("stroke", "#000000");'
if old_cnode in text:
    text = text.replace(old_cnode, new_cnode)
    print("✓ Updated construction anchor node (cNode) stroke to black (#000000)")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("✅ Station node styling update complete!")
