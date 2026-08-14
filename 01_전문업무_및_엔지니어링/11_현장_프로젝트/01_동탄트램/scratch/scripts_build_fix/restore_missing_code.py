import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# ========== STEP 1: Restore :root to original dark theme ==========
# The :root was changed to light defaults. Restore original dark :root
old_root_light = """:root {
  --bg-color: #f8fafc;
  --panel-bg: #ffffff;
  --card-bg: #ffffff;
  --text-primary: #0f172a;
  --text-secondary: #334155;
  --text-muted: #64748b;
  --border-color: #cbd5e1;
  --blue-glow: 0 0 15px rgba(29, 111, 232, 0.6);
  --red-glow: 0 0 15px rgba(224, 49, 49, 0.6);
  --blue: #1d6fe8;
  --red: #e03131;
  --glass-bg: rgba(255, 255, 255, 0.85);
  --header-bg: linear-gradient(135deg, #ffffff, #f1f5f9);"""

new_root_dark = """:root {
  --bg-color: #0f172a;
  --panel-bg: #1e293b;
  --card-bg: #1e293b;
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
  --border-color: #334155;
  --blue-glow: 0 0 15px rgba(29, 111, 232, 0.6);
  --red-glow: 0 0 15px rgba(224, 49, 49, 0.6);
  --blue: #1d6fe8;
  --red: #e03131;
  --glass-bg: rgba(30, 41, 59, 0.85);
  --header-bg: linear-gradient(135deg, #1e293b, #0f172a);"""

if old_root_light in text:
    text = text.replace(old_root_light, new_root_dark, 1)
    print("✓ Restored :root to original dark theme")

# ========== STEP 2: Restore .light-theme CSS override ==========
# The .dark-theme was used instead. Replace with original .light-theme
old_dark_class = """.dark-theme {
  --bg-color: #0f172a;
  --panel-bg: #1e293b;
  --card-bg: #1e293b;
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
  --border-color: #334155;
  --glass-bg: rgba(30, 41, 59, 0.85);
  --header-bg: linear-gradient(135deg, #1e293b, #0f172a);
}"""

new_light_class = """.light-theme {
  --bg-color: #f8fafc;
  --panel-bg: #ffffff;
  --card-bg: #ffffff;
  --text-primary: #0f172a;
  --text-secondary: #334155;
  --text-muted: #64748b;
  --border-color: #cbd5e1;
  --glass-bg: rgba(255, 255, 255, 0.85);
  --header-bg: linear-gradient(135deg, #ffffff, #f1f5f9);
}"""

if old_dark_class in text:
    text = text.replace(old_dark_class, new_light_class, 1)
    print("✓ Restored .light-theme CSS override")

# ========== STEP 3: Restore body.dark-theme back to body:not(.light-theme) ==========
text = text.replace('body.dark-theme', 'body:not(.light-theme)')
print("✓ Restored body:not(.light-theme) selectors")

# ========== STEP 4: Fill the empty DOMContentLoaded with proper init code ==========
empty_dom = 'document.addEventListener("DOMContentLoaded", () => {\n});'
full_dom = '''document.addEventListener("DOMContentLoaded", () => {
  // Load saved coordinates from localStorage if any
  const savedCoords = localStorage.getItem("dongtan_tram_map_coords_v1");
  if (savedCoords) {
    try {
      const parsed = JSON.parse(savedCoords);
      for (const [id, pt] of Object.entries(parsed)) {
        if (nodes[id]) {
          nodes[id].x = pt.x;
          nodes[id].y = pt.y;
        }
      }
    } catch (e) {
      console.error("Error parsing saved coordinates:", e);
    }
  }

  drawPaths();
  drawDistances();
  drawTurnouts();
  renderIntersections();
  renderConstructionSections();
  renderInteractiveElements();
  
  // Theme load
  if (localStorage.getItem("v1-theme") === "light") {
    document.body.classList.add("light-theme");
    btnTheme.textContent = "☀️";
  }
  
  // Font load
  applyFontSize(localStorage.getItem("v1-font") || "medium");
});'''

if empty_dom in text:
    text = text.replace(empty_dom, full_dom, 1)
    print("✓ Restored DOMContentLoaded init code")
else:
    print("!! empty DOMContentLoaded not found for replacement")

# ========== STEP 5: Insert missing code before DOMContentLoaded ==========
# We need to add: layer toggles, theme toggle, font size, section-quick-nav, 
# intersection modal, route path events, second DOMContentLoaded

