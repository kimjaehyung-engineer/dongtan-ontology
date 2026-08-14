import sys
import os
import glob
import re

sys.stdout.reconfigure(encoding='utf-8')

# Find V1 HTML file
search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Fixing badge bounds and font size in V1 HTML:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace badge rendering block inside renderIntersections
old_badge_code = """      const textStr = `${item.name.replace(/\\s+/g, '')} [${item.avgLen}m]`;
      const rectW = Math.max(26, textStr.length * 1.95 + 4);
      const rectH = 5.0;

      const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      rect.setAttribute("x", -rectW / 2);
      rect.setAttribute("y", -rectH / 2);
      rect.setAttribute("width", rectW);
      rect.setAttribute("height", rectH);
      rect.setAttribute("rx", "1.2");
      rect.setAttribute("fill", badgeBg);
      rect.setAttribute("stroke", lineColor);
      rect.setAttribute("stroke-width", "0.5");
      rect.setAttribute("filter", "drop-shadow(0 1px 2px rgba(0,0,0,0.25))");

      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", "0");
      text.setAttribute("y", "1.3");
      text.setAttribute("text-anchor", "middle");
      text.setAttribute("dominant-baseline", "middle");
      text.setAttribute("font-family", "Noto Sans KR");
      text.setAttribute("font-size", "3.3px");
      text.setAttribute("font-weight", "700");
      text.setAttribute("fill", textColor);
      text.textContent = textStr;"""

new_badge_code = """      const textStr = `${item.name.replace(/\\s+/g, '')} [${item.avgLen}m]`;
      
      // Calculate precise text width to prevent any box clipping
      let strW = 0;
      for (let c = 0; c < textStr.length; c++) {
        strW += textStr.charCodeAt(c) > 127 ? 2.3 : 1.35;
      }
      const rectW = Math.max(20, strW + 3.8);
      const rectH = 3.8;

      const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      rect.setAttribute("x", -rectW / 2);
      rect.setAttribute("y", -rectH / 2);
      rect.setAttribute("width", rectW);
      rect.setAttribute("height", rectH);
      rect.setAttribute("rx", "0.9");
      rect.setAttribute("fill", badgeBg);
      rect.setAttribute("stroke", lineColor);
      rect.setAttribute("stroke-width", "0.4");
      rect.setAttribute("filter", "drop-shadow(0 1px 1.5px rgba(0,0,0,0.2))");

      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", "0");
      text.setAttribute("y", "0.1");
      text.setAttribute("text-anchor", "middle");
      text.setAttribute("dominant-baseline", "central");
      text.setAttribute("font-family", "Noto Sans KR");
      text.setAttribute("font-size", "2.3px");
      text.setAttribute("font-weight", "700");
      text.setAttribute("fill", textColor);
      text.textContent = textStr;"""

if 'rectH = 5.0;' in content or 'font-size", "3.3px"' in content:
    pos_start = content.find("const textStr =")
    pos_end = content.find("labelBadge.appendChild(text);", pos_start) + len("labelBadge.appendChild(text);")
    content = content[:pos_start] + new_badge_code + content[pos_end:]
    print("Successfully replaced badge rendering code!")

with open(file_v1, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished updating V1 HTML with compact badge box and font size!")
