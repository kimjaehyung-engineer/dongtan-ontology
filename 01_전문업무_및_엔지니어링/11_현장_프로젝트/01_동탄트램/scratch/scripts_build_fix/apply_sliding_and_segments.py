import sys
import os
import json
import glob
import re

sys.stdout.reconfigure(encoding='utf-8')

# Load enriched JSON
with open(r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\intersections_segments.json', 'r', encoding='utf-8') as f:
    intersections = json.load(f)

# Find V1 HTML file
search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Applying to V1 HTML:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add drawer CSS before </head>
css_drawer = """
/* Intersection Sliding Drawer Styling */
.intersection-drawer {
  position: fixed;
  top: 0;
  right: 0;
  width: 440px;
  max-width: 90vw;
  height: 100vh;
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-left: 1.5px solid var(--border-color);
  box-shadow: -8px 0 30px rgba(0,0,0,0.3);
  z-index: 99990;
  display: flex;
  flex-direction: column;
  transform: translateX(100%);
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  color: var(--text-primary);
}
.intersection-drawer.open {
  transform: translateX(0);
}
.drawer-header {
  padding: 1.2rem 1.5rem;
  background: var(--header-bg);
  border-bottom: 1.5px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.drawer-title {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 1.05rem;
  font-weight: 700;
}
.drawer-close-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 1.6rem;
  cursor: pointer;
  line-height: 1;
  transition: color 0.2s;
}
.drawer-close-btn:hover {
  color: var(--text-primary);
}
.drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.drawer-controls {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
#drawer-search {
  width: 100%;
  padding: 0.65rem 1rem;
  border-radius: 8px;
  border: 1.5px solid var(--border-color);
  background: var(--card-bg);
  color: var(--text-primary);
  font-size: 0.85rem;
  outline: none;
}
.drawer-filter-group {
  display: flex;
  gap: 0.4rem;
}
.filter-btn {
  flex: 1;
  padding: 0.4rem 0.6rem;
  font-size: 0.78rem;
  font-weight: 600;
  border-radius: 6px;
  border: 1.5px solid var(--border-color);
  background: var(--panel-bg);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}
.filter-btn.active {
  background: #f97316;
  color: white;
  border-color: #ea580c;
}
.drawer-list {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}
.drawer-item-card {
  background: var(--card-bg);
  border: 1.5px solid var(--border-color);
  border-radius: 10px;
  padding: 0.85rem 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.drawer-item-card:hover, .drawer-item-card.selected {
  border-color: #f97316;
  box-shadow: 0 4px 15px rgba(249, 115, 22, 0.25);
  transform: translateY(-1px);
}
.intersection-route-line {
  transition: stroke-width 0.2s, opacity 0.2s, stroke 0.2s;
  cursor: pointer;
}
.intersection-route-line:hover {
  stroke-width: 6.5px !important;
  opacity: 1 !important;
  filter: drop-shadow(0 0 6px rgba(249, 115, 22, 0.8));
}
.btn-open-drawer-panel {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  background: #ea580c;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 50px;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(234, 88, 12, 0.4);
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}
.btn-open-drawer-panel:hover {
  background: #c2410c;
  transform: translateY(-2px);
}
"""

if '/* Intersection Sliding Drawer Styling */' not in content:
    content = content.replace("</style>", css_drawer + "\n</style>")

# 2. Add Sliding Drawer HTML body before </body>
drawer_html = """
<!-- Sliding Drawer Panel for Intersections -->
<div class="intersection-drawer" id="intersection-drawer">
  <div class="drawer-header">
    <div class="drawer-title">
      <span>🚧</span>
      <span>교차로 시공 공기산출 대시보드</span>
    </div>
    <button class="drawer-close-btn" onclick="closeIntersectionDrawer()">×</button>
  </div>
  
  <div class="drawer-body">
    <!-- Active Selected Item KPI Card -->
    <div id="drawer-active-card">
      <div style="text-align: center; padding: 2rem 1rem; color: var(--text-muted); border: 1.5px dashed var(--border-color); border-radius: 10px;">
        📌 노선 상의 교차로 구간을 선택하거나 아래 목록에서 클릭하세요.
      </div>
    </div>

    <!-- Search & Filter Bar -->
    <div class="drawer-controls">
      <input type="text" id="drawer-search" placeholder="교차로명 또는 번호 검색..." oninput="filterDrawerList()" />
      <div class="drawer-filter-group">
        <button class="filter-btn active" data-tool="all" onclick="setDrawerFilter('all', this)">전체 (94)</button>
        <button class="filter-btn" data-tool="1공구" onclick="setDrawerFilter('1공구', this)">1공구 (49)</button>
        <button class="filter-btn" data-tool="2공구" onclick="setDrawerFilter('2공구', this)">2공구 (45)</button>
      </div>
    </div>

    <!-- Scrollable Intersections List -->
    <div class="drawer-list" id="drawer-list"></div>
  </div>
</div>

<!-- Floating Trigger Button -->
<button class="btn-open-drawer-panel" onclick="openIntersectionDrawer()">
  <span>🚧</span>
  <span>교차로 대시보드 목록</span>
</button>
"""

if 'id="intersection-drawer"' not in content:
    content = content.replace("</body>", drawer_html + "\n</body>")

# 3. Replace JS block with full segment line rendering + sliding panel logic
js_dataset = json.dumps(intersections, ensure_ascii=False)

js_new_logic = """
// --- 교차로 노선 구간 시각화 & 슬라이딩 패널 통합 로직 ---
const intersectionData = """ + js_dataset + """;

let currentFilterTool = "all";

function openIntersectionDrawer() {
  const drawer = document.getElementById("intersection-drawer");
  if (drawer) drawer.classList.add("open");
}

function closeIntersectionDrawer() {
  const drawer = document.getElementById("intersection-drawer");
  if (drawer) drawer.classList.remove("open");
}

function renderIntersections() {
  const group = document.getElementById("intersections-group");
  const toggle = document.getElementById("toggle-intersections");
  if (!group) return;
  group.innerHTML = "";

  if (toggle && !toggle.checked) return;

  intersectionData.forEach(item => {
    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("class", "intersection-segment-group");
    g.setAttribute("data-id", `${item.tool}_${item.no}`);

    const is1Tool = item.tool === "1공구";
    const lineColor = is1Tool ? "#f97316" : "#2563eb";

    // 1. Route Segment Line Overlay (x1, y1 ~ x2, y2)
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", item.x1);
    line.setAttribute("y1", item.y1);
    line.setAttribute("x2", item.x2);
    line.setAttribute("y2", item.y2);
    line.setAttribute("stroke", lineColor);
    line.setAttribute("stroke-width", "4.5");
    line.setAttribute("stroke-linecap", "round");
    line.setAttribute("opacity", "0.85");
    line.setAttribute("class", "intersection-route-line");

    // 2. Terminal Circles at Start & End
    const cStart = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    cStart.setAttribute("cx", item.x1); cStart.setAttribute("cy", item.y1); cStart.setAttribute("r", "1.5");
    cStart.setAttribute("fill", lineColor); cStart.setAttribute("stroke", "#ffffff"); cStart.setAttribute("stroke-width", "0.5");

    const cEnd = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    cEnd.setAttribute("cx", item.x2); cEnd.setAttribute("cy", item.y2); cEnd.setAttribute("r", "1.5");
    cEnd.setAttribute("fill", lineColor); cEnd.setAttribute("stroke", "#ffffff"); cEnd.setAttribute("stroke-width", "0.5");

    // 3. Floating Label Badge at Midpoint (x, y)
    const labelGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    labelGroup.setAttribute("transform", `translate(${item.x}, ${item.y})`);
    
    const textStr = `${item.name.replace(/\\s+/g, '')} [${item.avgLen}m]`;
    const rectW = Math.max(28, textStr.length * 2.0 + 4);
    const rectH = 5.2;

    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("x", -rectW / 2);
    rect.setAttribute("y", -rectH / 2 - 5);
    rect.setAttribute("width", rectW);
    rect.setAttribute("height", rectH);
    rect.setAttribute("rx", "1.2");
    rect.setAttribute("fill", "rgba(255, 255, 255, 0.95)");
    rect.setAttribute("stroke", lineColor);
    rect.setAttribute("stroke-width", "0.5");
    rect.setAttribute("filter", "drop-shadow(0 1px 2px rgba(0,0,0,0.2))");

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", "0");
    text.setAttribute("y", -5 + 1.5);
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("dominant-baseline", "middle");
    text.setAttribute("font-family", "Noto Sans KR");
    text.setAttribute("font-size", "3.4px");
    text.setAttribute("font-weight", "700");
    text.setAttribute("fill", is1Tool ? "#c2410c" : "#1e40af");
    text.textContent = textStr;

    labelGroup.appendChild(rect);
    labelGroup.appendChild(text);

    g.appendChild(line);
    g.appendChild(cStart);
    g.appendChild(cEnd);
    g.appendChild(labelGroup);

    // Hover Events
    g.addEventListener("mouseenter", (e) => {
      showTooltip(e, `<b>[${item.tool} #${item.no}] ${item.name}</b><br>· STA: ${item.startSta}m ~ ${item.endSta}m (총연장 ${item.length}m)<br>· 공법: ${item.method} (${item.stage}단계)<br>· <b>단계별 평균작업연장: ${item.avgLen}m</b>`);
    });
    g.addEventListener("mouseleave", hideTooltip);

    // Click Event: Open Sliding Panel & Select Item
    g.addEventListener("click", (e) => {
      e.stopPropagation();
      selectIntersection(item);
    });

    group.appendChild(g);
  });

  renderDrawerList();
}

function selectIntersection(item) {
  panTo(item.x, item.y);
  openIntersectionDrawer();

  // Render Active KPI Card inside Drawer
  const activeCard = document.getElementById("drawer-active-card");
  if (activeCard) {
    const is1 = item.tool === "1공구";
    activeCard.innerHTML = `
      <div style="background: var(--card-bg); border: 2px solid ${is1 ? '#f97316' : '#3b82f6'}; border-radius: 12px; padding: 1.2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem;">
          <span style="font-size: 0.75rem; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 50px; background: ${is1 ? '#ffedd5' : '#dbeafe'}; color: ${is1 ? '#c2410c' : '#1e40af'};">${item.tool} #${item.no}</span>
          <span style="font-size: 0.75rem; color: var(--text-muted);">${item.code}</span>
        </div>
        <h3 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 0.8rem; color: var(--text-primary);">${item.name}</h3>

        <!-- Key Metric KPI -->
        <div style="background: ${is1 ? 'linear-gradient(135deg, #fff7ed, #ffedd5)' : 'linear-gradient(135deg, #eff6ff, #dbeafe)'}; border-radius: 10px; padding: 0.9rem; text-align: center; margin-bottom: 1rem; border: 1px solid ${is1 ? '#fdba74' : '#93c5fd'};">
          <div style="font-size: 0.75rem; font-weight: 700; color: ${is1 ? '#c2410c' : '#1e40af'}; text-transform: uppercase;">단계별 평균작업연장</div>
          <div style="font-size: 1.8rem; font-weight: 900; color: ${is1 ? '#ea580c' : '#2563eb'}; margin-top: 0.2rem;">${item.avgLen} <span style="font-size: 1rem;">m</span></div>
        </div>

        <table style="width: 100%; border-collapse: collapse; font-size: 0.82rem;">
          <tr style="border-bottom: 1px solid var(--border-color);"><td style="padding: 0.4rem 0; color: var(--text-muted);">체이닝 (STA)</td><td style="padding: 0.4rem 0; font-weight: 600; text-align: right;">${item.startSta}m ~ ${item.endSta}m</td></tr>
          <tr style="border-bottom: 1px solid var(--border-color);"><td style="padding: 0.4rem 0; color: var(--text-muted);">구간 총 연장</td><td style="padding: 0.4rem 0; font-weight: 600; text-align: right;">${item.length}m</td></tr>
          <tr style="border-bottom: 1px solid var(--border-color);"><td style="padding: 0.4rem 0; color: var(--text-muted);">적용 공법</td><td style="padding: 0.4rem 0; font-weight: 600; text-align: right;">${item.method}</td></tr>
          <tr><td style="padding: 0.4rem 0; color: var(--text-muted);">교통처리 단계</td><td style="padding: 0.4rem 0; font-weight: 600; text-align: right;">${item.stage} 단계</td></tr>
        </table>
      </div>
    `;
  }

  // Highlight card in list
  const listItems = document.querySelectorAll(".drawer-item-card");
  listItems.forEach(el => {
    if (el.getAttribute("data-id") === `${item.tool}_${item.no}`) {
      el.classList.add("selected");
      el.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } else {
      el.classList.remove("selected");
    }
  });
}

function setDrawerFilter(tool, btnEl) {
  currentFilterTool = tool;
  document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
  if (btnEl) btnEl.classList.add("active");
  renderDrawerList();
}

function filterDrawerList() {
  renderDrawerList();
}

function renderDrawerList() {
  const drawerList = document.getElementById("drawer-list");
  const searchInput = document.getElementById("drawer-search");
  if (!drawerList) return;

  const query = searchInput ? searchInput.value.trim().toLowerCase() : "";

  const filtered = intersectionData.filter(item => {
    const matchesTool = currentFilterTool === "all" || item.tool === currentFilterTool;
    const matchesQuery = !query || item.name.toLowerCase().includes(query) || String(item.no).includes(query) || item.code.toLowerCase().includes(query);
    return matchesTool && matchesQuery;
  });

  drawerList.innerHTML = "";
  filtered.forEach(item => {
    const card = document.createElement("div");
    card.className = "drawer-item-card";
    card.setAttribute("data-id", `${item.tool}_${item.no}`);

    const is1 = item.tool === "1공구";
    card.innerHTML = `
      <div>
        <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600;">[${item.tool} #${item.no}] ${item.code}</div>
        <div style="font-size: 0.9rem; font-weight: 700; margin-top: 0.1rem; color: var(--text-primary);">${item.name}</div>
        <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem;">STA ${item.startSta}~${item.endSta}m (${item.length}m)</div>
      </div>
      <div style="text-align: right; min-width: 90px;">
        <div style="font-size: 0.68rem; color: var(--text-muted); font-weight: 600;">평균작업연장</div>
        <div style="font-size: 1.15rem; font-weight: 800; color: ${is1 ? '#ea580c' : '#2563eb'};">${item.avgLen}m</div>
        <div style="font-size: 0.7rem; color: var(--text-muted);">${item.stage}단계 (${item.method})</div>
      </div>
    `;

    card.addEventListener("click", () => {
      selectIntersection(item);
    });

    drawerList.appendChild(card);
  });
}
"""

# Replace previous JS logic block
old_js_start = content.find("// --- 교차로 정보")
if old_js_start != -1:
    old_js_end = content.find("function renderInteractiveElements() {", old_js_start)
    content = content[:old_js_start] + js_new_logic + "\n\n" + content[old_js_end:]
else:
    # insert before renderInteractiveElements
    target_insert = "function renderInteractiveElements() {"
    content = content.replace(target_insert, js_new_logic + "\n\n" + target_insert)

# Save back to V1 HTML
with open(file_v1, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated V1 HTML with SVG route line segments and sliding drawer panel!")
