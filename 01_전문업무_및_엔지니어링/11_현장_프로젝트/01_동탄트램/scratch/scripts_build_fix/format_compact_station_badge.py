import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update renderStationTargetOverlay function for compact badge design
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
  
  // Format clean concise label: e.g. "🚊 115" or "🚊 301 (병점역)"
  let cleanStnLabel = id;
  if (stnName && stnName !== id && stnName !== `${id}정거장` && stnName !== `${id}역`) {
    const displayName = stnName.replace(/정거장$/, '').trim();
    if (displayName && displayName !== id) {
      cleanStnLabel = `${id} (${displayName})`;
    }
  }
  const fullLabelText = `🚊 ${cleanStnLabel}`;

  // 1. Inner Cyan Glowing Core Aura
  const aura = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  aura.setAttribute("cx", pt.x); aura.setAttribute("cy", pt.y);
  aura.setAttribute("r", "12");
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
  coreCircle.setAttribute("r", "7.5");
  coreCircle.setAttribute("fill", "#0284c7");
  coreCircle.setAttribute("stroke", "#ffffff");
  coreCircle.setAttribute("stroke-width", "2");
  coreCircle.setAttribute("filter", "drop-shadow(0 2px 4px rgba(0,0,0,0.4))");
  overlayGroup.appendChild(coreCircle);

  // 4. Compact Slim 3D Station Pin Badge
  const gBadge = document.createElementNS("http://www.w3.org/2000/svg", "g");
  gBadge.setAttribute("transform", `translate(${pt.x}, ${pt.y - 28})`);

  // Pointer Triangle pointing down
  const triangle = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
  triangle.setAttribute("points", "0,9 -5,2 5,2");
  triangle.setAttribute("fill", "#0f172a");
  gBadge.appendChild(triangle);

  // Compact Badge Container Box
  const badgeWidth = Math.max(54, fullLabelText.length * 7.5 + 20);
  const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  rect.setAttribute("x", -badgeWidth / 2);
  rect.setAttribute("y", -11);
  rect.setAttribute("width", badgeWidth);
  rect.setAttribute("height", "20");
  rect.setAttribute("fill", "#0f172a");
  rect.setAttribute("stroke", "#38bdf8");
  rect.setAttribute("stroke-width", "1.5");
  rect.setAttribute("rx", "10");
  rect.setAttribute("filter", "drop-shadow(0 2px 5px rgba(0,0,0,0.35))");
  gBadge.appendChild(rect);

  // Compact Badge Text Label
  const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
  text.setAttribute("x", "0");
  text.setAttribute("y", "3");
  text.setAttribute("text-anchor", "middle");
  text.setAttribute("font-family", "Noto Sans KR, sans-serif");
  text.setAttribute("font-size", "10.5px");
  text.setAttribute("font-weight", "800");
  text.setAttribute("fill", "#ffffff");
  text.textContent = fullLabelText;
  gBadge.appendChild(text);

  overlayGroup.appendChild(gBadge);
}"""

if re.search(old_func_pattern, content):
    content = re.sub(old_func_pattern, lambda m: new_func_code, content, count=1)
    print("Updated renderStationTargetOverlay to compact badge style!")

# 2. Update quickNav dropdown option formatting
old_option_code = r'option\.textContent = `\${id}역 - \${detail\.name}`;'
new_option_code = """let optName = detail.name || id;
    if (optName === `${id}정거장` || optName === `${id}역`) optName = id;
    else optName = `${id} (${optName.replace('정거장','').trim()})`;
    option.textContent = optName;"""

if re.search(old_option_code, content):
    content = re.sub(old_option_code, new_option_code, content, count=1)
    print("Updated quickNav dropdown option formatting!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished applying compact station badge formatting to V1 HTML!")
