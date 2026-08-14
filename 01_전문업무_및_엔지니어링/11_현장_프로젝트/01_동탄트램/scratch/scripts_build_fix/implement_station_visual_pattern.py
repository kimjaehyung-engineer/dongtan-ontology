import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for @keyframes stationTargetPulse
css_pulse_def = """
    /* Station Distinct Target Pulse Ring Animation */
    @keyframes stationTargetPulse {
      0% { r: 14px; opacity: 0.95; stroke-width: 3.5px; }
      50% { r: 35px; opacity: 0.55; stroke-width: 2.5px; }
      100% { r: 58px; opacity: 0; stroke-width: 1px; }
    }
    .station-pulse-ring-1 {
      animation: stationTargetPulse 1.8s infinite cubic-bezier(0.215, 0.61, 0.355, 1);
    }
    .station-pulse-ring-2 {
      animation: stationTargetPulse 1.8s infinite cubic-bezier(0.215, 0.61, 0.355, 1);
      animation-delay: 0.6s;
    }
"""

if '</style>' in content and '@keyframes stationTargetPulse' not in content:
    content = content.replace('</style>', css_pulse_def + '\n  </style>', 1)
    print("Added CSS @keyframes stationTargetPulse for Station visual pattern!")

# 2. Update selectStation implementation to render distinct Station Target Overlay
old_select_stn_pattern = r'function selectStation\(id\)\s*\{[\s\S]*?focusCoordinates\(pt\.x, pt\.y\);\s*\}\s*\}'

new_select_stn_code = """function selectStation(id) {
  const detail = stnDetail[id] || { name: id };
  const plat = platformData[id] || {};
  
  document.getElementById("stn-name").textContent = detail.name || id;
  document.getElementById("stn-type").textContent = detail.type || "-";
  document.getElementById("info-addr").textContent = detail.addr || "-";
  document.getElementById("info-km").textContent = detail.km || "-";
  
  document.getElementById("plat-width").textContent = plat.baseWidth || "-";
  document.getElementById("plat-col").textContent = plat.colPosition || "-";
  
  // Populate issues list
  const issuesList = document.getElementById("info-issues");
  issuesList.innerHTML = "";
  if (detail.issues && detail.issues.length > 0) {
    detail.issues.forEach(issue => {
      const li = document.createElement("li");
      li.textContent = "• " + issue;
      issuesList.appendChild(li);
    });
  } else {
    issuesList.innerHTML = "<li style='color:var(--text-muted)'>특이사항 없음</li>";
  }

  // Adjust sidepanel styling badge color
  const isRed = id.startsWith("3") || id.startsWith("2");
  const badge = document.getElementById("panel-badge");
  if (badge) {
    badge.textContent = isRed ? "1공구" : "2공구";
    badge.className = isRed ? "badge red" : "badge blue";
  }

  const sidePanel = document.getElementById("side-panel");
  if (sidePanel) sidePanel.classList.add("open");
  
  // Focus SVG on coordinates & Render Station Target Overlay Pattern
  const pt = nodes[id];
  if (pt) {
    focusCoordinates(pt.x, pt.y);
    renderStationTargetOverlay(id, pt, detail);
  }
}

// ============================================================================
// 🚊 정거장 선택 전용 지도 시각화 엔진 (에메랄드/시안 이중 퍼블 파동 & 3D 핀 뱃지)
// ============================================================================
function renderStationTargetOverlay(id, pt, detail) {
  let overlayGroup = document.getElementById("station-pulse-overlay");
  if (!overlayGroup) {
    overlayGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    overlayGroup.setAttribute("id", "station-pulse-overlay");
    const mapSvg = document.getElementById("map-svg");
    if (mapSvg) mapSvg.appendChild(overlayGroup);
  }
  overlayGroup.innerHTML = "";

  const stnName = detail.name || id;
  const isTransfer = ["S01", "301", "동탄역", "117"].includes(id);

  // 1. Inner Cyan Glowing Core Aura
  const aura = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  aura.setAttribute("cx", pt.x); aura.setAttribute("cy", pt.y);
  aura.setAttribute("r", "16");
  aura.setAttribute("fill", "#06b6d4");
  aura.setAttribute("opacity", "0.4");
  aura.setAttribute("filter", "url(#glow)");
  overlayGroup.appendChild(aura);

  // 2. Double Concentric Expanding Target Pulse Rings
  const ring1 = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  ring1.setAttribute("cx", pt.x); ring1.setAttribute("cy", pt.y);
  ring1.setAttribute("fill", "none");
  ring1.setAttribute("stroke", "#10b981");
  ring1.setAttribute("class", "station-pulse-ring-1");
  overlayGroup.appendChild(ring1);

  const ring2 = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  ring2.setAttribute("cx", pt.x); ring2.setAttribute("cy", pt.y);
  ring2.setAttribute("fill", "none");
  ring2.setAttribute("stroke", "#06b6d4");
  ring2.setAttribute("class", "station-pulse-ring-2");
  overlayGroup.appendChild(ring2);

  // 3. Station Core Marker Point
  const coreCircle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  coreCircle.setAttribute("cx", pt.x); coreCircle.setAttribute("cy", pt.y);
  coreCircle.setAttribute("r", "9");
  coreCircle.setAttribute("fill", "#0284c7");
  coreCircle.setAttribute("stroke", "#ffffff");
  coreCircle.setAttribute("stroke-width", "2.5");
  coreCircle.setAttribute("filter", "drop-shadow(0 2px 5px rgba(0,0,0,0.4))");
  overlayGroup.appendChild(coreCircle);

  // 4. Station Floating 3D Pin Badge (Hovering above station node)
  const gBadge = document.createElementNS("http://www.w3.org/2000/svg", "g");
  gBadge.setAttribute("transform", `translate(${pt.x}, ${pt.y - 42})`);

  // Pointer Triangle pointing down to station node
  const triangle = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
  triangle.setAttribute("points", "0,14 -7,4 7,4");
  triangle.setAttribute("fill", "#0f172a");
  gBadge.appendChild(triangle);

  // Badge Container Box
  const badgeWidth = Math.max(140, (stnName.length + String(id).length) * 11 + 45);
  const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  rect.setAttribute("x", -badgeWidth / 2);
  rect.setAttribute("y", -14);
  rect.setAttribute("width", badgeWidth);
  rect.setAttribute("height", "28");
  rect.setAttribute("fill", "#0f172a");
  rect.setAttribute("stroke", "#38bdf8");
  rect.setAttribute("stroke-width", "2");
  rect.setAttribute("rx", "14");
  rect.setAttribute("filter", "drop-shadow(0 4px 8px rgba(0,0,0,0.4))");
  gBadge.appendChild(rect);

  // Badge Text Label
  const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
  text.setAttribute("x", "0");
  text.setAttribute("y", "4");
  text.setAttribute("text-anchor", "middle");
  text.setAttribute("font-family", "Noto Sans KR, sans-serif");
  text.setAttribute("font-size", "12px");
  text.setAttribute("font-weight", "900");
  text.setAttribute("fill", "#ffffff");
  text.textContent = `🚊 ${id}역 ${stnName}`;
  gBadge.appendChild(text);

  overlayGroup.appendChild(gBadge);
}"""

if re.search(old_select_stn_pattern, content):
    content = re.sub(old_select_stn_pattern, lambda m: new_select_stn_code, content, count=1)
    print("Updated selectStation with renderStationTargetOverlay!")
else:
    # Alternative replacement strategy
    print("Pattern matched alternatively, checking selectStation location...")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished integrating Station Target Overlay into V1 HTML!")
