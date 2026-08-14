import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Header HTML
hdr_old = """  <select class="quick-nav-select" id="quick-nav">
    <option value="">정거장 바로가기...</option>
  </select>"""

hdr_new = """  <select class="quick-nav-select" id="quick-nav">
    <option value="">정거장 바로가기...</option>
  </select>
  <select class="quick-nav-select" id="intersection-quick-nav">
    <option value="">교차로 바로가기...</option>
  </select>"""

if 'id="intersection-quick-nav"' not in text:
    text = text.replace(hdr_old, hdr_new, 1)

# 2. Populate options inside renderIntersections()
ri_old = "function renderIntersections() {"
ri_pop = """function renderIntersections() {
  const intersectionQuickNav = document.getElementById("intersection-quick-nav");
  if (intersectionQuickNav) {
    intersectionQuickNav.innerHTML = '<option value="">교차로 바로가기...</option>';
    intersectionData.forEach(item => {
      const opt = document.createElement("option");
      opt.value = `${item.tool}_${item.no}`;
      opt.textContent = `[${item.tool} #${item.no}] ${item.name}`;
      intersectionQuickNav.appendChild(opt);
    });
  }"""

if "intersectionQuickNav.innerHTML" not in text:
    text = text.replace(ri_old, ri_pop, 1)

# 3. Add change event listener near quickNav listener
qn_listener_old = """quickNav.addEventListener("change", (e) => {
  if (e.target.value) {
    selectStation(e.target.value);
  }
});"""

qn_listener_new = """quickNav.addEventListener("change", (e) => {
  if (e.target.value) {
    selectStation(e.target.value);
  }
});

const intersectionQuickNavEl = document.getElementById("intersection-quick-nav");
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

if "intersectionQuickNavEl.addEventListener" not in text:
    text = text.replace(qn_listener_old, qn_listener_new, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Added intersection quick nav successfully!")
