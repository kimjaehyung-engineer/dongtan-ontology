import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add selectConstructionSection function before renderConstructionSections
select_sec_fn = """function selectConstructionSection(sec) {
  const startPos = getPosFromPair(sec.startStnA, sec.startStnB, sec.startRatio);
  const endPos = getPosFromPair(sec.endStnA, sec.endStnB, sec.endRatio);
  const midPos = getPosFromPair(sec.midStnA, sec.midStnB, sec.midRatio);

  focusCoordinates(midPos.x, midPos.y);

  let pulseGroup = document.getElementById("section-pulse-overlay");
  if (!pulseGroup) {
    pulseGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    pulseGroup.setAttribute("id", "section-pulse-overlay");
    const mapSvg = document.getElementById("map-svg");
    if (mapSvg) mapSvg.appendChild(pulseGroup);
  }
  pulseGroup.innerHTML = "";

  const is1 = sec.tool === "1공구";
  const glowColor = is1 ? "#ff4500" : "#0066ff";

  // 1. Neon Flashing Highlight Route Line Segment
  const flashLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
  flashLine.setAttribute("x1", startPos.x); flashLine.setAttribute("y1", startPos.y);
  flashLine.setAttribute("x2", endPos.x); flashLine.setAttribute("y2", endPos.y);
  flashLine.setAttribute("stroke", glowColor);
  flashLine.setAttribute("stroke-width", "6.5");
  flashLine.setAttribute("stroke-linecap", "round");
  flashLine.setAttribute("class", "flashing-route-line");

  // 2. Dual Pulse Rings at Center
  const ring1 = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  ring1.setAttribute("cx", midPos.x); ring1.setAttribute("cy", midPos.y);
  ring1.setAttribute("fill", "none"); ring1.setAttribute("stroke", glowColor);
  ring1.setAttribute("class", "pulse-ring-1");

  const ring2 = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  ring2.setAttribute("cx", midPos.x); ring2.setAttribute("cy", midPos.y);
  ring2.setAttribute("fill", "none"); ring2.setAttribute("stroke", glowColor);
  ring2.setAttribute("class", "pulse-ring-2");

  // 3. Center Glowing Beacon Dot
  const beacon = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  beacon.setAttribute("cx", midPos.x); beacon.setAttribute("cy", midPos.y);
  beacon.setAttribute("r", "3"); beacon.setAttribute("fill", "#ffffff");
  beacon.setAttribute("stroke", glowColor); beacon.setAttribute("stroke-width", "1.5");
  beacon.setAttribute("class", "flashing-route-line");

  pulseGroup.appendChild(flashLine);
  pulseGroup.appendChild(ring1);
  pulseGroup.appendChild(ring2);
  pulseGroup.appendChild(beacon);

  const sectionQuickNavEl = document.getElementById("section-quick-nav");
  if (sectionQuickNavEl) {
    sectionQuickNavEl.value = String(sec.no);
  }
}

"""

if "function selectConstructionSection(" not in text:
    text = text.replace("function renderConstructionSections() {", select_sec_fn + "function renderConstructionSections() {", 1)

# 2. Update renderConstructionSections line styling & click handler
old_line_style = """    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", startPos.x);
    line.setAttribute("y1", startPos.y);
    line.setAttribute("x2", endPos.x);
    line.setAttribute("y2", endPos.y);
    line.setAttribute("stroke", lineColor);
    line.setAttribute("stroke-width", "8");
    line.setAttribute("stroke-linecap", "round");
    line.setAttribute("opacity", "0.7");
    line.style.cursor = "pointer";"""

new_line_style = """    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", startPos.x);
    line.setAttribute("y1", startPos.y);
    line.setAttribute("x2", endPos.x);
    line.setAttribute("y2", endPos.y);
    line.setAttribute("stroke", is1 ? "#ea580c" : "#2563eb");
    line.setAttribute("stroke-width", "1.8");
    line.setAttribute("stroke-dasharray", "4, 3");
    line.setAttribute("opacity", "0.75");
    line.style.cursor = "pointer";"""

text = text.replace(old_line_style, new_line_style, 1)

# Update click handler inside renderConstructionSections
old_click_handler = """    gItem.addEventListener("click", (e) => {
      e.stopPropagation();
      focusCoordinates(midPos.x, midPos.y);
    });"""

new_click_handler = """    gItem.addEventListener("click", (e) => {
      e.stopPropagation();
      selectConstructionSection(sec);
    });"""

text = text.replace(old_click_handler, new_click_handler, 1)

# 3. Update section-quick-nav listener to call selectConstructionSection
old_sqn_listener = """const sectionQuickNavEl = document.getElementById("section-quick-nav");
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

new_sqn_listener = """const sectionQuickNavEl = document.getElementById("section-quick-nav");
if (sectionQuickNavEl) {
  sectionQuickNavEl.addEventListener("change", (e) => {
    const val = e.target.value;
    if (val) {
      const sec = constructionSections.find(s => s.no === parseInt(val, 10));
      if (sec) {
        selectConstructionSection(sec);
      }
    }
  });
}"""

text = text.replace(old_sqn_listener, new_sqn_listener, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied section highlight logic successfully!")
