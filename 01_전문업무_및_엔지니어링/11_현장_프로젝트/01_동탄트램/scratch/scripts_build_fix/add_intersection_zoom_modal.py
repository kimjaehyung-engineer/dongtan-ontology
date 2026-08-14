import sys
import os
import glob
import re

sys.stdout.reconfigure(encoding='utf-8')

search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Adding Enlarged Intersection Zoom Modal to V1 HTML:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for Modal
css_modal_code = """
/* --- 교차로 상세 확대 도면 모달 CSS --- */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(8px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.modal-overlay.open {
  opacity: 1;
  pointer-events: auto;
}

.modal-container {
  background: var(--card-bg, #ffffff);
  width: 92%;
  max-width: 960px;
  max-height: 90vh;
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.35);
  border: 1px solid var(--border-color, #e2e8f0);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transform: scale(0.92);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-overlay.open .modal-container {
  transform: scale(1);
}

.modal-header {
  padding: 1.2rem 1.5rem;
  background: var(--bg-secondary, #f8fafc);
  border-bottom: 1px solid var(--border-color, #e2e8f0);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title-group {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  flex-wrap: wrap;
}

.modal-tool-badge {
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.25rem 0.7rem;
  border-radius: 50px;
  background: #ffedd5;
  color: #c2410c;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--text-primary, #0f172a);
  margin: 0;
}

.modal-sta-badge {
  font-size: 0.8rem;
  font-weight: 600;
  color: #64748b;
  background: #f1f5f9;
  padding: 0.2rem 0.6rem;
  border-radius: 6px;
}

.modal-close-btn {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
  padding: 0.3rem 0.6rem;
  border-radius: 8px;
  transition: background 0.2s;
}

.modal-close-btn:hover {
  background: #e2e8f0;
  color: #0f172a;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.diagram-wrapper {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.04);
  display: flex;
  justify-content: center;
  align-items: center;
}

.diagram-wrapper svg {
  width: 100%;
  height: auto;
  max-height: 380px;
}

.specs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.spec-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 0.9rem 1.1rem;
}

.spec-card-title {
  font-size: 0.75rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  margin-bottom: 0.3rem;
}

.spec-card-value {
  font-size: 1.15rem;
  font-weight: 800;
  color: #0f172a;
}
"""

if '.modal-overlay' not in content:
    pos_style_end = content.find("</style>")
    content = content[:pos_style_end] + css_modal_code + "\n" + content[pos_style_end:]
    print("Added Modal CSS styles!")

# 2. Add Modal HTML Structure before </body>
modal_html = """
<!-- 교차로 상세 확대 도면 팝업 모달 -->
<div id="intersection-zoom-modal" class="modal-overlay" onclick="closeIntersectionModalOnBackdrop(event)">
  <div class="modal-container" onclick="event.stopPropagation()">
    <div class="modal-header">
      <div class="modal-title-group">
        <span id="modal-tool-badge" class="modal-tool-badge">1공구 #1</span>
        <h2 id="modal-title" class="modal-title">교차로 상세 도면</h2>
        <span id="modal-sta-badge" class="modal-sta-badge">STA 0m ~ 0m</span>
      </div>
      <button class="modal-close-btn" onclick="closeIntersectionModal()">✕</button>
    </div>
    <div class="modal-body">
      <!-- 2D High Resolution Schematic View -->
      <div class="diagram-wrapper">
        <svg id="modal-svg-diagram" viewBox="0 0 800 360" preserveAspectRatio="xMidYMid meet">
          <!-- Dynamic SVG diagram content -->
        </svg>
      </div>
      <!-- Spec Details Grid -->
      <div id="modal-specs-grid" class="specs-grid"></div>
    </div>
  </div>
</div>
"""

if 'id="intersection-zoom-modal"' not in content:
    pos_body_end = content.find("</body>")
    content = content[:pos_body_end] + modal_html + "\n" + content[pos_body_end:]
    print("Added Modal HTML markup!")

