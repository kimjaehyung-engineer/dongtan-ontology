import sys
import os
import glob

sys.stdout.reconfigure(encoding='utf-8')

# Target V1 HTML file
search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Fixing missing label appends in V1 HTML:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

target_str = """      text.setAttribute("fill", textColor);
      text.textContent = textStr;

      gLabel.appendChild(leaderLine);"""

replacement_str = """      text.setAttribute("fill", textColor);
      text.textContent = textStr;

      labelBadge.appendChild(rect);
      labelBadge.appendChild(text);

      gLabel.appendChild(leaderLine);"""

if target_str in content:
    content = content.replace(target_str, replacement_str)
    print("Successfully restored labelBadge.appendChild(rect) and labelBadge.appendChild(text)!")

with open(file_v1, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished fixing missing label boxes in V1 HTML!")
