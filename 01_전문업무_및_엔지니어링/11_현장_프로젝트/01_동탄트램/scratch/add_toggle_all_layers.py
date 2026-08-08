import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add CSS for btn-layer-all
css_to_add = """
.layer-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.6rem;
  font-weight: 700;
  color: var(--text-primary);
}
.btn-layer-all {
  background: transparent;
  border: 1px solid var(--border-color, #cbd5e1);
  border-radius: 4px;
  padding: 2px 7px;
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--text-secondary, #475569);
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-layer-all:hover {
  background: var(--border-color, #cbd5e1);
  color: var(--text-primary, #0f172a);
}
"""

style_end_idx = text.find('</style>')
if style_end_idx != -1:
    text = text[:style_end_idx] + css_to_add + text[style_end_idx:]
    print("✓ Added CSS for .btn-layer-all")

# 2. Update HTML header in layer-panel
old_title_html = '<div class="layer-title">도면 레이어</div>'
new_title_html = '''<div class="layer-title">
      <span>도면 레이어</span>
      <button id="btn-toggle-all-layers" class="btn-layer-all" type="button">전체 해제</button>
    </div>'''

if old_title_html in text:
    text = text.replace(old_title_html, new_title_html, 1)
    print("✓ Updated layer-title HTML with '전체 해제' button")
else:
    print("!! Could not find old_title_html")

# 3. Add JS logic for btn-toggle-all-layers
js_toggle_all_code = """
// --- 전체 레이어 토글(전체 선택 / 전체 해제) 기능 ---
const layerMappings = [
  { checkboxId: "toggle-bg", targetId: "bg-map" },
  { checkboxId: "toggle-routes", targetId: "routes-group" },
  { checkboxId: "toggle-nodes", targetId: "nodes-group" },
  { checkboxId: "toggle-labels", targetId: "labels-group" },
  { checkboxId: "toggle-distances", targetId: "distances-group" },
  { checkboxId: "toggle-turnouts", targetId: "turnouts-group" },
  { checkboxId: "toggle-intersections-lines", targetId: "intersections-lines-group" },
  { checkboxId: "toggle-intersections-labels", targetId: "intersections-labels-group" },
  { checkboxId: "toggle-construction-sections", targetId: "construction-sections-group" }
];

const btnToggleAll = document.getElementById("btn-toggle-all-layers");
if (btnToggleAll) {
  btnToggleAll.addEventListener("click", () => {
    const checkboxes = layerMappings.map(m => document.getElementById(m.checkboxId)).filter(Boolean);
    const anyChecked = checkboxes.some(cb => cb.checked);
    const targetState = !anyChecked;
    
    layerMappings.forEach(m => {
      const cb = document.getElementById(m.checkboxId);
      const target = document.getElementById(m.targetId);
      if (cb) cb.checked = targetState;
      if (target) target.style.display = targetState ? "block" : "none";
    });
    
    btnToggleAll.textContent = targetState ? "전체 해제" : "전체 선택";
  });

  function syncToggleAllButtonText() {
    const checkboxes = layerMappings.map(m => document.getElementById(m.checkboxId)).filter(Boolean);
    const anyChecked = checkboxes.some(cb => cb.checked);
    btnToggleAll.textContent = anyChecked ? "전체 해제" : "전체 선택";
  }

  layerMappings.forEach(m => {
    const cb = document.getElementById(m.checkboxId);
    if (cb) cb.addEventListener("change", syncToggleAllButtonText);
  });
}
"""

# Insert JS before DOMContentLoaded
dom_marker = 'document.addEventListener("DOMContentLoaded", () => {'
dom_pos = text.find(dom_marker)
if dom_pos != -1:
    text = text[:dom_pos] + js_toggle_all_code + '\n\n' + text[dom_pos:]
    print("✓ Added JS toggle all layers logic")
else:
    print("!! Could not find DOMContentLoaded marker")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("✅ Layer toggle all feature applied successfully!")
