import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Simplify Tabs HTML to exactly 2 clean buttons
old_tabs_pattern = r'<div class="modal-view-mode-tabs"[\s\S]*?</div>'

clean_tabs_html = """<div class="modal-view-mode-tabs" style="display: flex; gap: 0.4rem; background: #cbd5e1; padding: 0.25rem; border-radius: 8px; margin-left: auto; margin-right: 1rem;">
        <button id="tab-btn-diagram" onclick="switchModalViewMode('DIAGRAM')" style="padding: 0.4rem 0.95rem; border: none; border-radius: 6px; font-size: 0.82rem; font-weight: 800; cursor: pointer; background: #0f172a; color: #ffffff; box-shadow: 0 1px 4px rgba(15,23,42,0.25); transition: all 0.2s;">
          📐 2D 시뮬레이션 도식
        </button>
        <button id="tab-btn-naver" onclick="switchModalViewMode('NAVER')" style="padding: 0.4rem 0.95rem; border: none; border-radius: 6px; font-size: 0.82rem; font-weight: 800; cursor: pointer; background: transparent; color: #475569; transition: all 0.2s;">
          🗺️ 네이버 지도 실시간 위치
        </button>
      </div>"""

if re.search(old_tabs_pattern, content):
    content = re.sub(old_tabs_pattern, clean_tabs_html, content, count=1)
    print("Simplified modal-view-mode-tabs to 2 clean buttons!")

# 2. Simplify openIntersectionModal to default to DIAGRAM mode
if 'switchModalViewMode("SATELLITE");' in content:
    content = content.replace('switchModalViewMode("SATELLITE");', 'switchModalViewMode("DIAGRAM");')
    print("Set openIntersectionModal default mode to DIAGRAM!")

