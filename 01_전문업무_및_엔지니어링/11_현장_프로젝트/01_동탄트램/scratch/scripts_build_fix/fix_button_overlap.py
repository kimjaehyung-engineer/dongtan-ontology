import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove old schedule button from inside <header> if present
text = text.replace(
    """  <button id="btn-toggle-schedule" class="schedule-toggle-btn">
    📊 09.공정표 연동 대시보드
  </button>
</header>""",
    "</header>"
)
text = text.replace(
    """  <button id="btn-toggle-schedule" class="schedule-toggle-btn">
    📊 09.공정표 연동 대시보드
  </button>""",
    ""
)

# 2. Replace old .btn-open-drawer-panel CSS with floating-trigger-group CSS
old_btn_css = re.search(r'\.btn-open-drawer-panel\s*\{[^}]*?\}.*?\.btn-open-drawer-panel:hover\s*\{[^}]*?\}', text, re.DOTALL)

new_btn_css = """/* === 플로팅 우측 버튼 그룹 (간섭 방지 수직 스택) === */
.floating-trigger-group {
  position: fixed;
  top: 1.2rem;
  right: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  align-items: flex-end;
  z-index: 1150;
  pointer-events: auto;
}

.btn-open-drawer-panel, .btn-open-schedule-panel {
  position: relative;
  top: auto;
  right: auto;
  color: white;
  border: none;
  padding: 0.55rem 1.1rem;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 700;
  font-family: 'Noto Sans KR', sans-serif;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.45rem;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn-open-drawer-panel {
  background: linear-gradient(135deg, #f97316, #ea580c);
  box-shadow: 0 4px 15px rgba(234, 88, 12, 0.35);
}
.btn-open-drawer-panel:hover {
  background: linear-gradient(135deg, #ea580c, #c2410c);
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(234, 88, 12, 0.45);
}

.btn-open-schedule-panel {
  background: linear-gradient(135deg, #0284c7, #2563eb);
  box-shadow: 0 4px 15px rgba(37, 99, 235, 0.35);
}
.btn-open-schedule-panel:hover {
  background: linear-gradient(135deg, #0369a1, #1d4ed8);
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.45);
}"""

if old_btn_css:
    text = text.replace(old_btn_css.group(0), new_btn_css, 1)
    print("✓ Updated button CSS to floating group")

# 3. Replace single trigger button with floating group container HTML
old_btn_html = re.search(r'<!-- Floating Trigger Button -->.*?<button class="btn-open-drawer-panel".*?</button>', text, re.DOTALL)

new_btn_html = """<!-- Floating Trigger Buttons Group (간섭 없는 수직 배치) -->
<div class="floating-trigger-group">
  <button class="btn-open-drawer-panel" onclick="openIntersectionDrawer()">
    <span>🚧</span>
    <span>교차로 대시보드 목록</span>
  </button>
  <button id="btn-toggle-schedule" class="btn-open-schedule-panel">
    <span>📊</span>
    <span>09.공정표 연동 대시보드</span>
  </button>
</div>"""

if old_btn_html:
    text = text.replace(old_btn_html.group(0), new_btn_html, 1)
    print("✓ Updated floating button HTML container")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied button separation fix successfully!")
