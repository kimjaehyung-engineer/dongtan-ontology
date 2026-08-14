import sys
import os
import json
import glob
import re

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load mapped intersections JSON
with open(r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\intersections_mapped.json', 'r', encoding='utf-8') as f:
    intersections = json.load(f)

# 2. Find V1 HTML file
search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Found V1 HTML:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

# 3. Add checkbox to layer panel if not present
checkbox_code = '<label class="layer-item">\n      <input type="checkbox" id="toggle-intersections" checked> 교차로 정보 (단계별 평균연장)\n    </label>'
if 'toggle-intersections' not in content:
    target = '<label class="layer-item">\n      <input type="checkbox" id="toggle-turnouts" checked> 분기기 및 규격\n    </label>'
    content = content.replace(target, target + '\n    ' + checkbox_code)

# 4. Add SVG group if not present
if 'id="intersections-group"' not in content:
    target_svg = '<g id="turnouts-group"></g>'
    content = content.replace(target_svg, target_svg + '\n      <!-- Intersections Group -->\n      <g id="intersections-group"></g>')

# 5. Build JS code for intersectionData & rendering
js_intersections_json = json.dumps(intersections, ensure_ascii=False)

js_code_block = """
// --- 교차로 정보 (단계별 평균작업연장) 데이터 & 렌더링 ---
const intersectionData = """ + js_intersections_json + """;

const intersectionsGroup = document.getElementById("intersections-group");
const toggleIntersections = document.getElementById("toggle-intersections");

function renderIntersections() {
  if (!intersectionsGroup) return;
  intersectionsGroup.innerHTML = "";
  
  if (toggleIntersections && !toggleIntersections.checked) return;

  intersectionData.forEach(item => {
    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("class", "intersection-marker");
    g.setAttribute("data-id", `${item.tool}_${item.no}`);
    g.setAttribute("transform", `translate(${item.x}, ${item.y})`);
    g.style.cursor = "pointer";

    // Text Label: Name & Avg Len
    const textStr = `${item.name.replace(/\\s+/g, '')} (단계별 ${item.avgLen}m)`;
    const textLen = textStr.length;
    const rectW = Math.max(30, textLen * 2.1 + 4);
    const rectH = 5.2;

    // Outer Badge Rect
    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("x", -rectW / 2);
    rect.setAttribute("y", -rectH / 2 - 6);
    rect.setAttribute("width", rectW);
    rect.setAttribute("height", rectH);
    rect.setAttribute("rx", "1.2");
    rect.setAttribute("ry", "1.2");
    rect.setAttribute("fill", "rgba(255, 247, 237, 0.95)");
    rect.setAttribute("stroke", item.tool === "1공구" ? "#ea580c" : "#2563eb");
    rect.setAttribute("stroke-width", "0.4");
    rect.setAttribute("filter", "drop-shadow(0 0.5px 1px rgba(0,0,0,0.15))");

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", "0");
    text.setAttribute("y", -6 + 1.6);
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("dominant-baseline", "middle");
    text.setAttribute("font-family", "Noto Sans KR");
    text.setAttribute("font-size", "3.6px");
    text.setAttribute("font-weight", "700");
    text.setAttribute("fill", item.tool === "1공구" ? "#c2410c" : "#1d4ed8");
    text.textContent = textStr;

    g.appendChild(rect);
    g.appendChild(text);

    // Hover Tooltip
    g.addEventListener("mouseenter", (e) => {
      showTooltip(e, `[${item.tool} #${item.no}] ${item.name}<br>· STA: ${item.startSta}m ~ ${item.endSta}m (총연장 ${item.length}m)<br>· 공법: ${item.method} (${item.stage}단계)<br>· <b>단계별 평균작업연장: ${item.avgLen}m</b>`);
    });
    g.addEventListener("mouseleave", hideTooltip);

    // Click Event to Show Details
    g.addEventListener("click", (e) => {
      e.stopPropagation();
      selectIntersection(item);
    });

    intersectionsGroup.appendChild(g);
  });
}

function selectIntersection(item) {
  panTo(item.x, item.y);
  
  const stnNameEl = document.getElementById("stn-name");
  const stnTypeEl = document.getElementById("stn-type");
  
  if (stnNameEl) stnNameEl.textContent = item.name;
  if (stnTypeEl) stnTypeEl.textContent = `${item.tool} 교차로 (${item.code})`;

  const badge = document.getElementById("panel-badge");
  if (badge) {
    badge.textContent = item.tool;
    badge.className = item.tool === "1공구" ? "badge red" : "badge blue";
  }

  // Open station tab
  if (typeof switchPanelTab === 'function') {
    switchPanelTab('stn');
  }

  const issuesList = document.getElementById("info-issues");
  if (issuesList) {
    issuesList.innerHTML = `
      <div style="background: var(--card-bg); border: 1.5px solid ${item.tool === '1공구' ? '#f97316' : '#3b82f6'}; border-radius: 8px; padding: 0.8rem; margin-top: 0.5rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.4rem;">
          <span style="font-weight: 700; color: ${item.tool === '1공구' ? '#ea580c' : '#2563eb'}; font-size: 0.88rem;">🚧 교차로 시공 공기산출 상세</span>
          <span style="background: ${item.tool === '1공구' ? '#ffedd5' : '#dbeafe'}; color: ${item.tool === '1공구' ? '#c2410c' : '#1e40af'}; padding: 0.15rem 0.5rem; border-radius: 50px; font-size: 0.72rem; font-weight: 700;">${item.tool} #${item.no}</span>
        </div>
        <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem;">
          <tr style="border-bottom: 1px solid var(--border-color);"><td style="padding: 0.3rem 0; color: var(--text-muted);">구간 코드</td><td style="padding: 0.3rem 0; font-weight: 600; text-align: right;">${item.code}</td></tr>
          <tr style="border-bottom: 1px solid var(--border-color);"><td style="padding: 0.3rem 0; color: var(--text-muted);">STA 위치</td><td style="padding: 0.3rem 0; font-weight: 600; text-align: right;">${item.startSta}m ~ ${item.endSta}m</td></tr>
          <tr style="border-bottom: 1px solid var(--border-color);"><td style="padding: 0.3rem 0; color: var(--text-muted);">구간 총 연장</td><td style="padding: 0.3rem 0; font-weight: 600; text-align: right;">${item.length}m</td></tr>
          <tr style="border-bottom: 1px solid var(--border-color);"><td style="padding: 0.3rem 0; color: var(--text-muted);">공법 / 단계</td><td style="padding: 0.3rem 0; font-weight: 600; text-align: right;">${item.method} (${item.stage}단계)</td></tr>
          <tr style="background: ${item.tool === '1공구' ? 'rgba(249, 115, 22, 0.15)' : 'rgba(59, 130, 246, 0.15)'};"><td style="padding: 0.4rem; color: ${item.tool === '1공구' ? '#c2410c' : '#1e40af'}; font-weight: 700;">단계별 평균작업연장</td><td style="padding: 0.4rem; color: ${item.tool === '1공구' ? '#c2410c' : '#1e40af'}; font-weight: 800; font-size: 0.92rem; text-align: right;">${item.avgLen} m</td></tr>
        </table>
      </div>
    `;
  }
}
"""

if 'const intersectionData =' not in content:
    target_js_insert = "function renderInteractiveElements() {"
    content = content.replace(target_js_insert, js_code_block + "\n\n" + target_js_insert)

# 6. Add renderIntersections() call inside init DOMContentLoaded
if 'renderIntersections();' not in content:
    content = content.replace("renderInteractiveElements();", "renderIntersections();\n  renderInteractiveElements();")

# 7. Add toggle event listener
if 'toggle-intersections' in content and 'document.getElementById("toggle-intersections").addEventListener' not in content:
    toggle_target = 'document.getElementById("toggle-turnouts").addEventListener("change", (e) => {\n  document.getElementById("turnouts-group").style.display = e.target.checked ? "block" : "none";\n});'
    toggle_replacement = toggle_target + '\ndocument.getElementById("toggle-intersections").addEventListener("change", (e) => {\n  if (document.getElementById("intersections-group")) {\n    document.getElementById("intersections-group").style.display = e.target.checked ? "block" : "none";\n  }\n});'
    content = content.replace(toggle_target, toggle_replacement)

# Write back to file
with open(file_v1, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully applied intersection data and rendering to V1 HTML!")
