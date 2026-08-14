import sys
import os
import json
import glob

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\intersections_mapped.json', 'r', encoding='utf-8') as f:
    intersections = json.load(f)

search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]

with open(file_v1, 'r', encoding='utf-8') as f:
    v1 = f.read()

# 1. Prepare JS constant string
js_data_str = "const intersectionData = " + json.dumps(intersections, ensure_ascii=False, indent=2) + ";\n"

print("JS data length:", len(js_data_str))

# Print JS rendering function template to check
js_render_code = """
// --- 교차로 정보 렌더링 (단계별 평균작업연장 시각화) ---
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

    // Outer Badge Rect
    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("x", "-25");
    rect.setAttribute("y", "-7");
    rect.setAttribute("width", "50");
    rect.setAttribute("height", "14");
    rect.setAttribute("rx", "3");
    rect.setAttribute("fill", "#fff7ed");
    rect.setAttribute("stroke", "#f97316");
    rect.setAttribute("stroke-width", "0.8");
    rect.setAttribute("filter", "drop-shadow(0 1px 2px rgba(0,0,0,0.15))");

    // Text Label: Name & Avg Len
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", "0");
    text.setAttribute("y", "3");
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("font-family", "Noto Sans KR");
    text.setAttribute("font-size", "4.2px");
    text.setAttribute("font-weight", "700");
    text.setAttribute("fill", "#c2410c");
    text.textContent = `${item.name.slice(0, 8)} (${item.avgLen}m)`;

    g.appendChild(rect);
    g.appendChild(text);

    // Events
    g.addEventListener("mouseenter", (e) => {
      showTooltip(e, `[${item.tool} ${item.no}번 교차로] ${item.name}<br>· STA: ${item.startSta}~${item.endSta}m (연장 ${item.length}m)<br>· 공법: ${item.method} (${item.stage}단계)<br>· <b>단계별 평균작업연장: ${item.avgLen}m</b>`);
    });
    g.addEventListener("mouseleave", hideTooltip);

    g.addEventListener("click", (e) => {
      e.stopPropagation();
      selectIntersection(item);
    });

    intersectionsGroup.appendChild(g);
  });
}

function selectIntersection(item) {
  // Focus SVG on position
  panTo(item.x, item.y);
  
  // Populate Side Panel
  const stnNameEl = document.getElementById("stn-name");
  const stnTypeEl = document.getElementById("stn-type");
  const tabStnContent = document.getElementById("tab-stn-content");
  
  if (stnNameEl) stnNameEl.textContent = item.name;
  if (stnTypeEl) stnTypeEl.textContent = `${item.tool} 교차로 구간 (${item.code})`;
  
  const detailContainer = document.getElementById("stn-detail-container");
  if (detailContainer) {
    detailContainer.innerHTML = `
      <div style="background: var(--card-bg); border: 1.5px solid #f97316; border-radius: 10px; padding: 1rem; margin-top: 0.8rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
          <span style="font-weight: 700; color: #f97316; font-size: 0.9rem;">🚧 교차로 시공 공기정보</span>
          <span style="background: #ffedd5; color: #c2410c; padding: 0.2rem 0.6rem; border-radius: 50px; font-size: 0.75rem; font-weight: 700;">${item.tool} #${item.no}</span>
        </div>
        <table style="width: 100%; border-collapse: collapse; font-size: 0.82rem; margin-top: 0.5rem;">
          <tr style="border-bottom: 1px solid var(--border-color);"><td style="padding: 0.4rem; color: var(--text-muted);">구간 명칭</td><td style="padding: 0.4rem; font-weight: 600;">${item.name} (${item.code})</td></tr>
          <tr style="border-bottom: 1px solid var(--border-color);"><td style="padding: 0.4rem; color: var(--text-muted);">체이닝 (STA)</td><td style="padding: 0.4rem; font-weight: 600;">${item.startSta}m ~ ${item.endSta}m</td></tr>
          <tr style="border-bottom: 1px solid var(--border-color);"><td style="padding: 0.4rem; color: var(--text-muted);">구간 총 연장</td><td style="padding: 0.4rem; font-weight: 600;">${item.length}m</td></tr>
          <tr style="border-bottom: 1px solid var(--border-color);"><td style="padding: 0.4rem; color: var(--text-muted);">적용 공법</td><td style="padding: 0.4rem; font-weight: 600;">${item.method}</td></tr>
          <tr style="border-bottom: 1px solid var(--border-color);"><td style="padding: 0.4rem; color: var(--text-muted);">교통처리 단계</td><td style="padding: 0.4rem; font-weight: 600;">${item.stage}단계</td></tr>
          <tr style="background: rgba(249, 115, 22, 0.15);"><td style="padding: 0.5rem; color: #ea580c; font-weight: 700;">단계별 평균작업연장</td><td style="padding: 0.5rem; color: #ea580c; font-weight: 800; font-size: 0.95rem;">${item.avgLen} m</td></tr>
        </table>
      </div>
    `;
  }
}
"""
print("JS render code prepared.")