# 3. Add JS modal opening and dynamic diagram rendering logic
js_modal_logic = """
// --- 교차로 상세 확대 도면 팝업 모달 JS ---
function openIntersectionModal(item) {
  const modal = document.getElementById("intersection-zoom-modal");
  if (!modal) return;

  const is1 = item.tool === "1공구";
  const badgeEl = document.getElementById("modal-tool-badge");
  if (badgeEl) {
    badgeEl.textContent = `${item.tool} #${item.no}`;
    badgeEl.style.background = is1 ? "#ffedd5" : "#dbeafe";
    badgeEl.style.color = is1 ? "#c2410c" : "#1e40af";
  }

  const titleEl = document.getElementById("modal-title");
  if (titleEl) titleEl.textContent = `${item.name} 상세 확대 도면`;

  const staEl = document.getElementById("modal-sta-badge");
  if (staEl) staEl.textContent = `STA ${item.startSta}m ~ ${item.endSta}m (총 ${item.length}m)`;

  // Generate SVG Diagram
  renderModalSvgDiagram(item);

  // Render Specs Grid
  const gridEl = document.getElementById("modal-specs-grid");
  if (gridEl) {
    gridEl.innerHTML = `
      <div class="spec-card">
        <div class="spec-card-title">교차로 구간 총 연장</div>
        <div class="spec-card-value" style="color: ${is1 ? '#ea580c' : '#2563eb'};">${item.length} m</div>
      </div>
      <div class="spec-card">
        <div class="spec-card-title">체이닝 위치 (STA)</div>
        <div class="spec-card-value">${item.startSta}m ~ ${item.endSta}m</div>
      </div>
      <div class="spec-card">
        <div class="spec-card-title">적용 공법</div>
        <div class="spec-card-value">${item.method}</div>
      </div>
      <div class="spec-card">
        <div class="spec-card-title">교통처리 단계</div>
        <div class="spec-card-value">${item.stage} 단계</div>
      </div>
    `;
  }

  modal.classList.add("open");
}

function closeIntersectionModal() {
  const modal = document.getElementById("intersection-zoom-modal");
  if (modal) modal.classList.remove("open");
}

function closeIntersectionModalOnBackdrop(e) {
  if (e.target.id === "intersection-zoom-modal") {
    closeIntersectionModal();
  }
}

// ESC Key listener to close modal
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeIntersectionModal();
});

function renderModalSvgDiagram(item) {
  const svg = document.getElementById("modal-svg-diagram");
  if (!svg) return;

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
    <rect x="0" y="0" width="800" height="360" fill="#f8fafc" rx="8"/>

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
      <!-- West Crosswalk -->
      <rect x="290" y="105" width="6" height="150"/>
      <rect x="275" y="105" width="6" height="150"/>
      <rect x="260" y="105" width="6" height="150"/>

      <!-- East Crosswalk -->
      <rect x="500" y="105" width="6" height="150"/>
      <rect x="515" y="105" width="6" height="150"/>
      <rect x="530" y="105" width="6" height="150"/>
    </g>

    <!-- TRAM DUAL TRACKS (Center Corridor) -->
    <rect x="40" y="165" width="720" height="30" fill="#334155" rx="3"/>
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
        작업구간: ${item.name} (${item.length}m)
      </text>
    </g>

    <!-- STA Start & End Pins -->
    <g transform="translate(180, 180)">
      <line x1="0" y1="-80" x2="0" y2="80" stroke="${mainColor}" stroke-width="2"/>
      <circle cx="0" cy="-80" r="16" fill="${mainColor}"/>
      <text x="0" y="-75" text-anchor="middle" font-family="Noto Sans KR" font-size="10px" font-weight="800" fill="#ffffff">시점</text>
      <rect x="-55" y="45" width="110" height="24" fill="#0f172a" rx="4"/>
      <text x="0" y="61" text-anchor="middle" font-family="Noto Sans KR" font-size="11px" font-weight="700" fill="#ffffff">STA ${item.startSta}m</text>
    </g>

    <g transform="translate(620, 180)">
      <line x1="0" y1="-80" x2="0" y2="80" stroke="${mainColor}" stroke-width="2"/>
      <circle cx="0" cy="-80" r="16" fill="${mainColor}"/>
      <text x="0" y="-75" text-anchor="middle" font-family="Noto Sans KR" font-size="10px" font-weight="800" fill="#ffffff">종점</text>
      <rect x="-55" y="45" width="110" height="24" fill="#0f172a" rx="4"/>
      <text x="0" y="61" text-anchor="middle" font-family="Noto Sans KR" font-size="11px" font-weight="700" fill="#ffffff">STA ${item.endSta}m</text>
    </g>

    <!-- Stage & Method Overlay Badge -->
    <g transform="translate(400, 290)">
      <rect x="-160" y="-16" width="320" height="32" fill="#0f172a" rx="8" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.3))"/>
      <text x="0" y="4" text-anchor="middle" font-family="Noto Sans KR" font-size="13px" font-weight="700" fill="#38bdf8">
        교통처리 ${item.stage}단계 | 적용공법: ${item.method}
      </text>
    </g>
  `;
}
"""

if 'function openIntersectionModal' not in content:
    pos_js_end = content.rfind("</script>")
    content = content[:pos_js_end] + js_modal_logic + "\n" + content[pos_js_end:]
    print("Added Modal JS functions!")

# 4. Trigger Modal on Card Click & Add Button to Active Drawer Card
content = content.replace(
    'selectIntersection(item);',
    'selectIntersection(item);\n      openIntersectionModal(item);'
)

# Also add button inside selectIntersection activeCard innerHTML
old_active_table_end = "</table>\n      </div>"
new_active_table_end = """</table>

        <!-- Large Modal Zoom View Button -->
        <button onclick="openIntersectionModal(intersectionData.find(i=>i.tool==='${item.tool}'&&i.no===${item.no}))" style="width: 100%; margin-top: 1rem; padding: 0.75rem; background: ${is1 ? '#ea580c' : '#2563eb'}; color: #ffffff; border: none; border-radius: 8px; font-size: 0.88rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.5rem; box-shadow: 0 4px 12px ${is1 ? 'rgba(234, 88, 12, 0.3)' : 'rgba(37, 99, 235, 0.3)'}; transition: transform 0.15s ease;">
          <span>🔍 교차로 상세 확대 도면 보기</span>
        </button>
      </div>"""

if old_active_table_end in content:
    content = content.replace(old_active_table_end, new_active_table_end)
    print("Added Zoom Modal button to Drawer active card!")

with open(file_v1, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished integrating Enlarged Intersection Zoom Modal into V1 HTML!")
