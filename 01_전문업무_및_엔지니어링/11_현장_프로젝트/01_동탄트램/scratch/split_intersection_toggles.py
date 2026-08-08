import sys
import os
import glob
import re

sys.stdout.reconfigure(encoding='utf-8')

search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Updating HTML file:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Layer Panel Checkboxes
old_layer_item = """<label class="layer-item">
      <input type="checkbox" id="toggle-intersections" checked> 교차로 정보 (단계별 평균연장)
    </label>"""

new_layer_items = """<label class="layer-item">
      <input type="checkbox" id="toggle-intersections-lines" checked> 교차로 구간선 (노선 오버레이)
    </label>
    <label class="layer-item">
      <input type="checkbox" id="toggle-intersections-labels" checked> 교차로명 라벨 (단계별 평균연장)
    </label>"""

if 'id="toggle-intersections"' in content:
    content = content.replace(old_layer_item, new_layer_items)
    print("Updated layer panel checkboxes.")

# 2. Update SVG Groups inside map-svg
old_svg_group = '<g id="intersections-group"></g>'
new_svg_groups = """<!-- Intersections Layer Groups -->
      <g id="intersections-lines-group"></g>
      <g id="intersections-labels-group"></g>"""

if 'id="intersections-group"' in content:
    content = content.replace(old_svg_group, new_svg_groups)
    print("Updated SVG group elements into lines and labels groups.")

# 3. Update renderIntersections JS function
old_render_start = content.find("function renderIntersections() {")
old_render_end = content.find("function selectIntersection(item) {", old_render_start)

new_render_func = """function renderIntersections() {
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

    // Perpendicular unit vector calculation
    let dx = item.x2 - item.x1;
    let dy = item.y2 - item.y1;
    let len = Math.sqrt(dx * dx + dy * dy);
    if (len < 0.1) { dx = 1; dy = 0; len = 1; }
    const px = -dy / len;
    const py = dx / len;

    // Stagger offset distances
    const staggerStep = (idx % 4);
    let offsetDist = 16;
    if (staggerStep === 0) offsetDist = 16;
    else if (staggerStep === 1) offsetDist = -16;
    else if (staggerStep === 2) offsetDist = 26;
    else offsetDist = -26;

    const lx = item.x + px * offsetDist;
    const ly = item.y + py * offsetDist;

    // --- A. LINE SEGMENT & TERMINAL DOTS GROUP ---
    if (linesGroup) {
      const gLine = document.createElementNS("http://www.w3.org/2000/svg", "g");
      gLine.setAttribute("class", "intersection-line-group");
      gLine.setAttribute("data-id", `${item.tool}_${item.no}`);

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

      const cStart = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      cStart.setAttribute("cx", item.x1); cStart.setAttribute("cy", item.y1); cStart.setAttribute("r", "1.5");
      cStart.setAttribute("fill", lineColor); cStart.setAttribute("stroke", "#ffffff"); cStart.setAttribute("stroke-width", "0.5");

      const cEnd = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      cEnd.setAttribute("cx", item.x2); cEnd.setAttribute("cy", item.y2); cEnd.setAttribute("r", "1.5");
      cEnd.setAttribute("fill", lineColor); cEnd.setAttribute("stroke", "#ffffff"); cEnd.setAttribute("stroke-width", "0.5");

      gLine.appendChild(trackLine);
      gLine.appendChild(cStart);
      gLine.appendChild(cEnd);

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

    // --- B. LEADER LINE & FLOATING TEXT LABEL GROUP ---
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
}
"""

if old_render_start != -1 and old_render_end != -1:
    content = content[:old_render_start] + new_render_func + "\n\n" + content[old_render_end:]
    print("Replaced renderIntersections JS function.")

# 4. Update Event Listeners for Toggles
old_toggle = 'document.getElementById("toggle-intersections").addEventListener("change", (e) => {'
if old_toggle in content:
    pos_t = content.find(old_toggle)
    end_t = content.find('});', pos_t) + 3
    new_toggles = """document.getElementById("toggle-intersections-lines").addEventListener("change", (e) => {
  const g = document.getElementById("intersections-lines-group");
  if (g) g.style.display = e.target.checked ? "block" : "none";
});
document.getElementById("toggle-intersections-labels").addEventListener("change", (e) => {
  const g = document.getElementById("intersections-labels-group");
  if (g) g.style.display = e.target.checked ? "block" : "none";
});"""
    content = content[:pos_t] + new_toggles + content[end_t:]
    print("Replaced toggle event listeners.")

# Save back to HTML
with open(file_v1, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully applied split intersection toggles to V1 HTML!")