missing_code = '''

// Layers toggling
document.getElementById("toggle-bg").addEventListener("change", (e) => {
  document.getElementById("bg-map").style.display = e.target.checked ? "block" : "none";
});
document.getElementById("toggle-routes").addEventListener("change", (e) => {
  document.getElementById("routes-group").style.display = e.target.checked ? "block" : "none";
});
document.getElementById("toggle-nodes").addEventListener("change", (e) => {
  document.getElementById("nodes-group").style.display = e.target.checked ? "block" : "none";
});
document.getElementById("toggle-labels").addEventListener("change", (e) => {
  document.getElementById("labels-group").style.display = e.target.checked ? "block" : "none";
});
document.getElementById("toggle-distances").addEventListener("change", (e) => {
  document.getElementById("distances-group").style.display = e.target.checked ? "block" : "none";
});
document.getElementById("toggle-turnouts").addEventListener("change", (e) => {
  document.getElementById("turnouts-group").style.display = e.target.checked ? "block" : "none";
});
document.getElementById("toggle-intersections-lines").addEventListener("change", (e) => {
  const g = document.getElementById("intersections-lines-group");
  if (g) g.style.display = e.target.checked ? "block" : "none";
});
document.getElementById("toggle-intersections-labels").addEventListener("change", (e) => {
  const g = document.getElementById("intersections-labels-group");
  if (g) g.style.display = e.target.checked ? "block" : "none";
});
document.getElementById("toggle-construction-sections").addEventListener("change", (e) => {
  const g = document.getElementById("construction-sections-group");
  if (g) g.style.display = e.target.checked ? "block" : "none";
});

// Theme toggle
const btnTheme = document.getElementById("btn-theme");
btnTheme.addEventListener("click", () => {
  document.body.classList.toggle("light-theme");
  btnTheme.textContent = document.body.classList.contains("light-theme") ? "☀️" : "🌙";
  localStorage.setItem("v1-theme", document.body.classList.contains("light-theme") ? "light" : "dark");
});

// Font size sizing
function applyFontSize(size) {
  document.body.classList.remove("fs-small", "fs-medium", "fs-large");
  if (size === "small") {
    document.body.style.fontSize = "0.85rem";
    document.getElementById("btn-fs-small").style.background = "var(--border-color)";
    document.getElementById("btn-fs-medium").style.background = "";
    document.getElementById("btn-fs-large").style.background = "";
  } else if (size === "large") {
    document.body.style.fontSize = "1.15rem";
    document.getElementById("btn-fs-large").style.background = "var(--border-color)";
    document.getElementById("btn-fs-small").style.background = "";
    document.getElementById("btn-fs-medium").style.background = "";
  } else {
    document.body.style.fontSize = "1rem";
    document.getElementById("btn-fs-medium").style.background = "var(--border-color)";
    document.getElementById("btn-fs-small").style.background = "";
    document.getElementById("btn-fs-large").style.background = "";
  }
  localStorage.setItem("v1-font", size);
}
document.getElementById("btn-fs-small").addEventListener("click", () => applyFontSize("small"));
document.getElementById("btn-fs-medium").addEventListener("click", () => applyFontSize("medium"));
document.getElementById("btn-fs-large").addEventListener("click", () => applyFontSize("large"));

// --- Route path hover tooltip events ---
function bindRoutePathEvents() {
  const routePaths = document.querySelectorAll("#routes-group path");
  routePaths.forEach(p => {
    p.addEventListener("mouseenter", (e) => {
      const name = p.getAttribute("data-name") || "";
      if (name) showTooltipAt(e.offsetX, e.offsetY, name);
    });
    p.addEventListener("mouseleave", hideTooltip);
  });
}

window.addEventListener("DOMContentLoaded", () => {
  bindRoutePathEvents();
});

// --- 교차로 상세 확대 도면 팝업 모달 JS ---
function openIntersectionModal(item) {
  const modal = document.getElementById("intersection-zoom-modal");
  if (!modal) return;

  const is1 = item.tool === "1공구";
  const badgeEl = document.getElementById("modal-badge-tool");
  if (badgeEl) {
    badgeEl.textContent = item.tool;
    badgeEl.className = "badge-tool " + (is1 ? "badge-1" : "badge-2");
  }

  const titleEl = document.getElementById("modal-title");
  if (titleEl) titleEl.textContent = item.name;

  const metaEl = document.getElementById("modal-meta");
  if (metaEl) {
    metaEl.innerHTML = `
      <span>📍 ${item.startSta || ""} ~ ${item.endSta || ""}</span>
      <span>📏 구간연장: ${item.extension || ""}m</span>
      <span>⏱️ 공기: ${item.duration || ""}일</span>
    `;
  }

  modal.classList.add("active");
}

function closeIntersectionModal() {
  const modal = document.getElementById("intersection-zoom-modal");
  if (modal) modal.classList.remove("active");
}

'''

# Insert this code BEFORE the DOMContentLoaded block
dom_marker = 'document.addEventListener("DOMContentLoaded", () => {'
dom_idx = text.find(dom_marker)
if dom_idx != -1:
    text = text[:dom_idx] + missing_code + '\n' + text[dom_idx:]
    print("✓ Inserted layer toggles, theme, font, modal code")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"\n✅ Full restoration complete! File size: {len(text)} bytes")
