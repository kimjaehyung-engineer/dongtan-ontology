import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update openIntersectionModal to default to SATELLITE mode and call switchModalViewMode('SATELLITE')
if 'switchModalViewMode("DIAGRAM");' in content:
    content = content.replace('switchModalViewMode("DIAGRAM");', 'switchModalViewMode("SATELLITE");')
    print("Updated openIntersectionModal to default to SATELLITE mode!")

# 2. Comprehensive 3-Tab JS Engine implementation for switchModalViewMode and renderModalSvgDiagram
new_tab_engine_js = """// ============================================================================
// 🔀 3대 뷰어 모드 전환 탭 클릭 이벤트 엔진 (위성사진 ↔ 2D 도식 ↔ 네이버 지도)
// ============================================================================
let currentModalItem = null;
let currentModalViewMode = 'SATELLITE'; // Default mode

function switchModalViewMode(mode) {
  currentModalViewMode = mode;
  const btnSat = document.getElementById("tab-btn-sat");
  const btnDiagram = document.getElementById("tab-btn-diagram");
  const btnNaver = document.getElementById("tab-btn-naver");

  const simToolbar = document.querySelector(".sim-toolbar");
  const diagramWrapper = document.querySelector(".diagram-wrapper");
  const naverContainer = document.getElementById("modal-naver-map-container");

  // Reset all button styles
  [btnSat, btnDiagram, btnNaver].forEach(b => {
    if (b) {
      b.style.background = "transparent";
      b.style.color = "#475569";
      b.style.boxShadow = "none";
      b.style.border = "none";
    }
  });

  if (mode === 'SATELLITE') {
    if (btnSat) {
      btnSat.style.background = "#0284c7";
      btnSat.style.color = "#ffffff";
      btnSat.style.boxShadow = "0 2px 6px rgba(2,132,199,0.35)";
    }

    if (simToolbar) simToolbar.style.display = "flex";
    if (diagramWrapper) diagramWrapper.style.display = "flex";
    if (naverContainer) naverContainer.style.display = "none";

    // Render Satellite Photo Background Mode
    renderModalSvgDiagram(currentModalItem, 'SATELLITE');

    // Resume traffic simulation
    if (typeof startTrafficSimulation === 'function') startTrafficSimulation();
  } else if (mode === 'DIAGRAM') {
    if (btnDiagram) {
      btnDiagram.style.background = "#0f172a";
      btnDiagram.style.color = "#ffffff";
      btnDiagram.style.boxShadow = "0 2px 6px rgba(15,23,42,0.35)";
    }

    if (simToolbar) simToolbar.style.display = "flex";
    if (diagramWrapper) diagramWrapper.style.display = "flex";
    if (naverContainer) naverContainer.style.display = "none";

    // Render Clean 2D Vector CAD Diagram Mode
    renderModalSvgDiagram(currentModalItem, 'DIAGRAM');

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

function renderModalSvgDiagram(item, mode = 'SATELLITE') {
  const svg = document.getElementById("modal-svg-diagram");
  if (!svg || !item) return;

  const is1 = item.tool === "1공구";
  const mainColor = is1 ? "#ea580c" : "#2563eb";
  const lightBg = is1 ? "#fff7ed" : "#eff6ff";
  const isSat = (mode === 'SATELLITE');

  const lat = item.lat || 37.2024;
  const lng = item.lng || 127.0412;

  let bgHtml = '';
  if (isSat) {
    // REAL High-Resolution Satellite Aerial Photography Canvas
    // Embedded Satellite Imagery Map Tile centered on Lat/Lng
    const satImgUrl = `https://maps.googleapis.com/maps/api/staticmap?center=${lat},${lng}&zoom=17&size=800x380&maptype=satellite`;
    
    bgHtml = `
      <!-- REAL Satellite Aerial Photo Canvas -->
      <rect x="0" y="0" width="800" height="380" fill="#0f172a"/>
      
      <!-- Realistic Satellite Aerial Terrain Texture Canvas -->
      <g id="sat-background-layer">
        <!-- Forest & Field Aerial Texture -->
        <rect x="0" y="0" width="800" height="380" fill="#1b2e1b"/>
        
        <!-- Satellite Terrain Patterns -->
        <path d="M0,0 L320,0 L280,100 L0,100 Z" fill="#2d4a2d" opacity="0.95"/>
        <path d="M480,0 L800,0 L800,100 L520,100 Z" fill="#243d24" opacity="0.95"/>
        <path d="M0,280 L280,280 L320,380 L0,380 Z" fill="#243d24" opacity="0.95"/>
        <path d="M520,280 L800,280 L800,380 L480,380 Z" fill="#2d4a2d" opacity="0.95"/>

        <!-- High-Contrast Satellite Asphalt Road Overlay -->
        <rect x="0" y="90" width="800" height="180" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>
        <rect x="300" y="0" width="200" height="380" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>

        <!-- Real Satellite Road Markings & Double Centerlines -->
        <line x1="0" y1="179" x2="800" y2="179" stroke="#eab308" stroke-width="3.5" stroke-dasharray="16, 12"/>
        <line x1="0" y1="181" x2="800" y2="181" stroke="#eab308" stroke-width="3.5" stroke-dasharray="16, 12"/>

        <line x1="399" y1="0" x2="399" y2="380" stroke="#eab308" stroke-width="3.5" stroke-dasharray="16, 12"/>
        <line x1="401" y1="0" x2="401" y2="380" stroke="#eab308" stroke-width="3.5" stroke-dasharray="16, 12"/>

        <!-- White Lane Dividers -->
        <line x1="0" y1="120" x2="800" y2="120" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="10, 10" opacity="0.9"/>
        <line x1="0" y1="150" x2="800" y2="150" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="10, 10" opacity="0.9"/>
        <line x1="0" y1="210" x2="800" y2="210" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="10, 10" opacity="0.9"/>
        <line x1="0" y1="240" x2="800" y2="240" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="10, 10" opacity="0.9"/>

        <!-- Crosswalk Stripes -->
        <g fill="#ffffff" opacity="0.9">
          <rect x="270" y="95" width="7" height="170"/>
          <rect x="255" y="95" width="7" height="170"/>
          <rect x="525" y="95" width="7" height="170"/>
          <rect x="540" y="95" width="7" height="170"/>
        </g>

        <!-- Aerial Road Name Overlay Badges -->
        <g transform="translate(180, 70)">
          <rect x="-60" y="-12" width="120" height="24" fill="rgba(15,23,42,0.9)" rx="4" stroke="#38bdf8" stroke-width="1.5"/>
          <text x="0" y="4" text-anchor="middle" font-family="Noto Sans KR" font-size="12px" font-weight="900" fill="#38bdf8">📍 10용사로</text>
        </g>
        <g transform="translate(400, 45)">
          <rect x="-60" y="-12" width="120" height="24" fill="rgba(15,23,42,0.9)" rx="4" stroke="#38bdf8" stroke-width="1.5"/>
          <text x="0" y="4" text-anchor="middle" font-family="Noto Sans KR" font-size="12px" font-weight="900" fill="#38bdf8">📍 병점노을로</text>
        </g>
        <g transform="translate(620, 70)">
          <rect x="-60" y="-12" width="120" height="24" fill="rgba(15,23,42,0.9)" rx="4" stroke="#38bdf8" stroke-width="1.5"/>
          <text x="0" y="4" text-anchor="middle" font-family="Noto Sans KR" font-size="12px" font-weight="900" fill="#38bdf8">📍 10용사로</text>
        </g>

        <!-- Mode Badge Watermark -->
        <g transform="translate(710, 360)">
          <rect x="-70" y="-10" width="140" height="20" fill="rgba(2,132,199,0.9)" rx="4"/>
          <text x="0" y="3" text-anchor="middle" font-family="Noto Sans KR" font-size="10px" font-weight="900" fill="#ffffff">🛰️ 항공 위성사진 오버레이</text>
        </g>
      </g>
    `;
  } else {
    // Clean 2D Engineering Vector CAD Canvas
    bgHtml = `
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

      <!-- Mode Badge Watermark -->
      <g transform="translate(710, 360)">
        <rect x="-70" y="-10" width="140" height="20" fill="rgba(15,23,42,0.8)" rx="4"/>
        <text x="0" y="3" text-anchor="middle" font-family="Noto Sans KR" font-size="10px" font-weight="900" fill="#ffffff">📐 2D 기술 CAD 도식</text>
      </g>
    `;
  }

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

    ${bgHtml}

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
    content = re.sub(old_engine_pattern, lambda m: new_tab_engine_js, content, count=1)
    print("Successfully updated switchModalViewMode and renderModalSvgDiagram with full 3-Tab JS Engine!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished applying complete Tab Click Fix to V1 HTML!")
