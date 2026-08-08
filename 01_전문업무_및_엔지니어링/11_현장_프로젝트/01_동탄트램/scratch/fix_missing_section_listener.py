import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = """const intersectionQuickNavEl = document.getElementById("intersection-quick-nav");
if (intersectionQuickNavEl) {
  intersectionQuickNavEl.addEventListener("change", (e) => {
    const val = e.target.value;
    if (val) {
      const parts = val.split("_");
      const tool = parts[0];
      const no = parseInt(parts[1], 10);
      const item = intersectionData.find(i => i.tool === tool && i.no === no);
      if (item) {
        selectIntersection(item);
      }
    }
  });
}"""

replacement = target + """

const sectionQuickNavElHeader = document.getElementById("section-quick-nav");
if (sectionQuickNavElHeader) {
  sectionQuickNavElHeader.addEventListener("change", (e) => {
    const val = e.target.value;
    if (val) {
      const secNo = parseInt(val, 10);
      const sec = constructionSections.find(s => s.no === secNo);
      if (sec) {
        selectConstructionSection(sec);
      }
    }
  });
}"""

if "sectionQuickNavElHeader" not in text:
    text = text.replace(target, replacement, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Added sectionQuickNavElHeader event listener!")
else:
    print("sectionQuickNavElHeader already present!")
