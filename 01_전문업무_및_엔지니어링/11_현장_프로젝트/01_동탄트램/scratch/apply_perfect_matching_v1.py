import sys
import os
import glob
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load intersections with segment coords
with open(r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\intersections_segments.json', 'r', encoding='utf-8') as f:
    intersections = json.load(f)

# 2. Find V1 HTML file
search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Applying perfect matching to V1 HTML:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

js_dataset = json.dumps(intersections, ensure_ascii=False)

js_rendering_logic = """
// --- 교차로 노선 구간 정밀 매칭 & 지시선/슬라이딩 패널 렌더링 ---
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

  intersectionData.forEach((item, idx) => {
    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("class", "intersection-segment-group");
    g.setAttribute("data-id", `${item.tool}_${item.no}`);

    const is1Tool = item.tool === "1공구";
    const lineColor = is1Tool ? "#ea580c" : "#2563eb";
    const badgeBg = is1Tool ? "rgba(255, 247, 237, 0.96)" : "rgba(239, 246, 255, 0.96)";
    const textColor = is1Tool ? "#c2410c" : "#1d4ed8";

    // Calculate perpendicular offset for callout staggering
    let dx = item.x2 - item.x1;
    let dy = item.y2 - item.y1;
    let len = Math.sqrt(dx * dx + dy * dy);
    if (len < 0.1) { dx = 1; dy = 0; len = 1; }
    
    // Perpendicular unit vector
    const px = -dy / len;
    const py = dx / len;

    // Stagger distance: alternate +18px / -18px / +26px / -26px
    const staggerStep = (idx % 4);
    let offsetDist = 16;
    if (staggerStep === 0) offsetDist = 16;
    else if (staggerStep === 1) offsetDist = -16;
    else if (staggerStep === 2) offsetDist = 26;
    else offsetDist = -26;

    const lx = item.x + px * offsetDist;
    const ly = item.y + py * offsetDist;

    // 1. Route Track Segment Line (x1,y1 ~ x2,y2) - Matched directly on route
    const trackLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
    trackLine.setAttribute("x1", item.x1);
    trackLine.setAttribute("y1", item.y1);
    trackLine.setAttribute("x2", item.x2);
    trackLine.setAttribute("y2", item.y2);
    trackLine.setAttribute("stroke", lineColor);
    trackLine.setAttribute("stroke-width", "4.5");
    trackLine.setAttribute("stroke-linecap", "round");
    trackLine.setAttribute("opacity", "0.9");
    trackLine.setAttribute("class", "intersection-route-line");

    // 2. Terminal Dots at Start & End of Segment
    const cStart = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    cStart.setAttribute("cx", item.x1); cStart.setAttribute("cy", item.y1); cStart.setAttribute("r", "1.5");
    cStart.setAttribute("fill", lineColor); cStart.setAttribute("stroke", "#ffffff"); cStart.setAttribute("stroke-width", "0.5");

    const cEnd = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    cEnd.setAttribute("cx", item.x2); cEnd.setAttribute("cy", item.y2); cEnd.setAttribute("r", "1.5");
    cEnd.setAttribute("fill", lineColor); cEnd.setAttribute("stroke", "#ffffff"); cEnd.setAttribute("stroke-width", "0.5");

    // 3. Leader / Callout Line from Track Point (x,y) to Staggered Badge (lx, ly)
    const leaderLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
    leaderLine.setAttribute("x1", item.x);
    leaderLine.setAttribute("y1", item.y);
    leaderLine.setAttribute("x2", lx);
    leaderLine.setAttribute("y2", ly);
    leaderLine.setAttribute("stroke", lineColor);
    leaderLine.setAttribute("stroke-width", "0.5");
    leaderLine.setAttribute("stroke-dasharray", "1, 1");
    leaderLine.setAttribute("opacity", "0.75");
    leaderLine.setAttribute("style", "pointer-events: none;");

    // 4. Staggered Floating Badge Group at (lx, ly)
    const labelGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    labelGroup.setAttribute("transform", `translate(${lx}, ${ly})`);
    labelGroup.style.cursor = "pointer";

    const textStr = `${item.name.replace(/\\s+/g, '')} [${item.avgLen}m]`;
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
    text.textContent = textStr;

    labelGroup.appendChild(rect);
    labelGroup.appendChild(text);

    g.appendChild(trackLine);
    g.appendChild(cStart);
    g.appendChild(cEnd);
    g.appendChild(leaderLine);
    g.appendChild(labelGroup);

    // Hover Tooltip Events
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

# Replace JS logic in HTML
old_js_start = content.find("// --- 교차로 정보")
if old_js_start != -1:
    old_js_end = content.find("function renderInteractiveElements() {", old_js_start)
    content = content[:old_js_start] + js_rendering_logic + "\n\n" + content[old_js_end:]

# Write back
with open(file_v1, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully applied perfect matching & staggered callout lines to V1 HTML!")
