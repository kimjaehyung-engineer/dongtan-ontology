import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Print renderDrawerList
pattern = r'function renderDrawerList\(\)\s*\{(.*?)\n\}'
match = re.search(pattern, text, re.DOTALL)
if match:
    print("Found renderDrawerList block length:", len(match.group(0)))
    print("Full block:\n", match.group(0))

    new_renderDrawerList = """function renderDrawerList() {
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
    const idKey = `${item.tool}_${item.no}`;
    const isChecked = checkedIntersections.has(idKey);
    const card = document.createElement("div");
    card.className = `drawer-item-card${isChecked ? '' : ' unchecked'}`;
    card.setAttribute("data-id", idKey);

    const is1 = item.tool === "1공구";
    card.innerHTML = `
      <div style="display: flex; align-items: center; gap: 0.75rem;">
        <input type="checkbox" class="drawer-card-checkbox" data-id="${idKey}" ${isChecked ? 'checked' : ''} style="width: 18px; height: 18px; cursor: pointer; accent-color: ${is1 ? '#ea580c' : '#2563eb'}; flex-shrink: 0;" />
        <div>
          <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600;">[${item.tool} #${item.no}] ${item.code}</div>
          <div style="font-size: 0.9rem; font-weight: 700; margin-top: 0.1rem; color: var(--text-primary);">${item.name}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem;">STA ${item.startSta}~${item.endSta}m (${item.length}m)</div>
        </div>
      </div>
      <div style="text-align: right; min-width: 90px;">
        <div style="font-size: 0.68rem; color: var(--text-muted); font-weight: 600;">구간연장</div>
        <div style="font-size: 1.15rem; font-weight: 800; color: ${is1 ? '#ea580c' : '#2563eb'};">${item.length}m</div>
        <div style="font-size: 0.7rem; color: var(--text-muted);">${item.stage}단계 (${item.method})</div>
      </div>
    `;

    const chk = card.querySelector(".drawer-card-checkbox");
    if (chk) {
      chk.addEventListener("click", (e) => {
        e.stopPropagation();
      });
      chk.addEventListener("change", (e) => {
        e.stopPropagation();
        toggleIntersectionVisibility(item.tool, item.no, e.target.checked);
      });
    }

    card.addEventListener("click", () => {
      selectIntersection(item);
      openIntersectionModal(item);
    });

    drawerList.appendChild(card);
  });

  updateCheckAllState();
}"""

    text = text.replace(match.group(0), new_renderDrawerList, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced renderDrawerList successfully!")
