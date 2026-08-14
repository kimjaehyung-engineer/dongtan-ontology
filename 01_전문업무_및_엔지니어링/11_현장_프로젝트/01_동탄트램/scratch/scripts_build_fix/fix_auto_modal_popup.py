import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove openIntersectionModal from card event listener in renderDrawerList
old_card_click = """card.addEventListener("click", () => {
      selectIntersection(item);
      openIntersectionModal(item);
    });"""

new_card_click = """card.addEventListener("click", () => {
      selectIntersection(item);
    });"""

if old_card_click in content:
    content = content.replace(old_card_click, new_card_click)
    print("Removed openIntersectionModal from drawer card click event!")

# 2. Remove openIntersectionModal from gLine & gLabel click events in renderIntersectionOverlay
old_gline_click = """gLine.addEventListener("click", (e) => {
        e.stopPropagation();
        selectIntersection(item);
      openIntersectionModal(item);
      });"""

new_gline_click = """gLine.addEventListener("click", (e) => {
        e.stopPropagation();
        selectIntersection(item);
      });"""

if old_gline_click in content:
    content = content.replace(old_gline_click, new_gline_click)
    print("Removed openIntersectionModal from map gLine click event!")

old_glabel_click = """gLabel.addEventListener("click", (e) => {
        e.stopPropagation();
        selectIntersection(item);
      openIntersectionModal(item);
      });"""

new_glabel_click = """gLabel.addEventListener("click", (e) => {
        e.stopPropagation();
        selectIntersection(item);
      });"""

if old_glabel_click in content:
    content = content.replace(old_glabel_click, new_glabel_click)
    print("Removed openIntersectionModal from map gLabel click event!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished removing automatic modal popups from card & map clicks in V1 HTML!")
