# -*- coding: utf-8 -*-
import re

server_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# 1. Add CSS for tree view
tree_css = '''
    /* Document Folder Tree View Styles */
    .doc-tree-container {
      display: flex;
      flex-direction: column;
      gap: 6px;
      max-height: 480px;
      overflow-y: auto;
      padding-right: 2px;
    }
    .tree-folder {
      border: 1px solid var(--border-color, #e2e8f0);
      background: var(--bg-card, #ffffff);
      border-radius: 8px;
      overflow: hidden;
      transition: all 0.2s ease;
    }
    .tree-folder.open {
      border-color: #93c5fd;
      box-shadow: 0 2px 8px rgba(37, 99, 235, 0.06);
    }
    .folder-header {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 8px 10px;
      background: var(--bg-hover, #f8fafc);
      cursor: pointer;
      user-select: none;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-color, #1e293b);
      transition: background 0.15s;
    }
    .folder-header:hover {
      background: #eff6ff;
      color: #1d4ed8;
    }
    .folder-icon {
      font-size: 14px;
      flex-shrink: 0;
    }
    .folder-title {
      flex: 1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .folder-badge {
      font-size: 10px;
      font-weight: 600;
      padding: 1px 6px;
      border-radius: 10px;
      background: #e2e8f0;
      color: #475569;
    }
    .tree-folder.open .folder-badge {
      background: #dbeafe;
      color: #1e40af;
    }
    .folder-arrow {
      font-size: 10px;
      color: var(--text-muted, #94a3b8);
      transition: transform 0.2s ease;
    }
    .tree-folder.open .folder-arrow {
      transform: rotate(90deg);
      color: #2563eb;
    }
    .folder-content {
      display: none;
      padding: 4px 6px 6px 6px;
      background: var(--bg-card, #ffffff);
      flex-direction: column;
      gap: 4px;
    }
    .tree-folder.open .folder-content {
      display: flex;
    }
    .tree-subfolder {
      margin-left: 6px;
      border-left: 2px solid #e2e8f0;
      padding-left: 6px;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }
    .subfolder-header {
      display: flex;
      align-items: center;
      gap: 5px;
      padding: 4px 6px;
      font-size: 11px;
      font-weight: 600;
      color: var(--text-muted, #64748b);
      cursor: pointer;
      border-radius: 4px;
    }
    .subfolder-header:hover {
      background: #f1f5f9;
      color: #0f172a;
    }
    .tree-doc-item {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 6px 8px;
      border-radius: 6px;
      border: 1px solid #f1f5f9;
      background: var(--bg-card, #ffffff);
      font-size: 12px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .tree-doc-item:hover {
      background: #f0fdf4;
      border-color: #86efac;
      transform: translateX(2px);
    }
    .tree-doc-item.active {
      background: #eff6ff;
      border-color: #3b82f6;
      font-weight: 600;
    }
    .tree-doc-icon {
      font-size: 13px;
      flex-shrink: 0;
    }
    .tree-doc-info {
      flex: 1;
      min-width: 0;
    }
    .tree-doc-name {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      color: var(--text-color, #1e293b);
      line-height: 1.3;
      font-weight: 500;
    }
    .tree-doc-meta {
      font-size: 10px;
      color: var(--text-muted, #94a3b8);
    }
    .tree-doc-actions {
      display: flex;
      gap: 3px;
      align-items: center;
      flex-shrink: 0;
    }
    .tree-btn-view {
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      background: #eff6ff;
      color: #2563eb;
      border: 1px solid #bfdbfe;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.15s;
    }
    .tree-btn-view:hover {
      background: #2563eb;
      color: #ffffff;
    }
    .tree-btn-del {
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      background: #fff1f2;
      color: #e11d48;
      border: 1px solid #fecdd3;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.15s;
    }
    .tree-btn-del:hover {
      background: #e11d48;
      color: #ffffff;
    }
'''

if "/* Document Folder Tree View Styles */" not in code:
    code = code.replace("    .doc-list {", tree_css + "\n    .doc-list {")
    print("Tree view CSS added!")

# 2. Add View Switcher above #docList in HTML
old_markup = '''          <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 8px; line-height: 1.4;">
            문서 목록을 클릭하면 우측 뷰어에 즉시 열람되며, 질문시에는 AI가 아래 모든 문서를 실시간 교차 탐색합니다.
          </div>
          <div id="docList" class="doc-list">'''

