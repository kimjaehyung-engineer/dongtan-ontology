import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update renderConstructionSections function
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

  constructionSections.forEach((sec, idx) => {
    const startPos = getPosFromPair(sec.startStnA, sec.startStnB, sec.startRatio);
    const endPos = getPosFromPair(sec.endStnA, sec.endStnB, sec.endRatio);

    let dx = endPos.x - startPos.x;
    let dy = endPos.y - startPos.y;
    let len = Math.sqrt(dx * dx + dy * dy) || 1;
    let nx = -dy / len;
    let ny = dx / len;

    if (ny < 0) {
      nx = -nx;
      ny = -ny;
    }

    const offsetH = (idx % 2 === 0) ? 26 : 42;

    const startExt = { x: startPos.x + nx * offsetH, y: startPos.y + ny * offsetH };
    const endExt = { x: endPos.x + nx * offsetH, y: endPos.y + ny * offsetH };
    const midExt = { x: (startExt.x + endExt.x) / 2, y: (startExt.y + endExt.y) / 2 };

    const is1 = sec.tool === "1공구";
    const lineColor = "#000000";
    const nodeColor = "#000000";
    const badgeBg = is1 ? "#fff7ed" : "#eff6ff";
    const textColor = is1 ? "#9a3412" : "#1e3a8a";

    const gItem = document.createElementNS("http://www.w3.org/2000/svg", "g");
    gItem.setAttribute("class", "cs-section-group");
    gItem.setAttribute("data-cs-id", sec.no);

    // 1. Start & End Boundary Nodes on track
    const startNode = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    startNode.setAttribute("cx", startPos.x); startNode.setAttribute("cy", startPos.y);
    startNode.setAttribute("r", "1.2"); startNode.setAttribute("fill", nodeColor);

    const endNode = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    endNode.setAttribute("cx", endPos.x); endNode.setAttribute("cy", endPos.y);
    endNode.setAttribute("r", "1.2"); endNode.setAttribute("fill", nodeColor);

    // 2. Vertical Extension Leader Lines (thin black line 0.35px)
    const leaderLineStart = document.createElementNS("http://www.w3.org/2000/svg", "line");
    leaderLineStart.setAttribute("x1", startPos.x); leaderLineStart.setAttribute("y1", startPos.y);
    leaderLineStart.setAttribute("x2", startExt.x); leaderLineStart.setAttribute("y2", startExt.y);
    leaderLineStart.setAttribute("stroke", lineColor); leaderLineStart.setAttribute("stroke-width", "0.35");
    leaderLineStart.setAttribute("stroke-dasharray", "1.5, 1");

    const leaderLineEnd = document.createElementNS("http://www.w3.org/2000/svg", "line");
    leaderLineEnd.setAttribute("x1", endPos.x); leaderLineEnd.setAttribute("y1", endPos.y);
    leaderLineEnd.setAttribute("x2", endExt.x); leaderLineEnd.setAttribute("y2", endExt.y);
    leaderLineEnd.setAttribute("stroke", lineColor); leaderLineEnd.setAttribute("stroke-width", "0.35");
    leaderLineEnd.setAttribute("stroke-dasharray", "1.5, 1");

    // 3. Dimension Bracket Line (thin black line 0.4px)
    const dimLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
    dimLine.setAttribute("x1", startExt.x); dimLine.setAttribute("y1", startExt.y);
    dimLine.setAttribute("x2", endExt.x); dimLine.setAttribute("y2", endExt.y);
    dimLine.setAttribute("stroke", lineColor); dimLine.setAttribute("stroke-width", "0.4");
    dimLine.style.cursor = "pointer";

    // Start/End Ticks
    const tickStart = document.createElementNS("http://www.w3.org/2000/svg", "line");
    tickStart.setAttribute("x1", startExt.x - nx * 2); tickStart.setAttribute("y1", startExt.y - ny * 2);
    tickStart.setAttribute("x2", startExt.x + nx * 2); tickStart.setAttribute("y2", startExt.y + ny * 2);
    tickStart.setAttribute("stroke", lineColor); tickStart.setAttribute("stroke-width", "0.4");

    const tickEnd = document.createElementNS("http://www.w3.org/2000/svg", "line");
    tickEnd.setAttribute("x1", endExt.x - nx * 2); tickEnd.setAttribute("y1", endExt.y - ny * 2);
    tickEnd.setAttribute("x2", endExt.x + nx * 2); tickEnd.setAttribute("y2", endExt.y + ny * 2);
    tickEnd.setAttribute("stroke", lineColor); tickEnd.setAttribute("stroke-width", "0.4");

    // 4. Callout Title Badge at midExt
    const labelG = document.createElementNS("http://www.w3.org/2000/svg", "g");
    labelG.setAttribute("transform", `translate(${midExt.x}, ${midExt.y})`);
    labelG.style.cursor = "pointer";

    const textStr = `[${sec.tool}] ${sec.section} (${sec.length}m)`;
    let strW = 0;
    for (let c = 0; c < textStr.length; c++) {
      strW += textStr.charCodeAt(c) > 127 ? 2.2 : 1.3;
    }
    const rectW = Math.max(28, strW + 5);
    const rectH = 4.6;

    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("x", -rectW / 2); rect.setAttribute("y", -rectH / 2);
    rect.setAttribute("width", rectW); rect.setAttribute("height", rectH);
    rect.setAttribute("rx", "1.5");
    rect.setAttribute("fill", badgeBg); rect.setAttribute("stroke", "#333333");
    rect.setAttribute("stroke-width", "0.4");
    rect.setAttribute("filter", "drop-shadow(0 1px 2px rgba(0,0,0,0.15))");

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", "0"); text.setAttribute("y", "0.1");
    text.setAttribute("text-anchor", "middle"); text.setAttribute("dominant-baseline", "central");
    text.setAttribute("font-family", "Noto Sans KR");
    text.setAttribute("font-size", "2.3px"); text.setAttribute("font-weight", "700");
    text.setAttribute("fill", textColor);
    text.textContent = textStr;

    labelG.appendChild(rect); labelG.appendChild(text);

    gItem.appendChild(startNode);
    gItem.appendChild(endNode);
    gItem.appendChild(leaderLineStart);
    gItem.appendChild(leaderLineEnd);
    gItem.appendChild(dimLine);
    gItem.appendChild(tickStart);
    gItem.appendChild(tickEnd);
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
    print("Replaced renderConstructionSections with thin black CAD line styling")

# 2. Update selectConstructionSection function
old_select = re.search(r'function selectConstructionSection\(sec\)\s*\{(.*?)\n\}', text, re.DOTALL)

new_select = """function selectConstructionSection(sec) {
  const startPos = getPosFromPair(sec.startStnA, sec.startStnB, sec.startRatio);
  const endPos = getPosFromPair(sec.endStnA, sec.endStnB, sec.endRatio);

  let dx = endPos.x - startPos.x;
  let dy = endPos.y - startPos.y;
  let len = Math.sqrt(dx * dx + dy * dy) || 1;
  let nx = -dy / len;
  let ny = dx / len;
  if (ny < 0) { nx = -nx; ny = -ny; }

  const idx = constructionSections.findIndex(s => s.no === sec.no);
  const offsetH = (idx >= 0 && idx % 2 === 0) ? 26 : 42;

  const startExt = { x: startPos.x + nx * offsetH, y: startPos.y + ny * offsetH };
  const endExt = { x: endPos.x + nx * offsetH, y: endPos.y + ny * offsetH };
  const midExt = { x: (startExt.x + endExt.x) / 2, y: (startExt.y + endExt.y) / 2 };

  focusCoordinates(midExt.x, midExt.y);
  openIntersectionDrawer();

  const matchedIntersections = intersectionData.filter(item => 
    item.tool === sec.tool && !(item.endSta < sec.startSta || item.startSta > sec.endSta)
  );

  let pulseGroup = document.getElementById("section-pulse-overlay");
  if (!pulseGroup) {
    pulseGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    pulseGroup.setAttribute("id", "section-pulse-overlay");
    const mapSvg = document.getElementById("map-svg");
    if (mapSvg) mapSvg.appendChild(pulseGroup);
  }
  pulseGroup.innerHTML = "";

  const is1 = sec.tool === "1공구";
  const glowColor = is1 ? "#ea580c" : "#2563eb";

  // 1. Thin Black Highlight Leaders
  const lStart = document.createElementNS("http://www.w3.org/2000/svg", "line");
  lStart.setAttribute("x1", startPos.x); lStart.setAttribute("y1", startPos.y);
  lStart.setAttribute("x2", startExt.x); lStart.setAttribute("y2", startExt.y);
  lStart.setAttribute("stroke", "#000000"); lStart.setAttribute("stroke-width", "0.8");

  const lEnd = document.createElementNS("http://www.w3.org/2000/svg", "line");
  lEnd.setAttribute("x1", endPos.x); lEnd.setAttribute("y1", endPos.y);
  lEnd.setAttribute("x2", endExt.x); lEnd.setAttribute("y2", endExt.y);
  lEnd.setAttribute("stroke", "#000000"); lEnd.setAttribute("stroke-width", "0.8");

  const dimHighlight = document.createElementNS("http://www.w3.org/2000/svg", "line");
  dimHighlight.setAttribute("x1", startExt.x); dimHighlight.setAttribute("y1", startExt.y);
  dimHighlight.setAttribute("x2", endExt.x); dimHighlight.setAttribute("y2", endExt.y);
  dimHighlight.setAttribute("stroke", glowColor); dimHighlight.setAttribute("stroke-width", "1.5");

  pulseGroup.appendChild(lStart);
  pulseGroup.appendChild(lEnd);
  pulseGroup.appendChild(dimHighlight);

  // 2. Highlight track lines for matched intersections
  if (matchedIntersections.length > 0) {
    matchedIntersections.forEach(item => {
      const iStart = getPosFromPair(item.startStnA, item.startStnB, item.startRatio);
      const iEnd = getPosFromPair(item.endStnA, item.endStnB, item.endRatio);

      const trackLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
      trackLine.setAttribute("x1", iStart.x); trackLine.setAttribute("y1", iStart.y);
      trackLine.setAttribute("x2", iEnd.x); trackLine.setAttribute("y2", iEnd.y);
      trackLine.setAttribute("stroke", glowColor);
      trackLine.setAttribute("stroke-width", "4.5");
      trackLine.setAttribute("stroke-linecap", "round");
      trackLine.setAttribute("class", "flashing-route-line");

      pulseGroup.appendChild(trackLine);
    });
  }

  // 3. Update active card in drawer
  const activeCard = document.getElementById("drawer-active-card");
  if (activeCard) {
    let matchesHtml = "";
    if (matchedIntersections.length > 0) {
      matchesHtml = matchedIntersections.map(m => 
        `<div style="display: flex; align-items: center; justify-content: space-between; padding: 0.4rem 0.6rem; margin-top: 0.35rem; background: var(--panel-bg); border: 1px solid var(--border-color); border-radius: 6px; font-size: 0.78rem; cursor: pointer;" onclick="selectIntersection(intersectionData.find(i=>i.tool==='${m.tool}'&&i.no===${m.no}))">
          <span style="font-weight: 700; color: ${is1 ? '#c2410c' : '#1e40af'};">[${m.tool} #${m.no}] ${m.name}</span>
          <span style="font-size: 0.72rem; color: var(--text-muted);">${m.length}m</span>
        </div>`
      ).join("");
    } else {
      matchesHtml = `<div style="font-size: 0.78rem; color: var(--text-muted); padding: 0.4rem 0;">해당 구간 내 교차로 데이터 없음</div>`;
    }

    activeCard.innerHTML = `
      <div style="background: var(--card-bg); border: 2px solid ${is1 ? '#f97316' : '#3b82f6'}; border-radius: 12px; padding: 1.2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem;">
          <span style="font-size: 0.75rem; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 50px; background: ${is1 ? '#ffedd5' : '#dbeafe'}; color: ${is1 ? '#c2410c' : '#1e40af'};">${sec.tool} 시공구간</span>
          <span style="font-size: 0.75rem; color: var(--text-muted);">구간 No. ${sec.no}</span>
        </div>
        <h3 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 0.8rem; color: var(--text-primary);">${sec.section}</h3>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; margin-bottom: 1rem;">
          <div style="background: ${is1 ? 'linear-gradient(135deg, #fff7ed, #ffedd5)' : 'linear-gradient(135deg, #eff6ff, #dbeafe)'}; border-radius: 10px; padding: 0.8rem; text-align: center; border: 1px solid ${is1 ? '#fdba74' : '#93c5fd'};">
            <div style="font-size: 0.7rem; font-weight: 700; color: ${is1 ? '#c2410c' : '#1e40af'}; text-transform: uppercase;">시공구간 총연장</div>
            <div style="font-size: 1.5rem; font-weight: 900; color: ${is1 ? '#ea580c' : '#2563eb'}; margin-top: 0.1rem;">${sec.length} <span style="font-size: 0.85rem;">m</span></div>
          </div>
          <div style="background: ${is1 ? 'linear-gradient(135deg, #fff7ed, #ffedd5)' : 'linear-gradient(135deg, #eff6ff, #dbeafe)'}; border-radius: 10px; padding: 0.8rem; text-align: center; border: 1px solid ${is1 ? '#fdba74' : '#93c5fd'};">
            <div style="font-size: 0.7rem; font-weight: 700; color: ${is1 ? '#c2410c' : '#1e40af'}; text-transform: uppercase;">소요공기 산출</div>
            <div style="font-size: 1.5rem; font-weight: 900; color: ${is1 ? '#ea580c' : '#2563eb'}; margin-top: 0.1rem;">${sec.duration} <span style="font-size: 0.85rem;">개월</span></div>
          </div>
        </div>

        <table style="width: 100%; border-collapse: collapse; font-size: 0.82rem; margin-bottom: 0.8rem;">
          <tr style="border-bottom: 1px solid var(--border-color);"><td style="padding: 0.4rem 0; color: var(--text-muted);">체이닝 (STA)</td><td style="padding: 0.4rem 0; font-weight: 600; text-align: right;">STA ${sec.startSta}m ~ ${sec.endSta}m</td></tr>
          <tr style="border-bottom: 1px solid var(--border-color);"><td style="padding: 0.4rem 0; color: var(--text-muted);">포함 교차로 수</td><td style="padding: 0.4rem 0; font-weight: 600; text-align: right;">${matchedIntersections.length} 개소</td></tr>
        </table>

        <div style="font-size: 0.78rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.3rem;">📌 구간 내 포함 교차로 목록 (${matchedIntersections.length}):</div>
        <div style="max-height: 180px; overflow-y: auto;">
          ${matchesHtml}
        </div>
      </div>
    `;
  }

  const sectionQuickNavEl = document.getElementById("section-quick-nav");
  if (sectionQuickNavEl) {
    sectionQuickNavEl.value = String(sec.no);
  }
}"""

if old_select:
    text = text.replace(old_select.group(0), new_select, 1)
    print("Replaced selectConstructionSection with thin black CAD line selection")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied thin black CAD line styling successfully!")
