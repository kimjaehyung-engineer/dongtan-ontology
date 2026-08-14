import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace selectConstructionSection function
old_select = re.search(r'function selectConstructionSection\(sec\)\s*\{(.*?)\n\}', text, re.DOTALL)

new_select = """function selectConstructionSection(sec) {
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

  // 1. Dual Pulse Rings at Center
  const ring1 = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  ring1.setAttribute("cx", midPos.x); ring1.setAttribute("cy", midPos.y);
  ring1.setAttribute("fill", "none"); ring1.setAttribute("stroke", glowColor);
  ring1.setAttribute("class", "pulse-ring-1");

  const ring2 = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  ring2.setAttribute("cx", midPos.x); ring2.setAttribute("cy", midPos.y);
  ring2.setAttribute("fill", "none"); ring2.setAttribute("stroke", glowColor);
  ring2.setAttribute("class", "pulse-ring-2");

  // 2. Center Glowing Beacon Dot
  const beacon = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  beacon.setAttribute("cx", midPos.x); beacon.setAttribute("cy", midPos.y);
  beacon.setAttribute("r", "3"); beacon.setAttribute("fill", "#ffffff");
  beacon.setAttribute("stroke", glowColor); beacon.setAttribute("stroke-width", "1.5");
  beacon.setAttribute("class", "flashing-route-line");

  pulseGroup.appendChild(ring1);
  pulseGroup.appendChild(ring2);
  pulseGroup.appendChild(beacon);

  const sectionQuickNavEl = document.getElementById("section-quick-nav");
  if (sectionQuickNavEl) {
    sectionQuickNavEl.value = String(sec.no);
  }
}"""

if old_select:
    text = text.replace(old_select.group(0), new_select, 1)
    print("Replaced selectConstructionSection")

# 2. Replace renderConstructionSections function
old_render = re.search(r'function renderConstructionSections\(\)\s*\{(.*?)\n\}', text, re.DOTALL)

new_render = """function renderConstructionSections() {
  const group = document.getElementById("construction-sections-group");
  if (!group) return;
  group.innerHTML = "";

  const sectionQuickNav = document.getElementById("section-quick-nav");
  if (sectionQuickNav) {
    sectionQuickNav.innerHTML = '<option value="">시공구간 바로가기...</option>';
    constructionSections.forEach(sec => {
      const opt = document.createElement("option");
      opt.value = sec.no;
      opt.textContent = `[${sec.tool}] ${sec.section} (${sec.length}m)`;
      sectionQuickNav.appendChild(opt);
    });
  }

  constructionSections.forEach(sec => {
    const midPos = getPosFromPair(sec.midStnA, sec.midStnB, sec.midRatio);

    const is1 = sec.tool === "1공구";
    const nodeColor = is1 ? "#f97316" : "#3b82f6";
    const badgeBg = is1 ? "#fff7ed" : "#eff6ff";
    const textColor = is1 ? "#9a3412" : "#1e3a8a";

    const gItem = document.createElementNS("http://www.w3.org/2000/svg", "g");
    gItem.setAttribute("class", "cs-section-group");
    gItem.setAttribute("data-cs-id", sec.no);

    const labelG = document.createElementNS("http://www.w3.org/2000/svg", "g");
    labelG.setAttribute("transform", `translate(${midPos.x}, ${midPos.y})`);
    labelG.style.cursor = "pointer";

    const textStr = `${sec.section} [${sec.length}m]`;
    let strW = 0;
    for (let c = 0; c < textStr.length; c++) {
      strW += textStr.charCodeAt(c) > 127 ? 2.2 : 1.3;
    }
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

    gItem.appendChild(labelG);

    const tooltipText = `<b>[${sec.tool}] ${sec.section}</b><br>· STA: ${sec.startSta}m ~ ${sec.endSta}m<br>· 구간연장: ${sec.length}m<br>· 소요공기: ${sec.duration}개월<br>· 세부구간: ${sec.segCount}개`;
    gItem.addEventListener("mouseenter", (e) => showTooltip(e, tooltipText));
    gItem.addEventListener("mouseleave", hideTooltip);
    gItem.addEventListener("click", (e) => {
      e.stopPropagation();
      selectConstructionSection(sec);
    });

    group.appendChild(gItem);
  });
}"""

if old_render:
    text = text.replace(old_render.group(0), new_render, 1)
    print("Replaced renderConstructionSections")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Removed all straight/dashed lines successfully!")
