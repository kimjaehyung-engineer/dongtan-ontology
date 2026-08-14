import sys
import os
import glob
import re

sys.stdout.reconfigure(encoding='utf-8')

# Target V1 HTML file
search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Adding flashing pulse animation to V1 HTML:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS keyframes for pulse animation if not present
css_pulse_code = """
/* --- 교차로 카드 선택 시 위치 번쩍임(Pulse/Blink) 애니메이션 --- */
@keyframes intersectionPulsePing {
  0% {
    r: 3px;
    opacity: 1;
    stroke-width: 2.5px;
  }
  70% {
    r: 18px;
    opacity: 0.75;
    stroke-width: 1.5px;
  }
  100% {
    r: 25px;
    opacity: 0;
    stroke-width: 0.5px;
  }
}

@keyframes intersectionBlinkGlow {
  0%, 100% {
    opacity: 1;
    filter: drop-shadow(0 0 10px #ff3300) drop-shadow(0 0 20px #ff6600);
  }
  50% {
    opacity: 0.25;
    filter: drop-shadow(0 0 2px #ff3300);
  }
}

.pulse-ring-1 {
  animation: intersectionPulsePing 1.4s cubic-bezier(0, 0.2, 0.8, 1) infinite;
}

.pulse-ring-2 {
  animation: intersectionPulsePing 1.4s cubic-bezier(0, 0.2, 0.8, 1) 0.4s infinite;
}

.flashing-route-line {
  animation: intersectionBlinkGlow 0.8s ease-in-out infinite;
}
"""

if 'intersectionPulsePing' not in content:
    pos_style_end = content.find("</style>")
    content = content[:pos_style_end] + css_pulse_code + "\n" + content[pos_style_end:]
    print("Added CSS pulse keyframes!")

# 2. Update selectIntersection(item) JS function
old_select_func_start = content.find("function selectIntersection(item) {")
old_select_func_end = content.find("function setDrawerFilter(", old_select_func_start)

new_select_func = """function selectIntersection(item) {
  // Live recalculation from station node coordinates
  const pos = getPosFromPair(item.stnA, item.stnB, item.ratio);
  const startPos = getPosFromPair(item.startStnA, item.startStnB, item.startRatio);
  const endPos = getPosFromPair(item.endStnA, item.endStnB, item.endRatio);

  const posX = pos.x;
  const posY = pos.y;
  const x1 = startPos.x;
  const y1 = startPos.y;
  const x2 = endPos.x;
  const y2 = endPos.y;

  panTo(posX, posY);
  openIntersectionDrawer();

  // Create or Update Flashing Pulse Ring Overlay Group in SVG
  let pulseGroup = document.getElementById("intersection-pulse-overlay");
  if (!pulseGroup) {
    pulseGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    pulseGroup.setAttribute("id", "intersection-pulse-overlay");
    const mapSvg = document.getElementById("map-svg");
    if (mapSvg) mapSvg.appendChild(pulseGroup);
  }
  pulseGroup.innerHTML = "";

  const is1 = item.tool === "1공구";
  const glowColor = is1 ? "#ff4500" : "#0066ff";

  // 1. Neon Flashing Highlight Route Line Segment
  const flashLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
  flashLine.setAttribute("x1", x1); flashLine.setAttribute("y1", y1);
  flashLine.setAttribute("x2", x2); flashLine.setAttribute("y2", y2);
  flashLine.setAttribute("stroke", glowColor);
  flashLine.setAttribute("stroke-width", "6.5");
  flashLine.setAttribute("stroke-linecap", "round");
  flashLine.setAttribute("class", "flashing-route-line");

  // 2. Dual Pulse Expanding Ping Rings centered at (posX, posY)
  const ring1 = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  ring1.setAttribute("cx", posX); ring1.setAttribute("cy", posY);
  ring1.setAttribute("fill", "none");
  ring1.setAttribute("stroke", glowColor);
  ring1.setAttribute("class", "pulse-ring-1");

  const ring2 = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  ring2.setAttribute("cx", posX); ring2.setAttribute("cy", posY);
  ring2.setAttribute("fill", "none");
  ring2.setAttribute("stroke", glowColor);
  ring2.setAttribute("class", "pulse-ring-2");

  // 3. Center Glowing Beacon Dot
  const beaconDot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  beaconDot.setAttribute("cx", posX); beaconDot.setAttribute("cy", posY);
  beaconDot.setAttribute("r", "2.8");
  beaconDot.setAttribute("fill", "#ffffff");
  beaconDot.setAttribute("stroke", glowColor);
  beaconDot.setAttribute("stroke-width", "1.2");
  beaconDot.setAttribute("class", "flashing-route-line");

  pulseGroup.appendChild(flashLine);
  pulseGroup.appendChild(ring1);
  pulseGroup.appendChild(ring2);
  pulseGroup.appendChild(beaconDot);

  // Render Active KPI Card inside Drawer
  const activeCard = document.getElementById("drawer-active-card");
  if (activeCard) {
    activeCard.innerHTML = `
      <div style="background: var(--card-bg); border: 2px solid ${is1 ? '#f97316' : '#3b82f6'}; border-radius: 12px; padding: 1.2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem;">
          <span style="font-size: 0.75rem; font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 50px; background: ${is1 ? '#ffedd5' : '#dbeafe'}; color: ${is1 ? '#c2410c' : '#1e40af'};">${item.tool} #${item.no}</span>
          <span style="font-size: 0.75rem; color: var(--text-muted);">${item.code}</span>
        </div>
        <h3 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 0.8rem; color: var(--text-primary);">${item.name}</h3>

        <!-- Key Metric KPI -->
        <div style="background: ${is1 ? 'linear-gradient(135deg, #fff7ed, #ffedd5)' : 'linear-gradient(135deg, #eff6ff, #dbeafe)'}; border-radius: 10px; padding: 0.9rem; text-align: center; margin-bottom: 1rem; border: 1px solid ${is1 ? '#fdba74' : '#93c5fd'};">
          <div style="font-size: 0.75rem; font-weight: 700; color: ${is1 ? '#c2410c' : '#1e40af'}; text-transform: uppercase;">교차로 구간 연장</div>
          <div style="font-size: 1.8rem; font-weight: 900; color: ${is1 ? '#ea580c' : '#2563eb'}; margin-top: 0.2rem;">${item.length} <span style="font-size: 1rem;">m</span></div>
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
"""

if old_select_func_start != -1 and old_select_func_end != -1:
    content = content[:old_select_func_start] + new_select_func + "\n\n" + content[old_select_func_end:]
    print("Replaced selectIntersection function with flashing pulse overlay!")

with open(file_v1, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully added flashing pulse animation to V1 HTML!")