new_markup = '''          <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 8px; line-height: 1.4;">
            문서를 클릭하면 우측 뷰어에 즉시 열람되며, 질문 시 AI가 전 분야를 실시간 교차 탐색합니다.
          </div>
          <!-- 2-Way Tree Switcher (공구별 ↔ 분야별) -->
          <div class="tree-switcher" style="display: flex; gap: 4px; background: var(--bg-hover, #f1f5f9); padding: 3px; border-radius: 8px; margin-bottom: 8px; border: 1px solid var(--border-color, #e2e8f0);">
            <button id="btnViewZone" onclick="setDocTreeView('zone')" style="flex: 1; font-size: 11px; padding: 5px 6px; border-radius: 6px; border: none; font-weight: 600; cursor: pointer; background: #2563eb; color: #ffffff; transition: all 0.15s; display: flex; align-items: center; justify-content: center; gap: 3px;">
              <span>📍 공구·총괄별</span>
            </button>
            <button id="btnViewField" onclick="setDocTreeView('field')" style="flex: 1; font-size: 11px; padding: 5px 6px; border-radius: 6px; border: none; font-weight: 500; cursor: pointer; background: transparent; color: var(--text-muted, #64748b); transition: all 0.15s; display: flex; align-items: center; justify-content: center; gap: 3px;">
              <span>📐 분야(공종)별</span>
            </button>
          </div>
          <div id="docList" class="doc-tree-container">'''

if old_markup in code:
    code = code.replace(old_markup, new_markup)
    print("Tree switcher markup added!")
else:
    # Try with class="doc-list"
    code = code.replace(
        '<div id="docList" class="doc-list">',
        '''<!-- 2-Way Tree Switcher (공구별 ↔ 분야별) -->
          <div class="tree-switcher" style="display: flex; gap: 4px; background: var(--bg-hover, #f1f5f9); padding: 3px; border-radius: 8px; margin-bottom: 8px; border: 1px solid var(--border-color, #e2e8f0);">
            <button id="btnViewZone" onclick="setDocTreeView('zone')" style="flex: 1; font-size: 11px; padding: 5px 6px; border-radius: 6px; border: none; font-weight: 600; cursor: pointer; background: #2563eb; color: #ffffff; transition: all 0.15s; display: flex; align-items: center; justify-content: center; gap: 3px;">
              <span>📍 공구·총괄별</span>
            </button>
            <button id="btnViewField" onclick="setDocTreeView('field')" style="flex: 1; font-size: 11px; padding: 5px 6px; border-radius: 6px; border: none; font-weight: 500; cursor: pointer; background: transparent; color: var(--text-muted, #64748b); transition: all 0.15s; display: flex; align-items: center; justify-content: center; gap: 3px;">
              <span>📐 분야(공종)별</span>
            </button>
          </div>
          <div id="docList" class="doc-tree-container">'''
    )
    print("Replaced docList with doc-tree-container!")

