import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

html_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'
json_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\activities_db.json'

with open(html_path, 'r', encoding='utf-8') as f:
    html_text = f.read()

with open(json_path, 'r', encoding='utf-8') as f:
    activities_list = json.load(f)

print(f"Loaded {len(activities_list)} activities from activities_db.json")

# Prepare JSON string formatted cleanly for JavaScript
activities_json_str = json.dumps(activities_list, ensure_ascii=False, indent=2)

# Update CSS for 3-Level Accordion/Tree Gantt View
new_css = """
/* === 513개 Activity 계층형 공정표 패널 스타일 === */
.schedule-panel-container {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  width: min(97%, 1320px);
  max-height: 420px;
  background: var(--card-bg, #ffffff);
  border: 1px solid var(--border-color, #cbd5e1);
  border-radius: 14px;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.28);
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
  padding: 0.65rem 1.2rem;
  background: var(--panel-bg, #f8fafc);
  border-bottom: 1px solid var(--border-color, #e2e8f0);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.8rem;
  flex-wrap: wrap;
}

.schedule-title-area {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.schedule-badge {
  font-size: 0.72rem;
  font-weight: 800;
  padding: 0.2rem 0.6rem;
  border-radius: 50px;
  background: #dbeafe;
  color: #1e40af;
}

.schedule-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: var(--text-primary, #0f172a);
  margin: 0;
}

.schedule-filter-tabs {
  display: flex;
  gap: 0.3rem;
  flex-wrap: wrap;
}

.sch-filter-btn {
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  border: 1px solid var(--border-color, #cbd5e1);
  background: var(--card-bg, #ffffff);
  font-size: 0.73rem;
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

.schedule-panel-body {
  padding: 0.6rem 1rem;
  overflow-y: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

/* Accordion Tree View Styles */
.act-group-card {
  background: var(--panel-bg, #f8fafc);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.act-group-header {
  padding: 0.5rem 0.8rem;
  background: var(--card-bg, #ffffff);
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 700;
  border-bottom: 1px solid transparent;
}
.act-group-header:hover {
  background: #f1f5f9;
}
.act-group-card.open .act-group-header {
  border-bottom-color: var(--border-color, #e2e8f0);
  background: #eff6ff;
}

.act-tree-content {
  display: none;
  padding: 0.4rem 0.6rem;
  background: var(--panel-bg, #f8fafc);
}
.act-group-card.open .act-tree-content {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.act-item-row {
  display: grid;
  grid-template-columns: 110px 240px 100px 1fr 70px 140px;
  align-items: center;
  gap: 0.6rem;
  padding: 0.4rem 0.6rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.act-item-row:hover, .act-item-row.active {
  background: #f0f9ff;
  border-color: #0284c7;
  box-shadow: 0 2px 6px rgba(2, 132, 199, 0.15);
}

.act-cat-tag {
  display: inline-block;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  font-size: 0.68rem;
  font-weight: 700;
  text-align: center;
}
.cat-subgrade { background: #ffedd5; color: #c2410c; }
.cat-track { background: #dbeafe; color: #1e40af; }
.cat-pavement { background: #dcfce7; color: #15803d; }
.cat-station { background: #f3e8ff; color: #6b21a8; }
.cat-prep { background: #f1f5f9; color: #475569; }

.act-gantt-bar-bg {
  position: relative;
  height: 12px;
  background: #e2e8f0;
  border-radius: 6px;
  overflow: hidden;
}
.act-gantt-bar-fill {
  height: 100%;
  border-radius: 6px;
  transition: width 0.3s ease;
}
"""

# Replace old CSS or insert new CSS
if '.act-group-card' not in html_text:
    html_text = re.sub(r'/\* === 09\.공정표 연동 대시보드 CSS === \*/.*?\n\*/', new_css, html_text, flags=re.DOTALL)

# Update HTML panel header with category filter buttons
new_header_html = """  <!-- 09.공정표 513개 Activity 연동 대시보드 패널 -->
  <div id="schedule-panel" class="schedule-panel-container hidden">
    <div class="schedule-panel-header">
      <div class="schedule-title-area">
        <span class="schedule-badge">513개 Activity 연동</span>
        <h3 class="schedule-title">동탄트램 Time-Chainage 세부 시공 공정표</h3>
      </div>
      <div class="schedule-filter-tabs">
        <button class="sch-filter-btn active" data-filter="all">전체 (513개)</button>

        <button class="sch-filter-btn" data-filter="노반공">노반공 (120)</button>
        <button class="sch-filter-btn" data-filter="궤도공">궤도공 (123)</button>
        <button class="sch-filter-btn" data-filter="포장공">포장공 (122)</button>
        <button class="sch-filter-btn" data-filter="정거장공">정거장공 (65)</button>
        <button class="sch-filter-btn" data-filter="준비/지장물/시험">기타/준비 (83)</button>
      </div>
      <button id="btn-close-schedule" class="schedule-close-btn">✕ 닫기</button>
    </div>
    <div class="schedule-panel-body" id="schedule-timeline-body">
      <!-- Dynamically populated 3-level tree rows -->
    </div>
  </div>"""

if '513개 Activity' not in html_text:
    html_text = re.sub(r'<div id="schedule-panel".*?</div>\n  </div>', new_header_html, html_text, flags=re.DOTALL)

