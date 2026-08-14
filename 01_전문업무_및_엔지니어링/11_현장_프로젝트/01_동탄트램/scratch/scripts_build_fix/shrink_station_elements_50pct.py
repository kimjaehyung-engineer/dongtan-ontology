import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS @keyframes stationTargetPulse to 50% scale
old_css_pulse = r'@keyframes stationTargetPulse \{[\s\S]*?\}'
new_css_pulse = """@keyframes stationTargetPulse {
      0% { r: 6px; opacity: 0.95; stroke-width: 2px; }
      50% { r: 16px; opacity: 0.55; stroke-width: 1.5px; }
      100% { r: 28px; opacity: 0; stroke-width: 0.8px; }
    }"""

if re.search(old_css_pulse, content):
    content = re.sub(old_css_pulse, new_css_pulse, content, count=1)
    print("Updated CSS @keyframes stationTargetPulse to 50% scale!")

# 2. Update renderStationTargetOverlay function with exact 50% scaled parameters
old_func_pattern = r'function renderStationTargetOverlay\(id, pt, detail\)\s*\{[\s\S]*?\n\}'

new_func_code = """function renderStationTargetOverlay(id, pt, detail) {
  let overlayGroup = document.getElementById("station-pulse-overlay");
  if (!overlayGroup) {
    overlayGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    overlayGroup.setAttribute("id", "station-pulse-overlay");
    const mapSvg = document.getElementById("map-svg");
    if (mapSvg) mapSvg.appendChild(overlayGroup);
  }
  overlayGroup.innerHTML = "";

  const stnName = detail ? (detail.name || id) : id;
  const fullLabelText = `🚊 ${formatCleanStationLabel(id, stnName)}`;

  // 1. Inner Cyan Glowing Core Aura (50% Scaled: r=7)
  const aura = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  aura.setAttribute("cx", pt.x); aura.setAttribute("cy", pt.y);
  aura.setAttribute("r", "7");
  aura.setAttribute("fill", "#06b6d4");
  aura.setAttribute("opacity", "0.35");
  aura.setAttribute("filter", "url(#glow)");
  overlayGroup.appendChild(aura);

  // 2. Double Concentric Expanding Target Pulse Rings (50% Scaled)
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

  // 3. Station Core Marker Point (50% Scaled: r=3.8, stroke-width=1.0)
  const coreCircle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  coreCircle.setAttribute("cx", pt.x); coreCircle.setAttribute("cy", pt.y);
  coreCircle.setAttribute("r", "3.8");
  coreCircle.setAttribute("fill", "#0284c7");
  coreCircle.setAttribute("stroke", "#ffffff");
  coreCircle.setAttribute("stroke-width", "1.0");
  coreCircle.setAttribute("filter", "drop-shadow(0 1px 3px rgba(0,0,0,0.4))");
  overlayGroup.appendChild(coreCircle);

  // 4. Compact 50% Micro 3D Station Pin Badge (y=-15, height=13, font=8px)
  const gBadge = document.createElementNS("http://www.w3.org/2000/svg", "g");
  gBadge.setAttribute("transform", `translate(${pt.x}, ${pt.y - 15})`);

  // Pointer Triangle pointing down
  const triangle = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
  triangle.setAttribute("points", "0,5 -3,1 3,1");
  triangle.setAttribute("fill", "#0f172a");
  gBadge.appendChild(triangle);

  // Compact Badge Container Box
  const badgeWidth = Math.max(34, fullLabelText.length * 5.8 + 10);
  const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  rect.setAttribute("x", -badgeWidth / 2);
  rect.setAttribute("y", -7);
  rect.setAttribute("width", badgeWidth);
  rect.setAttribute("height", "13");
  rect.setAttribute("fill", "#0f172a");
  rect.setAttribute("stroke", "#38bdf8");
  rect.setAttribute("stroke-width", "1.0");
  rect.setAttribute("rx", "6.5");
  rect.setAttribute("filter", "drop-shadow(0 2px 4px rgba(0,0,0,0.35))");
  gBadge.appendChild(rect);

  // Compact Badge Text Label (8px)
  const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
  text.setAttribute("x", "0");
  text.setAttribute("y", "2.5");
  text.setAttribute("text-anchor", "middle");
  text.setAttribute("font-family", "Noto Sans KR, sans-serif");
  text.setAttribute("font-size", "8.0px");
  text.setAttribute("font-weight", "900");
  text.setAttribute("fill", "#ffffff");
  text.textContent = fullLabelText;
  gBadge.appendChild(text);

  overlayGroup.appendChild(gBadge);
}"""

if re.search(old_func_pattern, content):
    content = re.sub(old_func_pattern, lambda m: new_func_code, content, count=1)
    print("Updated renderStationTargetOverlay to 50% scale!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished applying 50% scale reduction to station badge and core point in V1 HTML!")
