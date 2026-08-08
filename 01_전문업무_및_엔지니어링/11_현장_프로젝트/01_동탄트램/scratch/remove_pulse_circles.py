import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace selectConstructionSection function with clean version (no pulse rings)
old_select = re.search(r'function selectConstructionSection\(sec\)\s*\{(.*?)\n\}', text, re.DOTALL)

new_select = """function selectConstructionSection(sec) {
  const midPos = getPosFromPair(sec.midStnA, sec.midStnB, sec.midRatio);

  focusCoordinates(midPos.x, midPos.y);
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
  const glowColor = is1 ? "#ff4500" : "#0066ff";

  if (matchedIntersections.length > 0) {
    matchedIntersections.forEach(item => {
      const startPos = getPosFromPair(item.startStnA, item.startStnB, item.startRatio);
      const endPos = getPosFromPair(item.endStnA, item.endStnB, item.endRatio);

      const flashLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
      flashLine.setAttribute("x1", startPos.x); flashLine.setAttribute("y1", startPos.y);
      flashLine.setAttribute("x2", endPos.x); flashLine.setAttribute("y2", endPos.y);
      flashLine.setAttribute("stroke", glowColor);
      flashLine.setAttribute("stroke-width", "5.5");
      flashLine.setAttribute("stroke-linecap", "round");
      flashLine.setAttribute("class", "flashing-route-line");

      pulseGroup.appendChild(flashLine);
    });
  }

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
    print("Replaced selectConstructionSection with clean line-only version")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Removed pulse rings from section selection successfully!")