# 3. Clean JS Engine for 2 Modes
clean_engine_js = """// ============================================================================
// 🔀 2대 뷰어 모드 전환 탭 엔진 (2D 시뮬레이션 도식 ↔ 네이버 지도 실시간 위치)
// ============================================================================
let currentModalItem = null;
let currentModalViewMode = 'DIAGRAM'; // Default mode

function switchModalViewMode(mode) {
  currentModalViewMode = mode;
  const btnDiagram = document.getElementById("tab-btn-diagram");
  const btnNaver = document.getElementById("tab-btn-naver");

  const simToolbar = document.querySelector(".sim-toolbar");
  const diagramWrapper = document.querySelector(".diagram-wrapper");
  const naverContainer = document.getElementById("modal-naver-map-container");

  // Reset button styles
  [btnDiagram, btnNaver].forEach(b => {
    if (b) {
      b.style.background = "transparent";
      b.style.color = "#475569";
      b.style.boxShadow = "none";
      b.style.border = "none";
    }
  });

  if (mode === 'DIAGRAM') {
    if (btnDiagram) {
      btnDiagram.style.background = "#0f172a";
      btnDiagram.style.color = "#ffffff";
      btnDiagram.style.boxShadow = "0 2px 6px rgba(15,23,42,0.35)";
    }

    if (simToolbar) simToolbar.style.display = "flex";
    if (diagramWrapper) diagramWrapper.style.display = "flex";
    if (naverContainer) naverContainer.style.display = "none";

    // Render 2D Simulation Diagram
    renderModalSvgDiagram(currentModalItem);

    // Resume traffic simulation
    if (typeof startTrafficSimulation === 'function') startTrafficSimulation();
  } else if (mode === 'NAVER') {
    if (btnNaver) {
      btnNaver.style.background = "#03c75a";
      btnNaver.style.color = "#ffffff";
      btnNaver.style.boxShadow = "0 2px 6px rgba(3,199,90,0.35)";
    }

    if (simToolbar) simToolbar.style.display = "none";
    if (diagramWrapper) diagramWrapper.style.display = "none";
    if (naverContainer) naverContainer.style.display = "flex";

    // Pause simulation while viewing portal map
    if (typeof stopTrafficSimulation === 'function') stopTrafficSimulation();

    renderNaverMapView(currentModalItem);
  }
}

function renderModalSvgDiagram(item) {
  const svg = document.getElementById("modal-svg-diagram");
  if (!svg || !item) return;

  const is1 = item.tool === "1공구";
  const mainColor = is1 ? "#ea580c" : "#2563eb";
  const lightBg = is1 ? "#fff7ed" : "#eff6ff";

  svg.innerHTML = `
    <defs>
      <linearGradient id="roadGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#cbd5e1"/>
        <stop offset="50%" stop-color="#94a3b8"/>
        <stop offset="100%" stop-color="#cbd5e1"/>
      </linearGradient>
      <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="3" result="blur"/>
        <feComposite in="SourceGraphic" in2="blur" operator="over"/>
      </filter>
    </defs>

    <!-- Background Canvas -->
    <rect x="0" y="0" width="800" height="380" fill="#f8fafc" rx="8"/>

    <!-- Main Road Surface (Horizontal 6-Lane) -->
    <rect x="40" y="100" width="720" height="160" fill="url(#roadGrad)" rx="6"/>
    <!-- Cross Road Surface (Vertical 4-Lane) -->
    <rect x="320" y="30" width="160" height="300" fill="url(#roadGrad)" rx="6"/>

    <!-- Road Center Lines (Yellow Double Lines) -->
    <line x1="40" y1="179" x2="760" y2="179" stroke="#eab308" stroke-width="2.5" stroke-dasharray="12, 8"/>
    <line x1="40" y1="181" x2="760" y2="181" stroke="#eab308" stroke-width="2.5" stroke-dasharray="12, 8"/>

    <line x1="399" y1="30" x2="399" y2="330" stroke="#eab308" stroke-width="2.5" stroke-dasharray="12, 8"/>
    <line x1="401" y1="30" x2="401" y2="330" stroke="#eab308" stroke-width="2.5" stroke-dasharray="12, 8"/>

    <!-- White Lane Dividers -->
    <line x1="40" y1="130" x2="760" y2="130" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="8, 8"/>
    <line x1="40" y1="230" x2="760" y2="230" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="8, 8"/>

    <!-- Crosswalk Stripes -->
    <g fill="#ffffff" opacity="0.9">
      <rect x="290" y="105" width="6" height="150"/>
      <rect x="275" y="105" width="6" height="150"/>
      <rect x="260" y="105" width="6" height="150"/>
      <rect x="500" y="105" width="6" height="150"/>
      <rect x="515" y="105" width="6" height="150"/>
      <rect x="530" y="105" width="6" height="150"/>
    </g>

    <!-- TRAM DUAL TRACKS (Center Corridor) -->
    <rect x="40" y="165" width="720" height="30" fill="#1e293b" rx="3" stroke="#0284c7" stroke-width="1.5"/>
    <!-- Rails -->
    <line x1="40" y1="170" x2="760" y2="170" stroke="#cbd5e1" stroke-width="2"/>
    <line x1="40" y1="174" x2="760" y2="174" stroke="#cbd5e1" stroke-width="2"/>
    <line x1="40" y1="186" x2="760" y2="186" stroke="#cbd5e1" stroke-width="2"/>
    <line x1="40" y1="190" x2="760" y2="190" stroke="#cbd5e1" stroke-width="2"/>

    <!-- WORK ZONE ENLARGED HIGHLIGHT BOX -->
    <rect x="180" y="90" width="440" height="180" fill="${lightBg}" stroke="${mainColor}" stroke-width="3" stroke-dasharray="6, 4" rx="10" opacity="0.85" filter="url(#glow)"/>

    <!-- Work Zone Banner Badge -->
    <g transform="translate(400, 70)">
      <rect x="-140" y="-18" width="280" height="36" fill="${mainColor}" rx="18" filter="drop-shadow(0 4px 6px rgba(0,0,0,0.2))"/>
      <text x="0" y="5" text-anchor="middle" font-family="Noto Sans KR" font-size="14px" font-weight="900" fill="#ffffff">
        작업구간: ${item.name || ''} (${item.length || 0}m)
      </text>
    </g>

    <!-- STA Start & End Pins -->
    <g transform="translate(180, 180)">
      <line x1="0" y1="-80" x2="0" y2="80" stroke="${mainColor}" stroke-width="2"/>
      <circle cx="0" cy="-80" r="16" fill="${mainColor}"/>
      <text x="0" y="-75" text-anchor="middle" font-family="Noto Sans KR" font-size="10px" font-weight="800" fill="#ffffff">시점</text>
      <rect x="-55" y="45" width="110" height="24" fill="#0f172a" rx="4"/>
      <text x="0" y="61" text-anchor="middle" font-family="Noto Sans KR" font-size="11px" font-weight="700" fill="#ffffff">STA ${item.startSta || 0}m</text>
    </g>

    <g transform="translate(620, 180)">
      <line x1="0" y1="-80" x2="0" y2="80" stroke="${mainColor}" stroke-width="2"/>
      <circle cx="0" cy="-80" r="16" fill="${mainColor}"/>
      <text x="0" y="-75" text-anchor="middle" font-family="Noto Sans KR" font-size="10px" font-weight="800" fill="#ffffff">종점</text>
      <rect x="-55" y="45" width="110" height="24" fill="#0f172a" rx="4"/>
      <text x="0" y="61" text-anchor="middle" font-family="Noto Sans KR" font-size="11px" font-weight="700" fill="#ffffff">STA ${item.endSta || 0}m</text>
    </g>

    <!-- Stage & Method Overlay Badge -->
    <g transform="translate(400, 315)">
      <rect x="-160" y="-16" width="320" height="32" fill="#0f172a" rx="8" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.3))"/>
      <text x="0" y="4" text-anchor="middle" font-family="Noto Sans KR" font-size="13px" font-weight="700" fill="#38bdf8">
        교통처리 ${item.stage || '-'}단계 | 적용공법: ${item.method || '-'}
      </text>
    </g>

    <!-- Dynamic Animated Vehicles & Tram Overlay Layer -->
    <g id="svg-vehicles-group"></g>
  `;
}"""

old_engine_pattern = r'// ============================================================================[\s\S]*?function renderModalSvgDiagram\(item[\s\S]*?\n\}'

if re.search(old_engine_pattern, content):
    content = re.sub(old_engine_pattern, lambda m: clean_engine_js, content, count=1)
    print("Updated JS Engine to clean 2-mode system!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished applying clean 2-mode UI to V1 HTML!")
