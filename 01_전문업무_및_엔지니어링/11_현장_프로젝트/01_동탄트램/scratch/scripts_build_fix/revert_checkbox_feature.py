import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove added CSS
text = re.sub(r'\.drawer-item-card\.unchecked\s*\{[^}]*\}\s*body\.dark-theme \.drawer-item-card\.unchecked\s*\{[^}]*\}\s*', '', text)

# 2. Remove added functions (checkedIntersections, toggleIntersectionVisibility, toggleAllIntersections, updateCheckAllState)
text = re.sub(r'const checkedIntersections = new Set\(\);.*?(?=function renderIntersections\(\))', '', text, flags=re.DOTALL)

# 3. Restore renderIntersections to original
ri_modified = """const idKey = `${item.tool}_${item.no}`;
      gLine.style.display = checkedIntersections.has(idKey) ? "inline" : "none";
      linesGroup.appendChild(gLine);"""
text = text.replace(ri_modified, "linesGroup.appendChild(gLine);")

lbl_modified = """const idKey = `${item.tool}_${item.no}`;
      gLabel.style.display = checkedIntersections.has(idKey) ? "inline" : "none";
      labelsGroup.appendChild(gLabel);"""
text = text.replace(lbl_modified, "labelsGroup.appendChild(gLabel);")

# Remove any leftover checkedIntersections in renderIntersections
text = text.replace("""  if (checkedIntersections.size === 0) {
    intersectionData.forEach(item => checkedIntersections.add(`${item.tool}_${item.no}`));
  }""", "")

# 4. Restore original renderDrawerList()
original_renderDrawerList = """function renderDrawerList() {
  const drawerList = document.getElementById("drawer-list");
  const searchInput = document.getElementById("drawer-search");
  if (!drawerList) return;

  const query = searchInput ? searchInput.value.trim().toLowerCase() : "";

  const filtered = intersectionData.filter(item => {
    const matchesTool = currentFilterTool === "all" || item.tool === currentFilterTool;
    const matchesQuery = !query || item.name.toLowerCase().includes(query) || String(item.no).includes(query) || item.code.toLowerCase().includes(query);
    return matchesTool && matchesQuery;
  });

  drawerList.innerHTML = "";
  filtered.forEach(item => {
    const card = document.createElement("div");
    card.className = "drawer-item-card";
    card.setAttribute("data-id", `${item.tool}_${item.no}`);

    const is1 = item.tool === "1공구";
    card.innerHTML = `
      <div>
        <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600;">[${item.tool} #${item.no}] ${item.code}</div>
        <div style="font-size: 0.9rem; font-weight: 700; margin-top: 0.1rem; color: var(--text-primary);">${item.name}</div>
        <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem;">STA ${item.startSta}~${item.endSta}m (${item.length}m)</div>
      </div>
      <div style="text-align: right; min-width: 90px;">
        <div style="font-size: 0.68rem; color: var(--text-muted); font-weight: 600;">구간연장</div>
        <div style="font-size: 1.15rem; font-weight: 800; color: ${is1 ? '#ea580c' : '#2563eb'};">${item.length}m</div>
        <div style="font-size: 0.7rem; color: var(--text-muted);">${item.stage}단계 (${item.method})</div>
      </div>
    `;

    card.addEventListener("click", () => {
      selectIntersection(item);
      openIntersectionModal(item);
    });

    drawerList.appendChild(card);
  });
}"""

match_rdl = re.search(r'function renderDrawerList\(\)\s*\{(.*?)\n\}', text, re.DOTALL)
if match_rdl:
    text = text.replace(match_rdl.group(0), original_renderDrawerList, 1)

# 5. Restore original drawer-controls HTML
dc_modified = """<div class="drawer-controls">
      <div style="display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; margin-bottom: 0.4rem;">
        <input type="text" id="drawer-search" placeholder="교차로명 또는 번호 검색..." oninput="filterDrawerList()" style="flex: 1; margin-bottom: 0;" />
        <label style="display: flex; align-items: center; gap: 0.35rem; font-size: 0.78rem; font-weight: 600; color: var(--text-primary); cursor: pointer; user-select: none; white-space: nowrap; padding: 0.4rem 0.6rem; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 8px;">
          <input type="checkbox" id="drawer-check-all" checked onchange="toggleAllIntersections(this.checked)" style="width: 15px; height: 15px; cursor: pointer; accent-color: #2563eb;" />
          <span>전체 선택</span>
        </label>
      </div>
      <div class="drawer-filter-group">"""

dc_original = """<div class="drawer-controls">
      <input type="text" id="drawer-search" placeholder="교차로명 또는 번호 검색..." oninput="filterDrawerList()" />
      <div class="drawer-filter-group">"""

text = text.replace(dc_modified, dc_original)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Reverted checkbox feature completely!")