# Replace JavaScript logic with 513 Activities Tree View & Map Focus
new_js_logic = f"""
// === 513개 Activity 데이터베이스 ===
const activitiesDatabase = {activities_json_str};

function initScheduleIntegration() {{
  const toggleBtn = document.getElementById("btn-toggle-schedule");
  const closeBtn = document.getElementById("btn-close-schedule");
  const panel = document.getElementById("schedule-panel");
  const filterBtns = document.querySelectorAll(".sch-filter-btn");

  if (!toggleBtn || !panel) return;

  toggleBtn.addEventListener("click", () => {{
    panel.classList.toggle("hidden");
    if (!panel.classList.contains("hidden")) {{
      renderActivityTree("all");
    }}
  }});

  if (closeBtn) {{
    closeBtn.addEventListener("click", () => {{
      panel.classList.add("hidden");
    }});
  }}

  filterBtns.forEach(btn => {{
    btn.addEventListener("click", (e) => {{
      filterBtns.forEach(b => b.classList.remove("active"));
      e.target.classList.add("active");
      const filter = e.target.getAttribute("data-filter");
      renderActivityTree(filter);
    }});
  }});
}}

function renderActivityTree(filterCategory = "all") {{
  const body = document.getElementById("schedule-timeline-body");
  if (!body) return;
  body.innerHTML = "";

  const filtered = activitiesDatabase.filter(act => {{
    if (filterCategory === "all") return true;
    return act.category === filterCategory;
  }});

  // Group by tool & masterSection
  const groups = {{}};
  filtered.forEach(act => {{
    const groupKey = `[${{act.tool}}] ${{act.masterSection || '기타/전체구간'}}`;
    if (!groups[groupKey]) groups[groupKey] = [];
    groups[groupKey].push(act);
  }});

  const totalFilteredCount = filtered.length;

  Object.keys(groups).forEach((gKey, gIdx) => {{
    const groupActs = groups[gKey];
    const groupCard = document.createElement("div");
    groupCard.setAttribute("class", `act-group-card ${{gIdx === 0 ? 'open' : ''}}`);

    const header = document.createElement("div");
    header.setAttribute("class", "act-group-header");
    header.innerHTML = `
      <span>📌 ${{gKey}} (${{groupActs.length}}개 Activity)</span>
      <span style="font-size: 0.72rem; color: var(--text-muted);">클릭하여 펼치기/접기 ▾</span>
    `;

    header.addEventListener("click", () => {{
      groupCard.classList.toggle("open");
    }});

    const content = document.createElement("div");
    content.setAttribute("class", "act-tree-content");

    groupActs.forEach(act => {{
      const row = document.createElement("div");
      row.setAttribute("class", "act-item-row");
      row.setAttribute("data-acode", act.acode);

      let catClass = "cat-prep";
      if (act.category === "노반공") catClass = "cat-subgrade";
      else if (act.category === "궤도공") catClass = "cat-track";
      else if (act.category === "포장공") catClass = "cat-pavement";
      else if (act.category === "정거장공") catClass = "cat-station";

      let fillClass = "#3b82f6";
      if (act.category === "노반공") fillClass = "#ea580c";
      else if (act.category === "포장공") fillClass = "#16a34a";
      else if (act.category === "정거장공") fillClass = "#9333ea";

      const maxEd = 400;
      const durationPct = Math.min(100, Math.max(5, (act.ed / maxEd) * 100));

      row.innerHTML = `
        <div><span class="act-cat-tag ${{catClass}}">${{act.category}}</span></div>
        <div style="font-weight: 700; color: var(--text-primary);">${{act.adesc}}</div>
        <div style="font-size: 0.7rem; color: var(--text-muted);">${{act.acode}}</div>
        <div class="act-gantt-bar-bg">
          <div class="act-gantt-bar-fill" style="width: ${{durationPct.toFixed(1)}}%; background: ${{fillClass}};"></div>
        </div>
        <div style="font-weight: 700; color: #2563eb; text-align: right;">${{act.ed}}일</div>
        <div style="font-size: 0.7rem; color: var(--text-muted); text-align: right;">${{act.es || '미정'}} ~ ${{act.ef || '미정'}}</div>
      `;

      row.addEventListener("click", (e) => {{
        e.stopPropagation();
        document.querySelectorAll(".act-item-row").forEach(r => r.classList.remove("active"));
        row.classList.add("active");
        focusActivityOnMap(act);
      }});

      content.appendChild(row);
    }});

    groupCard.appendChild(header);
    groupCard.appendChild(content);
    body.appendChild(groupCard);
  }});
}}

function focusActivityOnMap(act) {{
  // Find matching section in constructionSections
  const matchedSec = constructionSections.find(s => 
    s.tool === act.tool && (s.section.includes(act.cleanSub) || act.adesc.includes(s.section))
  );

  if (matchedSec) {{
    selectConstructionSection(matchedSec);
  }} else {{
    // Fallback search by sub-section name in stations or intersections
    const matchedStn = stationData.find(stn => act.adesc.includes(stn.name) || act.adesc.includes(String(stn.id)));
    if (matchedStn) {{
      focusCoordinates(matchedStn.x, matchedStn.y);
      showTooltipAt(matchedStn.x, matchedStn.y, `<b>[Activity] ${{act.adesc}}</b><br>· 코드: ${{act.acode}}<br>· 공기: ${{act.ed}}일 (${{act.es}} ~ ${{act.ef}})`);
    }}
  }}
}}

document.addEventListener("DOMContentLoaded", () => {{
  initScheduleIntegration();
}});
"""

# Replace JS block with new JS logic
if 'activitiesDatabase' not in html_text:
    html_text = re.sub(r'// === 09\.공정표 연동 대시보드 JS Logic ===.*?</script>', new_js_logic + '\n</script>', html_text, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_text)

print(f"✅ Successfully integrated 513 activities into V1 HTML! File size: {len(html_text)} bytes")
