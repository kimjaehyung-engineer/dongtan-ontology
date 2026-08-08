import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

html_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

# ============================================
# 1. Add CSS for schedule panel & toggle button
# ============================================
css_insert = """
/* === 09.공정표 연동 대시보드 CSS === */
.schedule-toggle-btn {
  background: linear-gradient(135deg, #0284c7, #2563eb);
  color: #ffffff;
  border: none;
  padding: 0.4rem 0.85rem;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 700;
  font-family: 'Noto Sans KR', sans-serif;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  margin-left: 0.5rem;
}
.schedule-toggle-btn:hover {
  background: linear-gradient(135deg, #0369a1, #1d4ed8);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
}

.schedule-panel-container {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%);
  width: min(96%, 1280px);
  max-height: 380px;
  background: var(--card-bg, #ffffff);
  border: 1px solid var(--border-color, #cbd5e1);
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
  z-index: 1200;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
}

.schedule-panel-container.hidden {
  display: none !important;
}

.schedule-panel-header {
  padding: 0.75rem 1.2rem;
  background: var(--panel-bg, #f8fafc);
  border-bottom: 1px solid var(--border-color, #e2e8f0);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.schedule-title-area {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.schedule-badge {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.2rem 0.55rem;
  border-radius: 50px;
  background: #dbeafe;
  color: #1e40af;
}

.schedule-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-primary, #0f172a);
  margin: 0;
}

.schedule-filter-tabs {
  display: flex;
  gap: 0.35rem;
}

.sch-filter-btn {
  padding: 0.3rem 0.65rem;
  border-radius: 6px;
  border: 1px solid var(--border-color, #cbd5e1);
  background: var(--card-bg, #ffffff);
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-muted, #64748b);
  cursor: pointer;
  transition: all 0.15s ease;
}

.sch-filter-btn.active, .sch-filter-btn:hover {
  background: #2563eb;
  color: #ffffff;
  border-color: #2563eb;
}

.schedule-close-btn {
  background: transparent;
  border: none;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-muted, #64748b);
  cursor: pointer;
  padding: 0.3rem 0.6rem;
  border-radius: 6px;
}
.schedule-close-btn:hover {
  background: #fee2e2;
  color: #dc2626;
}

.schedule-panel-body {
  padding: 0.8rem 1.2rem;
  overflow-y: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.sch-row {
  display: grid;
  grid-template-columns: 240px 1fr 110px 100px;
  align-items: center;
  gap: 0.8rem;
  padding: 0.55rem 0.8rem;
  background: var(--panel-bg, #f8fafc);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sch-row:hover, .sch-row.active {
  background: #eff6ff;
  border-color: #3b82f6;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
}

.sch-row-info {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.sch-row-title {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text-primary, #0f172a);
}

.sch-row-sub {
  font-size: 0.72rem;
  color: var(--text-muted, #64748b);
}

.sch-bar-container {
  position: relative;
  height: 14px;
  background: #e2e8f0;
  border-radius: 7px;
  overflow: hidden;
}

.sch-bar-fill {
  height: 100%;
  border-radius: 7px;
  transition: width 0.4s ease;
}

.sch-bar-fill.tool-1 {
  background: linear-gradient(90deg, #f97316, #ea580c);
}

.sch-bar-fill.tool-2 {
  background: linear-gradient(90deg, #3b82f6, #2563eb);
}

.sch-stat-val {
  font-size: 0.8rem;
  font-weight: 700;
  color: #2563eb;
  text-align: right;
}

.sch-sta-val {
  font-size: 0.74rem;
  color: var(--text-muted, #64748b);
  text-align: right;
}
"""

if '.schedule-toggle-btn' not in text:
  text = text.replace('</style>', css_insert + '\n</style>', 1)
  print("✓ Added schedule panel CSS")

# ============================================
# 2. Add header button html
# ============================================
hdr_anchor = '</header>'
hdr_btn_html = """  <button id="btn-toggle-schedule" class="schedule-toggle-btn">
    📊 09.공정표 연동 대시보드
  </button>
</header>"""

if 'id="btn-toggle-schedule"' not in text:
  text = text.replace(hdr_anchor, hdr_btn_html, 1)
  print("✓ Added header schedule toggle button")