# 3. Replace fetchDocs and implement Tree View logic in JS
tree_js = '''
  let currentDocTreeViewMode = 'zone'; // 'zone' or 'field'
  window.cachedDocs = [];
  let currentViewingDoc = null;

  function setDocTreeView(mode) {
    currentDocTreeViewMode = mode;
    const btnZone = document.getElementById('btnViewZone');
    const btnField = document.getElementById('btnViewField');
    if (btnZone && btnField) {
      if (mode === 'zone') {
        btnZone.style.background = '#2563eb';
        btnZone.style.color = '#ffffff';
        btnZone.style.fontWeight = '600';
        btnField.style.background = 'transparent';
        btnField.style.color = 'var(--text-muted, #64748b)';
        btnField.style.fontWeight = '500';
      } else {
        btnField.style.background = '#2563eb';
        btnField.style.color = '#ffffff';
        btnField.style.fontWeight = '600';
        btnZone.style.background = 'transparent';
        btnZone.style.color = 'var(--text-muted, #64748b)';
        btnZone.style.fontWeight = '500';
      }
    }
    renderDocTree();
  }

  function classifyDoc(docName) {
    let zone = '05. 기타 및 일반';
    let field = '기타 · 일반';

    // Zone
    if (docName.includes('1공구') || docName.startsWith('NH')) {
      zone = '01. 1공구 본선';
    } else if (docName.includes('2공구') || docName.startsWith('DT')) {
      zone = '02. 2공구 본선';
    } else if (docName.includes('차량기지') || docName.startsWith('GB') || docName.startsWith('NGB')) {
      zone = '03. 차량기지';
    } else if (docName.includes('제안') || docName.includes('증빙') || docName.includes('#3편')) {
      zone = '04. 기술제안 및 특화';
    } else if (docName.includes('입찰') || docName.includes('안내서') || docName.includes('과업') || docName.includes('공정표') || docName.includes('총괄')) {
      zone = '00. 총괄 및 입찰·계약';
    }

    // Field
    if (docName.includes('토질') || docName.includes('지반') || docName.includes('시추') || docName.includes('기초') || docName.includes('비탈면') || docName.includes('가시설') || docName.includes('사면')) {
      field = '토목 · 지반';
    } else if (docName.includes('궤도') || docName.includes('분기기') || docName.includes('레일')) {
      field = '궤도 · 철도';
    } else if (docName.includes('건축') || docName.includes('정거장') || docName.includes('환승') || docName.includes('검수고') || docName.includes('관리동')) {
      field = '건축 · 정거장';
    } else if (docName.includes('신호') || docName.includes('전기') || docName.includes('통신') || docName.includes('전차선') || docName.includes('시스템')) {
      field = '시스템 (신호/전기/통신)';
    } else if (docName.includes('입찰') || docName.includes('계약') || docName.includes('총괄')) {
      field = '총괄 · 계약';
    }

    return { zone, field };
  }

  async function fetchDocs() {
    try {
      const res = await fetch('/api/documents');
      const docs = await res.json();
      window.cachedDocs = docs;
      renderDocTree();
    } catch(e) {
      console.error(e);
    }
  }

  function renderDocTree() {
    const listEl = document.getElementById('docList');
    if (!listEl) return;
    listEl.innerHTML = '';
    const docs = window.cachedDocs || [];

    const badge = document.getElementById('docCountBadge');
    if (badge) {
      badge.innerText = `총 ${docs.length}권 탑재`;
    }

    if (docs.length === 0) {
      listEl.innerHTML = '<div style="font-size:12px; color:var(--text-muted); padding:8px;">등록된 문서가 없습니다.</div>';
      return;
    }

    if (currentDocTreeViewMode === 'zone') {
      // 1. 공구별 트리
      const zoneOrder = [
        '00. 총괄 및 입찰·계약',
        '01. 1공구 본선',
        '02. 2공구 본선',
        '03. 차량기지',
        '04. 기술제안 및 특화',
        '05. 기타 및 일반'
      ];

      const tree = {};
      zoneOrder.forEach(z => { tree[z] = {}; });

      docs.forEach(doc => {
        const { zone, field } = classifyDoc(doc.name);
        if (!tree[zone]) tree[zone] = {};
        if (!tree[zone][field]) tree[zone][field] = [];
        tree[zone][field].push(doc);
      });

      zoneOrder.forEach(zoneName => {
        const fields = tree[zoneName] || {};
        let zoneDocCount = 0;
        Object.values(fields).forEach(arr => { zoneDocCount += arr.length; });

        // Skip empty folders if 0 documents (except if total docs is small, show populated ones)
        if (zoneDocCount === 0 && zoneName === '05. 기타 및 일반') return;

        const folderEl = document.createElement('div');
        folderEl.className = 'tree-folder' + (zoneDocCount > 0 ? ' open' : '');

        folderEl.innerHTML = `
          <div class="folder-header" onclick="this.parentElement.classList.toggle('open')">
            <span class="folder-arrow">▶</span>
            <span class="folder-icon">📁</span>
            <span class="folder-title" title="${zoneName}">${zoneName}</span>
            <span class="folder-badge">${zoneDocCount}</span>
          </div>
          <div class="folder-content"></div>
        `;

        const contentEl = folderEl.querySelector('.folder-content');

        if (zoneDocCount === 0) {
          contentEl.innerHTML = '<div style="font-size:11px; color:var(--text-muted); padding:4px 8px;">문서 없음</div>';
        } else {
          Object.keys(fields).forEach(fieldName => {
            const docList = fields[fieldName];
            if (!docList || docList.length === 0) return;

            const subEl = document.createElement('div');
            subEl.className = 'tree-subfolder';
            subEl.innerHTML = `
              <div class="subfolder-header" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display==='none'?'flex':'none'">
                <span>📂</span>
                <span style="flex:1;">${fieldName}</span>
                <span style="font-size:10px; opacity:0.7;">(${docList.length})</span>
              </div>
              <div class="subfolder-items" style="display:flex; flex-direction:column; gap:3px;"></div>
            `;

            const itemsContainer = subEl.querySelector('.subfolder-items');
            docList.forEach(doc => {
              itemsContainer.appendChild(createDocItemEl(doc));
            });
            contentEl.appendChild(subEl);
          });
        }
        listEl.appendChild(folderEl);
      });

    } else {
      // 2. 분야별 트리
      const fieldOrder = [
        '총괄 · 계약',
        '토목 · 지반',
        '궤도 · 철도',
        '건축 · 정거장',
        '시스템 (신호/전기/통신)',
        '기타 · 일반'
      ];

      const tree = {};
      fieldOrder.forEach(f => { tree[f] = {}; });

      docs.forEach(doc => {
        const { zone, field } = classifyDoc(doc.name);
        if (!tree[field]) tree[field] = {};
        if (!tree[field][zone]) tree[field][zone] = [];
        tree[field][zone].push(doc);
      });

      fieldOrder.forEach(fieldName => {
        const zones = tree[fieldName] || {};
        let fieldDocCount = 0;
        Object.values(zones).forEach(arr => { fieldDocCount += arr.length; });

        if (fieldDocCount === 0 && fieldName === '기타 · 일반') return;

        const folderEl = document.createElement('div');
        folderEl.className = 'tree-folder' + (fieldDocCount > 0 ? ' open' : '');

        folderEl.innerHTML = `
          <div class="folder-header" onclick="this.parentElement.classList.toggle('open')">
            <span class="folder-arrow">▶</span>
            <span class="folder-icon">📂</span>
            <span class="folder-title" title="${fieldName}">${fieldName}</span>
            <span class="folder-badge">${fieldDocCount}</span>
          </div>
          <div class="folder-content"></div>
        `;

        const contentEl = folderEl.querySelector('.folder-content');

        if (fieldDocCount === 0) {
          contentEl.innerHTML = '<div style="font-size:11px; color:var(--text-muted); padding:4px 8px;">문서 없음</div>';
        } else {
          Object.keys(zones).forEach(zoneName => {
            const docList = zones[zoneName];
            if (!docList || docList.length === 0) return;

            const subEl = document.createElement('div');
            subEl.className = 'tree-subfolder';
            subEl.innerHTML = `
              <div class="subfolder-header" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display==='none'?'flex':'none'">
                <span>📍</span>
                <span style="flex:1;">${zoneName}</span>
                <span style="font-size:10px; opacity:0.7;">(${docList.length})</span>
              </div>
              <div class="subfolder-items" style="display:flex; flex-direction:column; gap:3px;"></div>
            `;

            const itemsContainer = subEl.querySelector('.subfolder-items');
            docList.forEach(doc => {
              itemsContainer.appendChild(createDocItemEl(doc));
            });
            contentEl.appendChild(subEl);
          });
        }
        listEl.appendChild(folderEl);
      });
    }
  }

  function createDocItemEl(doc) {
    const item = document.createElement('div');
    item.className = 'tree-doc-item' + (currentViewingDoc === doc.name ? ' active' : '');
    item.onclick = (e) => {
      e.stopPropagation();
      viewDoc(doc.name);
      document.querySelectorAll('.tree-doc-item').forEach(el => el.classList.remove('active'));
      item.classList.add('active');
    };

    item.innerHTML = `
      <span class="tree-doc-icon">📄</span>
      <div class="tree-doc-info">
        <div class="tree-doc-name" title="${doc.name}">${doc.name}</div>
        <div class="tree-doc-meta">${doc.size_mb} MB${doc.total_pages ? ' · ' + doc.total_pages + 'p' : ''}</div>
      </div>
      <div class="tree-doc-actions">
        <button class="tree-btn-view" title="웹 뷰어에서 문서 열람" onclick="event.stopPropagation(); viewDoc('${doc.name}');">열람</button>
        <button class="tree-btn-del" title="서재 및 지식망에서 삭제" onclick="deleteDoc(event, '${doc.name}')">내리기</button>
      </div>
    `;
    return item;
  }
'''

# Replace fetchDocs implementation in code
pattern = r'async function fetchDocs\(\)\s*\{[\s\S]*?async function deleteDoc'
replacement = tree_js.strip() + "\n\n  async function deleteDoc"

code = re.sub(pattern, replacement, code)

with open(server_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Successfully patched server.py with Folder Tree View!")
