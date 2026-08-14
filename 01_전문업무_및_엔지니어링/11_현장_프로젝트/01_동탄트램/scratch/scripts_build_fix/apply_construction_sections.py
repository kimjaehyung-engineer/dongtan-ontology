import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

html_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'
json_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\construction_sections_js.json'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

with open(json_path, 'r', encoding='utf-8') as f:
    cs_data = json.load(f)

cs_json_str = json.dumps(cs_data, ensure_ascii=False)

# ============================================
# 1. Add SVG layer group (before nodes-group)
# ============================================
svg_anchor = '      <!-- Intersections Group -->'
svg_insert = """      <!-- Construction Sections Group -->
      <g id="construction-sections-group"></g>
      <!-- Intersections Group -->"""

if 'id="construction-sections-group"' not in html:
    html = html.replace(svg_anchor, svg_insert, 1)
    print("✓ Added SVG layer group")

# ============================================
# 2. Add layer toggle checkbox (after intersections labels toggle)
# ============================================
layer_anchor = """    <label class="layer-item">
      <input type="checkbox" id="toggle-intersections-labels" checked> 교차로명 라벨 (구간연장)
    </label>
  </div>"""

layer_insert = """    <label class="layer-item">
      <input type="checkbox" id="toggle-intersections-labels" checked> 교차로명 라벨 (구간연장)
    </label>
    <label class="layer-item">
      <input type="checkbox" id="toggle-construction-sections" checked> 시공구간 분할 (본선)
    </label>
  </div>"""

if 'toggle-construction-sections' not in html:
    html = html.replace(layer_anchor, layer_insert, 1)
    print("✓ Added layer toggle checkbox")

# ============================================
# 3. Add header quick nav dropdown (after intersection-quick-nav)
# ============================================
hdr_anchor = """  <select class="quick-nav-select" id="intersection-quick-nav">
    <option value="">교차로 바로가기...</option>
  </select>"""

hdr_insert = """  <select class="quick-nav-select" id="intersection-quick-nav">
    <option value="">교차로 바로가기...</option>
  </select>
  <select class="quick-nav-select" id="section-quick-nav">
    <option value="">시공구간 바로가기...</option>
  </select>"""

if 'id="section-quick-nav"' not in html:
    html = html.replace(hdr_anchor, hdr_insert, 1)
    print("✓ Added header quick nav dropdown")

# ============================================
# 4. Add constructionSections data array + renderConstructionSections function
#    (insert before renderIntersections function)
# ============================================

render_anchor = "function renderIntersections() {"