# ============================================
# 3. Add schedule panel container html
# ============================================
body_anchor = '</body>'
panel_html = """  <!-- 09.공정표 연동 대시보드 패널 -->
  <div id="schedule-panel" class="schedule-panel-container hidden">
    <div class="schedule-panel-header">
      <div class="schedule-title-area">
        <span class="schedule-badge">09.공정표 연동</span>
        <h3 class="schedule-title">동탄트램 시공 공정표 & Time-Chainage 연동 대시보드</h3>
      </div>
      <div class="schedule-filter-tabs">
        <button class="sch-filter-btn active" data-filter="all">전체 공정 (28구간)</button>
        <button class="sch-filter-btn" data-filter="1공구">1공구 본선</button>
        <button class="sch-filter-btn" data-filter="2공구">2공구 본선</button>
      </div>
      <button id="btn-close-schedule" class="schedule-close-btn">✕ 닫기</button>
    </div>
    <div class="schedule-panel-body" id="schedule-timeline-body">
      <!-- Dynamically populated schedule Gantt rows -->
    </div>
  </div>
</body>"""

if 'id="schedule-panel"' not in text:
  text = text.replace(body_anchor, panel_html, 1)
  print("✓ Added schedule panel container HTML")

# ============================================
# 4. Add JavaScript schedule timeline logic
# ============================================
js_schedule_logic = """
// === 09.공정표 연동 대시보드 JS Logic ===
function initScheduleIntegration() {
  const toggleBtn = document.getElementById("btn-toggle-schedule");
  const closeBtn = document.getElementById("btn-close-schedule");
  const panel = document.getElementById("schedule-panel");
  const body = document.getElementById("schedule-timeline-body");
  const filterBtns = document.querySelectorAll(".sch-filter-btn");

  if (!toggleBtn || !panel || !body) return;

  toggleBtn.addEventListener("click", () => {
    panel.classList.toggle("hidden");
    if (!panel.classList.contains("hidden")) {
      renderScheduleTimeline("all");
    }
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      panel.classList.add("hidden");
    });
  }

  filterBtns.forEach(btn => {
    btn.addEventListener("click", (e) => {
      filterBtns.forEach(b => b.classList.remove("active"));
      e.target.classList.add("active");
      const filter = e.target.getAttribute("data-filter");
      renderScheduleTimeline(filter);
    });
  });
}

function renderScheduleTimeline(filter = "all") {
  const body = document.getElementById("schedule-timeline-body");
  if (!body) return;
  body.innerHTML = "";

  const filtered = constructionSections.filter(sec => {
    if (filter === "1공구") return sec.tool === "1공구";
    if (filter === "2공구") return sec.tool === "2공구";
    return true;
  });

  const maxDuration = Math.max(...constructionSections.map(s => s.duration || 12), 12);

  filtered.forEach(sec => {
    const is1 = sec.tool === "1공구";
    const durationPercent = Math.min(100, (sec.duration / maxDuration) * 100);

    const row = document.createElement("div");
    row.setAttribute("class", "sch-row");
    row.setAttribute("data-sch-id", sec.no);

    row.innerHTML = `
      <div class="sch-row-info">
        <div class="sch-row-title">[${sec.tool}] ${sec.section}</div>
        <div class="sch-row-sub">STA ${sec.startSta}m ~ ${sec.endSta}m (${sec.length}m)</div>
      </div>
      <div class="sch-bar-container">
        <div class="sch-bar-fill ${is1 ? 'tool-1' : 'tool-2'}" style="width: ${durationPercent.toFixed(1)}%;"></div>
      </div>
      <div class="sch-stat-val">${sec.duration}개월</div>
      <div class="sch-sta-val">${sec.segCount}개 구간</div>
    `;

    row.addEventListener("click", () => {
      document.querySelectorAll(".sch-row").forEach(r => r.classList.remove("active"));
      row.classList.add("active");
      selectConstructionSection(sec);
    });

    body.appendChild(row);
  });
}

// Hook into DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  initScheduleIntegration();
});
"""

# Append JS schedule logic before closing </script> tag
if 'initScheduleIntegration' not in text:
  text = text.replace('</script>', js_schedule_logic + '\n</script>', 1)
  print("✓ Added schedule integration JS logic")

with open(html_path, 'w', encoding='utf-8') as f:
  f.write(text)

print(f"✅ Schedule integration applied successfully! File size: {len(text)} bytes")
