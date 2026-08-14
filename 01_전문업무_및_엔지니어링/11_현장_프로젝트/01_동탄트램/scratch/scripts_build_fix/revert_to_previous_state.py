import sys
import os
import glob
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load exact fixed JSON
with open(r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\intersections_segments_fixed.json', 'r', encoding='utf-8') as f:
    intersections = json.load(f)

# 2. Find V1 HTML file
search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Reverting V1 HTML file to immediately previous state:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

# Restore JS block without getSnapPointOnPath
js_dataset = json.dumps(intersections, ensure_ascii=False)

js_rendering_logic_previous = """// --- 교차로 노선 구간 정밀 매칭 & 지시선/슬라이딩 패널 렌더링 ---
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
  const linesGroup = document.getElementById("intersections-lines-group");
  const labelsGroup = document.getElementById("intersections-labels-group");
  const toggleLines = document.getElementById("toggle-intersections-lines");
  const toggleLabels = document.getElementById("toggle-intersections-labels");

  if (linesGroup) linesGroup.innerHTML = "";
  if (labelsGroup) labelsGroup.innerHTML = "";

  if (linesGroup && toggleLines) {
    linesGroup.style.display = toggleLines.checked ? "block" : "none";
  }
  if (labelsGroup && toggleLabels) {
    labelsGroup.style.display = toggleLabels.checked ? "block" : "none";
  }

  intersectionData.forEach((item, idx) => {
    const is1Tool = item.tool === "1공구";
    const lineColor = is1Tool ? "#ea580c" : "#2563eb";
    const badgeBg = is1Tool ? "rgba(255, 247, 237, 0.96)" : "rgba(239, 246, 255, 0.96)";
    const textColor = is1Tool ? "#c2410c" : "#1d4ed8";

    // Perpendicular unit vector calculation for staggered label offset
    let dx = item.x2 - item.x1;
    let dy = item.y2 - item.y1;
    let len = Math.sqrt(dx * dx + dy * dy);
    if (len < 0.1) { dx = 1; dy = 0; len = 1; }
    const px = -dy / len;
    const py = dx / len;

    // Stagger offset distances
    const staggerStep = (idx % 4);
    let offsetDist = 18;
    if (staggerStep === 0) offsetDist = 18;
    else if (staggerStep === 1) offsetDist = -18;
    else if (staggerStep === 2) offsetDist = 28;
    else offsetDist = -28;

    const lx = item.x + px * offsetDist;
    const ly = item.y + py * offsetDist;

    // --- A. TRACK SEGMENT OVERLAY & SINGLE CLEAN INTERSECTION NODE ---
    if (linesGroup) {
      const gLine = document.createElementNS("http://www.w3.org/2000/svg", "g");
      gLine.setAttribute("class", "intersection-line-group");
      gLine.setAttribute("data-id", `${item.tool}_${item.no}`);

      // Track Segment Line (x1,y1 ~ x2,y2)
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

      // Single Clean Node Circle Dot at Center Point (x, y)
      const cNode = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      cNode.setAttribute("cx", item.x);
      cNode.setAttribute("cy", item.y);
      cNode.setAttribute("r", "2.2");
      cNode.setAttribute("fill", lineColor);
      cNode.setAttribute("stroke", "#ffffff");
      cNode.setAttribute("stroke-width", "0.8");
      cNode.style.cursor = "pointer";

      gLine.appendChild(trackLine);
      gLine.appendChild(cNode);

      gLine.addEventListener("mouseenter", (e) => {
        showTooltip(e, `<b>[${item.tool} #${item.no}] ${item.name}</b><br>· STA: ${item.startSta}m ~ ${item.endSta}m (총연장 ${item.length}m)<br>· 공법: ${item.method} (${item.stage}단계)<br>· <b>단계별 평균작업연장: ${item.avgLen}m</b>`);
      });
      gLine.addEventListener("mouseleave", hideTooltip);
      gLine.addEventListener("click", (e) => {
        e.stopPropagation();
        selectIntersection(item);
      });

      linesGroup.appendChild(gLine);
    }

    // --- B. LEADER LINE & FLOATING TEXT LABEL BADGE ---
    if (labelsGroup) {
      const gLabel = document.createElementNS("http://www.w3.org/2000/svg", "g");
      gLabel.setAttribute("class", "intersection-label-group");
      gLabel.setAttribute("data-id", `${item.tool}_${item.no}`);

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

      const labelBadge = document.createElementNS("http://www.w3.org/2000/svg", "g");
      labelBadge.setAttribute("transform", `translate(${lx}, ${ly})`);
      labelBadge.style.cursor = "pointer";

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

      labelBadge.appendChild(rect);
      labelBadge.appendChild(text);

      gLabel.appendChild(leaderLine);
      gLabel.appendChild(labelBadge);

      gLabel.addEventListener("mouseenter", (e) => {
        showTooltip(e, `<b>[${item.tool} #${item.no}] ${item.name}</b><br>· STA: ${item.startSta}m ~ ${item.endSta}m (총연장 ${item.length}m)<br>· 공법: ${item.method} (${item.stage}단계)<br>· <b>단계별 평균작업연장: ${item.avgLen}m</b>`);
      });
      gLabel.addEventListener("mouseleave", hideTooltip);
      gLabel.addEventListener("click", (e) => {
        e.stopPropagation();
        selectIntersection(item);
      });

      labelsGroup.appendChild(gLabel);
    }
  });

  renderDrawerList();
}"""

start_pos = content.find("// --- 교차로 노선 구간")
if start_pos == -1:
    start_pos = content.find("// --- SVG 경로(Path)")

end_pos = content.find("function selectIntersection(item) {", start_pos)

if start_pos != -1 and end_pos != -1:
    content = content[:start_pos] + js_rendering_logic_previous + "\n\n" + content[end_pos:]
    print("Restored previous JS rendering logic successfully!")

with open(file_v1, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully reverted V1 HTML to the immediately previous state!")
