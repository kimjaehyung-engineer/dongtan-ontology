import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Complete Modal JS code
complete_modal_js = """
// --- 교차로 상세 확대 도면 팝업 모달 JS (완벽 복원) ---
function openIntersectionModal(item) {
  if (!item) return;
  const modal = document.getElementById("intersection-zoom-modal");
  if (!modal) return;

  const is1 = item.tool === "1공구";
  const badgeEl = document.getElementById("modal-tool-badge");
  if (badgeEl) {
    badgeEl.textContent = `${item.tool || ''} #${item.no || ''}`;
    badgeEl.style.background = is1 ? "#ffedd5" : "#dbeafe";
    badgeEl.style.color = is1 ? "#c2410c" : "#1e40af";
  }

  const titleEl = document.getElementById("modal-title");
  if (titleEl) titleEl.textContent = `${item.name || '교차로'} 상세 확대 도면`;

  const staEl = document.getElementById("modal-sta-badge");
  if (staEl) staEl.textContent = `STA ${item.startSta || 0}m ~ ${item.endSta || 0}m (총 ${item.length || 0}m)`;

  // Generate SVG Diagram
  renderModalSvgDiagram(item);

  // Render Specs Grid
  const gridEl = document.getElementById("modal-specs-grid");
  if (gridEl) {
    gridEl.innerHTML = `
      <div class="spec-card">
        <div class="spec-card-title">교차로 구간 총 연장</div>
        <div class="spec-card-value" style="color: ${is1 ? '#ea580c' : '#2563eb'};">${item.length || 0} m</div>
      </div>
      <div class="spec-card">
        <div class="spec-card-title">체이닝 위치 (STA)</div>
        <div class="spec-card-value">${item.startSta || 0}m ~ ${item.endSta || 0}m</div>
      </div>
      <div class="spec-card">
        <div class="spec-card-title">적용 공법</div>
        <div class="spec-card-value">${item.method || '-'}</div>
      </div>
      <div class="spec-card">
        <div class="spec-card-title">교통처리 단계</div>
        <div class="spec-card-value">${item.stage || '-'} 단계</div>
      </div>
    `;
  }

  modal.classList.add("open");
  modal.classList.add("active"); // compatibility
}

function closeIntersectionModal() {
  const modal = document.getElementById("intersection-zoom-modal");
  if (modal) {
    modal.classList.remove("open");
    modal.classList.remove("active");
  }
}

function closeIntersectionModalOnBackdrop(e) {
  if (e.target.id === "intersection-zoom-modal") {
    closeIntersectionModal();
  }
}

if (!window._modalEscListenerAdded) {
  window._modalEscListenerAdded = true;
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeIntersectionModal();
  });
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
    <g transform="translate(400, 290)">
      <rect x="-160" y="-16" width="320" height="32" fill="#0f172a" rx="8" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.3))"/>
      <text x="0" y="4" text-anchor="middle" font-family="Noto Sans KR" font-size="13px" font-weight="700" fill="#38bdf8">
        교통처리 ${item.stage || '-'}단계 | 적용공법: ${item.method || '-'}
      </text>
    </g>
  `;
}
"""

# Replace existing openIntersectionModal implementation
pattern_old_func = r'function openIntersectionModal\(item\)\s*\{[\s\S]*?\n\s*function closeIntersectionModal\(\)\s*\{[\s\S]*?\}\n'

if re.search(pattern_old_func, content):
    content = re.sub(pattern_old_func, complete_modal_js + "\n", content, count=1)
    print("Successfully replaced openIntersectionModal & closeIntersectionModal with complete implementation!")
else:
    # Append if not found
    pos_js_end = content.rfind("</script>")
    content = content[:pos_js_end] + complete_modal_js + "\n" + content[pos_js_end:]
    print("Appended complete_modal_js before </script>!")

# Ensure modal CSS supports both .open and .active
if '.modal-overlay.open' in content and '.modal-overlay.active' not in content:
    content = content.replace('.modal-overlay.open', '.modal-overlay.open, .modal-overlay.active')
    print("Updated CSS to support both .open and .active classes!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done updating V1 HTML!")