js_block = f"""const constructionSections = {cs_json_str};

function renderConstructionSections() {{
  const group = document.getElementById("construction-sections-group");
  if (!group) return;
  group.innerHTML = "";

  const sectionQuickNav = document.getElementById("section-quick-nav");
  if (sectionQuickNav) {{
    sectionQuickNav.innerHTML = '<option value="">시공구간 바로가기...</option>';
    constructionSections.forEach(sec => {{
      const opt = document.createElement("option");
      opt.value = sec.no;
      opt.textContent = `[${{sec.tool}}] ${{sec.section}} (${{sec.length}}m)`;
      sectionQuickNav.appendChild(opt);
    }});
  }}

  constructionSections.forEach(sec => {{
    const startPos = getPosFromPair(sec.startStnA, sec.startStnB, sec.startRatio);
    const endPos = getPosFromPair(sec.endStnA, sec.endStnB, sec.endRatio);
    const midPos = getPosFromPair(sec.midStnA, sec.midStnB, sec.midRatio);

    const is1 = sec.tool === "1공구";
    const lineColor = is1 ? "rgba(249, 115, 22, 0.55)" : "rgba(37, 99, 235, 0.55)";
    const nodeColor = is1 ? "#f97316" : "#3b82f6";
    const badgeBg = is1 ? "#fff7ed" : "#eff6ff";
    const textColor = is1 ? "#9a3412" : "#1e3a8a";

    const gItem = document.createElementNS("http://www.w3.org/2000/svg", "g");
    gItem.setAttribute("class", "cs-section-group");
    gItem.setAttribute("data-cs-id", sec.no);

    // Section overlay line
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", startPos.x);
    line.setAttribute("y1", startPos.y);
    line.setAttribute("x2", endPos.x);
    line.setAttribute("y2", endPos.y);
    line.setAttribute("stroke", lineColor);
    line.setAttribute("stroke-width", "8");
    line.setAttribute("stroke-linecap", "round");
    line.setAttribute("opacity", "0.7");
    line.style.cursor = "pointer";

    // Start node
    const startNode = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    startNode.setAttribute("cx", startPos.x);
    startNode.setAttribute("cy", startPos.y);
    startNode.setAttribute("r", "2");
    startNode.setAttribute("fill", nodeColor);
    startNode.setAttribute("stroke", "#fff");
    startNode.setAttribute("stroke-width", "0.6");

    // End node
    const endNode = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    endNode.setAttribute("cx", endPos.x);
    endNode.setAttribute("cy", endPos.y);
    endNode.setAttribute("r", "2");
    endNode.setAttribute("fill", nodeColor);
    endNode.setAttribute("stroke", "#fff");
    endNode.setAttribute("stroke-width", "0.6");

    // Label badge at midpoint
    const labelG = document.createElementNS("http://www.w3.org/2000/svg", "g");
    const dx = endPos.x - startPos.x;
    const dy = endPos.y - startPos.y;
    const len = Math.sqrt(dx * dx + dy * dy) || 1;
    const px = -dy / len;
    const py = dx / len;
    const offsetDist = is1 ? 18 : -18;
    const lx = midPos.x + px * offsetDist;
    const ly = midPos.y + py * offsetDist;

    labelG.setAttribute("transform", `translate(${{lx}}, ${{ly}})`);
    labelG.style.cursor = "pointer";

    const textStr = `${{sec.section}} [${{sec.length}}m]`;
    let strW = 0;
    for (let c = 0; c < textStr.length; c++) {{
      strW += textStr.charCodeAt(c) > 127 ? 2.2 : 1.3;
    }}
    const rectW = Math.max(24, strW + 4);
    const rectH = 4.2;

    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("x", -rectW / 2);
    rect.setAttribute("y", -rectH / 2);
    rect.setAttribute("width", rectW);
    rect.setAttribute("height", rectH);
    rect.setAttribute("rx", "1");
    rect.setAttribute("fill", badgeBg);
    rect.setAttribute("stroke", nodeColor);
    rect.setAttribute("stroke-width", "0.4");
    rect.setAttribute("filter", "drop-shadow(0 0.5px 1px rgba(0,0,0,0.15))");

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", "0");
    text.setAttribute("y", "0.1");
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("dominant-baseline", "central");
    text.setAttribute("font-family", "Noto Sans KR");
    text.setAttribute("font-size", "2.1px");
    text.setAttribute("font-weight", "700");
    text.setAttribute("fill", textColor);
    text.textContent = textStr;

    labelG.appendChild(rect);
    labelG.appendChild(text);

    gItem.appendChild(line);
    gItem.appendChild(startNode);
    gItem.appendChild(endNode);
    gItem.appendChild(labelG);

    // Tooltip
    const tooltipText = `<b>[${{sec.tool}}] ${{sec.section}}</b><br>· STA: ${{sec.startSta}}m ~ ${{sec.endSta}}m<br>· 구간연장: ${{sec.length}}m<br>· 소요공기: ${{sec.duration}}개월<br>· 세부구간: ${{sec.segCount}}개`;
    gItem.addEventListener("mouseenter", (e) => showTooltip(e, tooltipText));
    gItem.addEventListener("mouseleave", hideTooltip);
    gItem.addEventListener("click", (e) => {{
      e.stopPropagation();
      focusCoordinates(midPos.x, midPos.y);
    }});

    group.appendChild(gItem);
  }});
}}

""" + render_anchor

if "const constructionSections = " not in html:
    html = html.replace(render_anchor, js_block, 1)
    print("✓ Added constructionSections data + renderConstructionSections function")

# ============================================
# 5. Call renderConstructionSections() after renderIntersections() call
# ============================================
init_anchor = "renderIntersections();"
init_insert = """renderIntersections();
renderConstructionSections();"""

if "renderConstructionSections();" not in html:
    html = html.replace(init_anchor, init_insert, 1)
    print("✓ Added renderConstructionSections() init call")

# ============================================
# 6. Add layer toggle event listener (after intersections-labels toggle listener)
# ============================================
toggle_anchor = """document.getElementById("toggle-intersections-labels").addEventListener("change", (e) => {
  const g = document.getElementById("intersections-labels-group");
  if (g) g.style.display = e.target.checked ? "block" : "none";
});"""

toggle_insert = toggle_anchor + """
document.getElementById("toggle-construction-sections").addEventListener("change", (e) => {
  const g = document.getElementById("construction-sections-group");
  if (g) g.style.display = e.target.checked ? "block" : "none";
});"""

if 'toggle-construction-sections"' not in html or 'addEventListener("change"' not in html.split('toggle-construction-sections')[1][:300]:
    html = html.replace(toggle_anchor, toggle_insert, 1)
    print("✓ Added layer toggle event listener")

# ============================================
# 7. Add section quick nav event listener (after intersection quick nav listener)
# ============================================
iqn_anchor = """const intersectionQuickNavEl = document.getElementById("intersection-quick-nav");
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

sqn_insert = iqn_anchor + """

const sectionQuickNavEl = document.getElementById("section-quick-nav");
if (sectionQuickNavEl) {
  sectionQuickNavEl.addEventListener("change", (e) => {
    const val = e.target.value;
    if (val) {
      const sec = constructionSections.find(s => s.no === parseInt(val, 10));
      if (sec) {
        const midPos = getPosFromPair(sec.midStnA, sec.midStnB, sec.midRatio);
        focusCoordinates(midPos.x, midPos.y);
      }
    }
  });
}"""

if 'sectionQuickNavEl' not in html:
    html = html.replace(iqn_anchor, sqn_insert, 1)
    print("✓ Added section quick nav event listener")

# ============================================
# Save
# ============================================
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ All changes applied! File size: {len(html)} bytes")
