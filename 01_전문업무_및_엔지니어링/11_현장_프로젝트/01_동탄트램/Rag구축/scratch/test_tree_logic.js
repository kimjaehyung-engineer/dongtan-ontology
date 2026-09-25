// Test script for syntax validation
const testScript = `
let currentDocTreeViewMode = 'zone'; // 'zone' or 'field'
window.cachedDocs = [
  { name: '#3편 증빙자료_토질 및 기초.pdf', size_mb: 326.22, total_pages: 221 },
  { name: '기본설계 시추주상도(1공구)_45공.pdf', size_mb: 28.32, total_pages: 54 },
  { name: '기본설계 시추주상도(2공구)_27공.pdf', size_mb: 5.06, total_pages: 30 },
  { name: '기술제안_4편 토질 및 기초(97~116).pdf', size_mb: 11.97, total_pages: 22 },
  { name: '토질_차량기지 비탈면 안정성 검토-rev01_260630.pdf', size_mb: 0.58, total_pages: 6 }
];
let currentViewingDoc = null;

function getCustomFolders() {
  try {
    return JSON.parse(localStorage.getItem('CUSTOM_USER_FOLDERS') || '[]');
  } catch(e) {
    return [];
  }
}

function saveCustomFolders(folders) {
  try {
    localStorage.setItem('CUSTOM_USER_FOLDERS', JSON.stringify(folders));
  } catch(e) {}
}

function getCustomDocFolderMap() {
  try {
    return JSON.parse(localStorage.getItem('CUSTOM_DOC_FOLDER_MAP') || '{}');
  } catch(e) {
    return {};
  }
}

function saveCustomDocFolderMap(map) {
  try {
    localStorage.setItem('CUSTOM_DOC_FOLDER_MAP', JSON.stringify(map));
  } catch(e) {}
}

function promptCreateNewFolder() {
  const name = prompt('생성할 새 폴더명을 입력하세요\\n(예: 05. 정거장 건축설계 / 06. 트램 궤도공사):');
  if (!name || !name.trim()) return;
  const clean = name.trim();
  const folders = getCustomFolders();
  if (!folders.includes(clean)) {
    folders.push(clean);
    saveCustomFolders(folders);
  }
  renderDocTree();
}

function promptMoveDocFolder(event, docName) {
  event.stopPropagation();
  const builtInFolders = currentDocTreeViewMode === 'zone' 
    ? ['00. 총괄 및 입찰·계약', '01. 1공구 본선', '02. 2공구 본선', '03. 차량기지', '04. 기술제안 및 특화', '05. 기타 및 일반']
    : ['총괄 · 계약', '토목 · 지반', '궤도 · 철도', '건축 · 정거장', '시스템 (신호/전기/통신)', '기타 · 일반'];
  const allFolders = Array.from(new Set([...builtInFolders, ...getCustomFolders()]));
  
  const msg = "'" + docName + "' 문서를 이동할 폴더를 선택하거나 직접 입력하세요:\\n\\n" + 
    allFolders.map((f, i) => (i + 1) + '. ' + f).join('\\n');
  const selected = prompt(msg, '1');
  if (!selected) return;

  let targetFolder = null;
  const idx = parseInt(selected.trim(), 10);
  if (!isNaN(idx) && idx >= 1 && idx <= allFolders.length) {
    targetFolder = allFolders[idx - 1];
  } else if (selected.trim()) {
    targetFolder = selected.trim();
    const cf = getCustomFolders();
    if (!cf.includes(targetFolder)) {
      cf.push(targetFolder);
      saveCustomFolders(cf);
    }
  }

  if (targetFolder) {
    const map = getCustomDocFolderMap();
    map[docName] = targetFolder;
    saveCustomDocFolderMap(map);
    renderDocTree();
  }
}

function classifyDoc(docName) {
  const customMap = getCustomDocFolderMap();
  let zone = customMap[docName] || null;
  let field = '기타 · 일반';

  if (!zone) {
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
    } else {
      zone = '05. 기타 및 일반';
    }
  }

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

function createDocItemEl(doc) {
  const item = document.createElement('div');
  item.className = 'tree-doc-item' + (currentViewingDoc === doc.name ? ' active' : '');
  item.onclick = (e) => {
    e.stopPropagation();
    viewDoc(doc.name);
    document.querySelectorAll('.tree-doc-item').forEach(el => el.classList.remove('active'));
    item.classList.add('active');
  };

  item.innerHTML = \`
    <span class="tree-doc-icon">📄</span>
    <div class="tree-doc-info">
      <div class="tree-doc-name" title="\${doc.name}">\${doc.name}</div>
      <div class="tree-doc-meta">\${doc.size_mb} MB\${doc.total_pages ? ' · ' + doc.total_pages + 'p' : ''}</div>
    </div>
    <div class="tree-doc-actions">
      <button class="tree-btn-view" title="웹 뷰어에서 문서 열람" onclick="event.stopPropagation(); viewDoc('\${doc.name}');">열람</button>
      <button class="tree-btn-move" title="다른 폴더로 이동" onclick="promptMoveDocFolder(event, '\${doc.name}');" style="font-size:10px; padding:2px 5px; border-radius:4px; background:#f8fafc; color:#475569; border:1px solid #cbd5e1; cursor:pointer;">이동</button>
      <button class="tree-btn-del" title="서재에서 삭제" onclick="deleteDoc(event, '\${doc.name}')">내리기</button>
    </div>
  \`;
  return item;
}

function renderDocTree() {
  const listEl = document.getElementById('docList');
  if (!listEl) return;
  listEl.innerHTML = '';
  const docs = window.cachedDocs || [];

  const badge = document.getElementById('docCountBadge');
  if (badge) {
    badge.innerText = '총 ' + docs.length + '권 탑재';
  }

  if (docs.length === 0) {
    listEl.innerHTML = '<div style="font-size:12px; color:var(--text-muted); padding:8px;">등록된 문서가 없습니다.</div>';
    return;
  }

  if (currentDocTreeViewMode === 'zone') {
    const builtInZones = [
      '00. 총괄 및 입찰·계약',
      '01. 1공구 본선',
      '02. 2공구 본선',
      '03. 차량기지',
      '04. 기술제안 및 특화',
      '05. 기타 및 일반'
    ];
    const customZones = getCustomFolders();
    const zoneOrder = Array.from(new Set([...builtInZones, ...customZones]));

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

      const folderEl = document.createElement('div');
      folderEl.className = 'tree-folder' + (zoneDocCount > 0 ? ' open' : '');

      folderEl.innerHTML = \`
        <div class="folder-header" onclick="this.parentElement.classList.toggle('open')">
          <span class="folder-arrow">▶</span>
          <span class="folder-icon">📁</span>
          <span class="folder-title" title="\${zoneName}">\${zoneName}</span>
          <span class="folder-badge">\${zoneDocCount}</span>
        </div>
        <div class="folder-content"></div>
      \`;

      const contentEl = folderEl.querySelector('.folder-content');

      if (zoneDocCount === 0) {
        contentEl.innerHTML = '<div style="font-size:11px; color:var(--text-muted); padding:4px 8px;">문서 없음 (+ 아래에서 파일 추가)</div>';
      } else {
        Object.keys(fields).forEach(fieldName => {
          const docList = fields[fieldName];
          if (!docList || docList.length === 0) return;

          const subEl = document.createElement('div');
          subEl.className = 'tree-subfolder';
          subEl.innerHTML = \`
            <div class="subfolder-header" onclick="const it = this.nextElementSibling; it.style.display = it.style.display==='none'?'flex':'none'">
              <span>📂</span>
              <span style="flex:1;">\${fieldName}</span>
              <span style="font-size:10px; opacity:0.7;">(\${docList.length})</span>
            </div>
            <div class="subfolder-items" style="display:flex; flex-direction:column; gap:3px;"></div>
          \`;

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
    const builtInFields = [
      '총괄 · 계약',
      '토목 · 지반',
      '궤도 · 철도',
      '건축 · 정거장',
      '시스템 (신호/전기/통신)',
      '기타 · 일반'
    ];
    const customFields = getCustomFolders();
    const fieldOrder = Array.from(new Set([...builtInFields, ...customFields]));

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

      const folderEl = document.createElement('div');
      folderEl.className = 'tree-folder' + (fieldDocCount > 0 ? ' open' : '');

      folderEl.innerHTML = \`
        <div class="folder-header" onclick="this.parentElement.classList.toggle('open')">
          <span class="folder-arrow">▶</span>
          <span class="folder-icon">📂</span>
          <span class="folder-title" title="\${fieldName}">\${fieldName}</span>
          <span class="folder-badge">\${fieldDocCount}</span>
        </div>
        <div class="folder-content"></div>
      \`;

      const contentEl = folderEl.querySelector('.folder-content');

      if (fieldDocCount === 0) {
        contentEl.innerHTML = '<div style="font-size:11px; color:var(--text-muted); padding:4px 8px;">문서 없음</div>';
      } else {
        Object.keys(zones).forEach(zoneName => {
          const docList = zones[zoneName];
          if (!docList || docList.length === 0) return;

          const subEl = document.createElement('div');
          subEl.className = 'tree-subfolder';
          subEl.innerHTML = \`
            <div class="subfolder-header" onclick="const it = this.nextElementSibling; it.style.display = it.style.display==='none'?'flex':'none'">
              <span>📍</span>
              <span style="flex:1;">\${zoneName}</span>
              <span style="font-size:10px; opacity:0.7;">(\${docList.length})</span>
            </div>
            <div class="subfolder-items" style="display:flex; flex-direction:column; gap:3px;"></div>
          \`;

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
`;
console.log("Ready to validate testScript");
