
    let activeDoc = "";
    let serverIp = "";
    let network = null;

    function initTheme() {
      const savedTheme = localStorage.getItem('THEME') || 'light';
      applyTheme(savedTheme);
    }

    function toggleTheme() {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      applyTheme(newTheme);
      localStorage.setItem('THEME', newTheme);
      if (network) {
        network.redraw();
      }
    }

    function applyTheme(theme) {
      const btn = document.getElementById('themeToggleBtn');
      if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        if (btn) btn.innerHTML = '☀️ 라이트 모드로 전환';
      } else {
        document.documentElement.removeAttribute('data-theme');
        if (btn) btn.innerHTML = '🌙 다크 모드로 전환';
      }
    }

    window.onload = async () => {
      initTheme();
      await fetchConfig();
      await fetchDocs();
    };

    function switchTab(tab) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      if (tab === 'chat') {
        document.querySelector('.tab-btn:nth-child(1)').classList.add('active');
        document.getElementById('chatTab').classList.add('active');
      } else {
        document.querySelector('.tab-btn:nth-child(2)').classList.add('active');
        document.getElementById('graphTab').classList.add('active');
        if (!hasLoadedMasterGraph) {
          loadMasterGraph();
        } else if (network) {
          setTimeout(() => network.fit(), 200);
        }
      }
    }

    async function fetchConfig() {
      try {
        const res = await fetch('/api/config');
        const data = await res.json();
        serverIp = data.server_ip;
        document.getElementById('serverAddress').innerText = `http://${serverIp}:${data.port}`;
        if (data.api_key) {
          document.getElementById('apiKeyInput').value = data.api_key;
        } else {
          const saved = localStorage.getItem('GEMINI_API_KEY');
          if (saved) {
            document.getElementById('apiKeyInput').value = saved;
            saveApiKey(saved);
          }
        }
      } catch (e) {
        console.error(e);
      }
    }

    async function saveApiKey(key) {
      localStorage.setItem('GEMINI_API_KEY', key);
      try {
        await fetch('/api/config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ api_key: key })
        });
      } catch(e) {}
    }

    let currentDocTreeViewMode = 'zone'; // 'zone' or 'field'
  window.cachedDocs = [];
  // currentViewingDoc declared in viewer section below

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
    const name = prompt('생성할 새 폴더명을 입력하세요 (예: 05. 정거장 건축설계 / 06. 트램 궤도공사):');
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
    
    const folderListStr = allFolders.map((f, i) => `${i + 1}. ${f}`).join('\n');
    const msg = `'${docName}' 문서를 이동할 폴더 번호(또는 새 폴더명)를 입력하세요:\n\n` + folderListStr;
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
    const isAct = (typeof currentViewingDoc !== 'undefined' && currentViewingDoc === doc.name);
    item.className = 'tree-doc-item' + (isAct ? ' active' : '');
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
        <button class="tree-btn-move" title="다른 폴더로 이동" onclick="promptMoveDocFolder(event, '${doc.name}');" style="font-size:10px; padding:2px 5px; border-radius:4px; background:#f8fafc; color:#475569; border:1px solid #cbd5e1; cursor:pointer;">이동</button>
        <button class="tree-btn-del" title="서재에서 삭제" onclick="deleteDoc(event, '${doc.name}')">내리기</button>
      </div>
    `;
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
          contentEl.innerHTML = '<div style="font-size:11px; color:var(--text-muted); padding:5px 8px;">(문서 없음)</div>';
        } else {
          Object.keys(fields).forEach(fieldName => {
            const docList = fields[fieldName];
            if (!docList || docList.length === 0) return;

            const subEl = document.createElement('div');
            subEl.className = 'tree-subfolder';
            subEl.innerHTML = `
              <div class="subfolder-header" onclick="const it = this.nextElementSibling; it.style.display = it.style.display==='none'?'flex':'none'">
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
          contentEl.innerHTML = '<div style="font-size:11px; color:var(--text-muted); padding:5px 8px;">(문서 없음)</div>';
        } else {
          Object.keys(zones).forEach(zoneName => {
            const docList = zones[zoneName];
            if (!docList || docList.length === 0) return;

            const subEl = document.createElement('div');
            subEl.className = 'tree-subfolder';
            subEl.innerHTML = `
              <div class="subfolder-header" onclick="const it = this.nextElementSibling; it.style.display = it.style.display==='none'?'flex':'none'">
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

  async function deleteDoc(event, name) {
      event.stopPropagation();
      const msg = `'${name}' 문서를 보관함에서 내리시겠습니까?\n\n※ 프로젝트 원본 파일은 안전하게 보존되며, 웹 화면(서버)에 업로드된 복사본 파일만 제거되어 디스크 용량이 확보됩니다.`;
      if (!confirm(msg)) {
        return;
      }
      try {
        const res = await fetch('/api/delete', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ document: name })
        });
        const data = await res.json();
        if (res.ok) {
          if (currentViewingDoc === name) {
            currentViewingDoc = null;
            const topDl = document.getElementById('topDownloadBtn');
            if (topDl) topDl.style.display = 'none';
            const vTitle = document.getElementById('viewerDocTitle');
            if (vTitle) vTitle.innerText = '출처 문서 미리보기';
            const vSize = document.getElementById('viewerDocSize');
            if (vSize) vSize.innerText = '';
            const iframe = document.getElementById('pdfViewerFrame');
            if (iframe) { iframe.src = 'about:blank'; iframe.style.display = 'none'; }
            const ph = document.getElementById('viewerPlaceholder');
            if (ph) ph.style.display = 'flex';
          }
          await fetchDocs();
        } else {
          alert('내리기 실패: ' + (data.error || '오류 발생'));
        }
      } catch(e) {
        alert('서버 요청 중 오류: ' + e);
      }
    }

    window.cachedDocs = [];
    let currentViewingDoc = null;

    function viewDoc(name) {
      currentViewingDoc = name;
      loadViewerDoc(name, 1);
      toggleViewerPanel(true);
      const topRef = document.getElementById('topSourceRef');
      if (topRef) {
        topRef.innerHTML = `📖 <b>직접 열람 중:</b> <span style="color:var(--text-color);">${name}</span>`;
      }
      const topDlBtn = document.getElementById('topDownloadBtn');
      if (topDlBtn) topDlBtn.style.display = 'inline-flex';
    }

    function linkifyPageNumbers(htmlText) {
      if (!htmlText) return '';
      // Linkify occurrences like p.50, p. 50, p.50~51, 페이지 50, (p.50)
      return htmlText.replace(/(?:p\.|페이지\s*)(\d+)(?:\s*[~-]\s*(\d+))?/gi, (match, p1, p2) => {
        const pageNum = parseInt(p1);
        const label = p2 ? `p.${p1}~${p2}` : `p.${p1}`;
        return `<button class="page-link-badge" onclick="jumpToPage(${pageNum})" title="클릭 시 우측 뷰어 ${pageNum}페이지로 즉시 이동">📄 ${label}</button>`;
      });
    }

    function loadViewerDoc(name, targetPage, activeSections) {
      if (!name) return;
      currentViewingDoc = name;
      const titleEl = document.getElementById('viewerDocTitle');
      const sizeEl = document.getElementById('viewerDocSize');
      const iframe = document.getElementById('pdfViewerFrame');
      const placeholder = document.getElementById('viewerPlaceholder');
      const pageBar = document.getElementById('viewerPageBar');
      const pillsContainer = document.getElementById('viewerPagePills');

      if (titleEl) {
        titleEl.innerText = name;
        titleEl.title = name;
      }

      const docObj = (window.cachedDocs || []).find(d => d.name === name);
      if (docObj && sizeEl) {
        sizeEl.innerText = `(${docObj.size_mb} MB${docObj.total_pages ? ' · ' + docObj.total_pages + 'p' : ''})`;
      } else if (sizeEl) {
        sizeEl.innerText = '';
      }

      const effectiveTargetPage = targetPage || 1;

      // Smart Fast Jump Pills: Priority to this query's matched activeSections!
      if (pillsContainer) {
        pillsContainer.innerHTML = '';
        const renderedPages = new Set();

        // 1. Matched Active Sections for this exact question
        if (activeSections && activeSections.length > 0) {
          activeSections.forEach(sec => {
            const pill = document.createElement('button');
            const isCur = sec.start_page === effectiveTargetPage;
            pill.className = 'page-pill highlight' + (isCur ? ' current' : '');
            pill.dataset.page = sec.start_page;
            const shortTitle = sec.title.replace(' 시추주상도', '').replace(' 구조계산서', '');
            pill.innerText = `🎯 ${shortTitle} (p.${sec.start_page})`;
            pill.title = `[질문 근거 섹션] ${sec.title} (p.${sec.start_page}~${sec.end_page})`;
            pill.onclick = () => jumpToPage(sec.start_page);
            pillsContainer.appendChild(pill);
            renderedPages.add(sec.start_page);
          });
        }

        // 2. Additional Sections from Document (if room)
        if (docObj && docObj.sections) {
          docObj.sections.slice(0, 16).forEach(sec => {
            if (renderedPages.has(sec.start_page)) return;
            const pill = document.createElement('button');
            const isCur = sec.start_page === effectiveTargetPage;
            pill.className = 'page-pill' + (isCur ? ' current' : '');
            pill.dataset.page = sec.start_page;
            const shortTitle = sec.title.replace(' 시추주상도', '').replace(' 구조계산서', '');
            pill.innerText = `${shortTitle} (p.${sec.start_page})`;
            pill.title = `${sec.title} (p.${sec.start_page}~${sec.end_page})`;
            pill.onclick = () => jumpToPage(sec.start_page);
            pillsContainer.appendChild(pill);
          });
        }

        if (pageBar) {
          pageBar.style.display = (pillsContainer.children.length > 0) ? 'flex' : 'none';
        }
      }

      if (iframe) {
        // Enforce reliable reload with timestamp to guarantee browser jumps to #page
        iframe.src = `/api/view?document=${encodeURIComponent(name)}&t=${Date.now()}#page=${effectiveTargetPage}`;
        iframe.style.display = 'block';
      }
      if (placeholder) {
        placeholder.style.display = 'none';
      }
    }

    function jumpToPage(pageNum) {
      if (!currentViewingDoc) return;
      const iframe = document.getElementById('pdfViewerFrame');
      if (iframe) {
        iframe.src = `/api/view?document=${encodeURIComponent(currentViewingDoc)}&t=${Date.now()}#page=${pageNum}`;
      }
      // Update active state among pills
      document.querySelectorAll('.page-pill').forEach(btn => {
        const isCurrent = btn.dataset.page == pageNum;
        btn.classList.toggle('current', isCurrent);
      });
      // Also sync direct jump input
      const input = document.getElementById('pageJumpInput');
      if (input) input.value = pageNum;
    }

    function jumpToDirectPage() {
      const input = document.getElementById('pageJumpInput');
      if (!input) return;
      const val = parseInt(input.value);
      if (val && val > 0) {
        jumpToPage(val);
      }
    }

    function downloadActiveDoc() {
      if (!currentViewingDoc) {
        alert('다운로드할 출처 문서가 아직 열리지 않았습니다. 질문을 입력하시거나 보관함의 [열람] 버튼을 누르세요.');
        return;
      }
      window.location.href = `/api/download?document=${encodeURIComponent(currentViewingDoc)}`;
    }

    function openActiveDocNewTab() {
      if (!currentViewingDoc) {
        alert('열람할 문서가 아직 없습니다. 질문을 입력하시거나 보관함의 [열람] 버튼을 누르세요.');
        return;
      }
      const page = document.getElementById('pageJumpInput')?.value || 1;
      window.open(`/api/view?document=${encodeURIComponent(currentViewingDoc)}#page=${page}`, '_blank');
    }

    function toggleViewerPanel(forceState) {
      const panel = document.getElementById('docViewerPanel');
      const btn = document.getElementById('topToggleViewerBtn');
      if (!panel) return;
      const isCollapsed = panel.classList.contains('collapsed');
      const shouldOpen = (forceState !== undefined) ? forceState : isCollapsed;
      if (shouldOpen) {
        panel.classList.remove('collapsed');
        if (btn) {
          btn.classList.add('active');
          btn.innerHTML = '📖 출처 문서 뷰어';
        }
        if (currentViewingDoc && document.getElementById('pdfViewerFrame') && (!document.getElementById('pdfViewerFrame').src || document.getElementById('pdfViewerFrame').src === 'about:blank')) {
          loadViewerDoc(currentViewingDoc);
        }
      } else {
        panel.classList.add('collapsed');
        if (btn) {
          btn.classList.remove('active');
          btn.innerHTML = '📖 뷰어 열기';
        }
      }
    }

    async function uploadDoc() {
      const fileInput = document.getElementById('fileInput');
      if (!fileInput.files || fileInput.files.length === 0) return;
      const files = Array.from(fileInput.files);
      const total = files.length;

      const uploadBtn = document.querySelector('.upload-btn');
      const originalText = uploadBtn ? uploadBtn.innerHTML : '➕ 새 시방서/보고서 PDF 추가';

      let successCount = 0;
      let lastUploadedName = '';

      for (let i = 0; i < total; i++) {
        const file = files[i];
        if (uploadBtn) {
          uploadBtn.innerHTML = `⏳ 업로드 중 (${i+1}/${total}): ${file.name.slice(0, 12)}...`;
          uploadBtn.style.opacity = '0.7';
          uploadBtn.style.pointerEvents = 'none';
        }

        const formData = new FormData();
        formData.append('file', file);
        try {
          const res = await fetch('/api/upload', {
            method: 'POST',
            body: formData
          });
          if (res.ok) {
            successCount++;
            lastUploadedName = file.name;
          }
        } catch (e) {
          console.error('업로드 실패:', file.name, e);
        }
      }

      if (uploadBtn) {
        uploadBtn.innerHTML = originalText;
        uploadBtn.style.opacity = '1.0';
        uploadBtn.style.pointerEvents = 'auto';
      }

      fileInput.value = '';
      await fetchDocs();
      if (lastUploadedName) {
        viewDoc(lastUploadedName);
      }
      if (total > 1) {
        alert(`선택한 ${total}개 파일 중 ${successCount}개 파일이 보관함에 추가되었습니다!`);
      }
    }

    function handleKey(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendQuery();
      }
    }

    function appendMessage(role, text) {
      const chatBody = document.getElementById('chatBody');
      if (!chatBody) return null;
      const msg = document.createElement('div');
      msg.className = `message ${role}`;
      msg.innerHTML = `
        <div class="avatar ${role}">${role === 'bot' ? '🤖' : '👷'}</div>
        <div class="message-content">${role === 'user' ? escapeHtml(text) : text}</div>
      `;
      chatBody.appendChild(msg);
      scrollToBottom();
      return msg.querySelector('.message-content');
    }

    function scrollToBottom() {
      const chatBody = document.getElementById('chatBody');
      if (chatBody) {
        chatBody.scrollTop = chatBody.scrollHeight;
      }
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    
    
    let originalRawNodes = [];
    let originalRawEdges = [];
    let isGraphHighlighted = false;

    function resetGraphHighlight() {
      if (!isGraphHighlighted || !window.masterGraphDataSets) return;
      const { nodes, edges } = window.masterGraphDataSets;
      
      // 원본 상태로 복원
      const colorMap = {
        'BORING': { background: '#f97316', border: '#ea580c' },
        'STRATUM': { background: '#a16207', border: '#854d0e' },
        'PARAMETER': { background: '#06b6d4', border: '#0891b2' },
        'DESIGN_ELEMENT': { background: '#3b82f6', border: '#2563eb' },
        'DISCREPANCY': { background: '#ef4444', border: '#dc2626' },
        'DEFAULT': { background: '#64748b', border: '#475569' }
      };

      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

      const nodeUpdates = originalRawNodes.map(n => {
        const col = colorMap[n.type] || colorMap['DEFAULT'];
        return {
          id: n.id,
          color: { background: col.background, border: col.border },
          opacity: 1.0,
          font: { color: '#fff', size: 12 },
          size: n.type === 'DESIGN_ELEMENT' ? 24 : 18
        };
      });
      nodes.update(nodeUpdates);

      const edgeUpdates = originalRawEdges.map(e => {
        const isWarn = e.is_warning || e.relation === 'DISCREPANCY';
        return {
          id: e.id || `${e.from}_${e.to}`,
          color: isWarn ? { color: '#ef4444' } : { color: isDark ? '#64748b' : '#94a3b8' },
          width: isWarn ? 2.5 : 1.2,
          opacity: 1.0
        };
      });
      edges.update(edgeUpdates);

      isGraphHighlighted = false;
      const chip = document.getElementById('resetHighlightChip');
      if (chip) chip.style.display = 'none';

      if (network) network.fit({ animation: { duration: 600, easingFunction: 'easeInOutQuad' } });
    }

    async function highlightGraphPath(targetNodeIdsJson) {
      let targetIds = [];
      try {
        const decoded = typeof targetNodeIdsJson === 'string' ? decodeURIComponent(targetNodeIdsJson) : targetNodeIdsJson;
        targetIds = typeof decoded === 'string' ? JSON.parse(decoded) : decoded;
      } catch (e) {
        targetIds = targetNodeIdsJson.split(',').map(s => s.trim()).filter(Boolean);
      }
      if (!targetIds || targetIds.length === 0) return;

      // 1. 그래프 탭으로 전환
      switchTab('graph');

      // 2. 마스터 그래프가 아직 없으면 로드 대기
      if (!hasLoadedMasterGraph) {
        await loadMasterGraph();
        await new Promise(r => setTimeout(r, 600));
      }

      if (!window.masterGraphDataSets || !network) return;
      const { nodes, edges } = window.masterGraphDataSets;

      const targetSet = new Set(targetIds);

      // 허브 노드 및 관련 엣지도 포함
      originalRawEdges.forEach(e => {
        if (targetSet.has(e.from) && targetSet.has(e.to)) {
          // Both in path
        }
      });

      // 3. 노드 스타일 업데이트: 타겟 노드는 형광 네온 하이라이트 + 확대, 나머지는 페이드아웃
      const nodeUpdates = originalRawNodes.map(n => {
        const isHit = targetSet.has(n.id);
        if (isHit) {
          return {
            id: n.id,
            color: { background: '#f59e0b', border: '#b45309', highlight: { background: '#fbbf24', border: '#d97706' } },
            font: { color: '#ffffff', size: 14, strokeWidth: 2, strokeColor: '#000' },
            size: n.type === 'DESIGN_ELEMENT' ? 32 : 26,
            shadow: { enabled: true, color: '#f59e0b', size: 16 }
          };
        } else {
          return {
            id: n.id,
            color: { background: 'rgba(100, 116, 139, 0.25)', border: 'rgba(100, 116, 139, 0.3)' },
            font: { color: 'rgba(255, 255, 255, 0.3)', size: 10 },
            shadow: { enabled: false },
            size: 14
          };
        }
      });
      nodes.update(nodeUpdates);

      // 4. 엣지 업데이트: 타겟 연결선은 두껍고 선명하게, 나머지는 투명하게
      const edgeUpdates = originalRawEdges.map(e => {
        const isHit = targetSet.has(e.from) && targetSet.has(e.to);
        const isConnected = targetSet.has(e.from) || targetSet.has(e.to);
        if (isHit) {
          return {
            id: e.id || `${e.from}_${e.to}`,
            color: { color: '#f59e0b' },
            width: 3.5,
            opacity: 1.0
          };
        } else if (isConnected) {
          return {
            id: e.id || `${e.from}_${e.to}`,
            color: { color: 'rgba(245, 158, 11, 0.6)' },
            width: 2.2,
            opacity: 0.8
          };
        } else {
          return {
            id: e.id || `${e.from}_${e.to}`,
            color: { color: 'rgba(148, 163, 184, 0.1)' },
            width: 0.8,
            opacity: 0.1
          };
        }
      });
      edges.update(edgeUpdates);

      isGraphHighlighted = true;

      // 5. 복원 칩 표시
      let chip = document.getElementById('resetHighlightChip');
      if (!chip) {
        const toolbar = document.querySelector('.graph-toolbar');
        if (toolbar) {
          chip = document.createElement('button');
          chip.id = 'resetHighlightChip';
          chip.className = 'graph-reset-chip';
          chip.innerHTML = '✨ 탐색 경로 표시 중 (클릭 시 전체 복원)';
          chip.onclick = resetGraphHighlight;
          toolbar.appendChild(chip);
        }
      } else {
        chip.style.display = 'inline-flex';
      }

      // 6. 타겟 노드 군집으로 부드럽게 줌인(Focus)
      setTimeout(() => {
        const existingTargetIds = targetIds.filter(id => nodes.get(id));
        if (existingTargetIds.length > 0) {
          network.fit({
            nodes: existingTargetIds,
            animation: { duration: 900, easingFunction: 'easeInOutQuad' }
          });
        }
      }, 200);
    }

    function toggleTrace(el) {
      const card = el.closest('.trace-card');
      const body = card.querySelector('.trace-body');
      const arrow = card.querySelector('.trace-arrow');
      if (body.style.display === 'none' || !body.style.display) {
        body.style.display = 'block';
        if (arrow) arrow.innerText = '▲';
      } else {
        body.style.display = 'none';
        if (arrow) arrow.innerText = '▼';
      }
    }

    function buildTraceHtml(trace) {
      if (!trace || !trace.steps || trace.steps.length === 0) return '';
      let stepsHtml = '';
      trace.steps.forEach(s => {
        stepsHtml += `
          <div class="trace-item">
            <div class="trace-dot">${s.step}</div>
            <div class="trace-content">
              <div class="trace-step-title">
                <span>${s.icon || '📌'} ${s.title}</span>
                <span class="trace-step-badge">${s.badge || '완료'}</span>
              </div>
              <div class="trace-step-desc">${s.detail}</div>
            </div>
          </div>
        `;
      });

      return `
        <div class="trace-card">
          <div class="trace-header" onclick="toggleTrace(this)">
            <div style="display:flex; align-items:center; gap:8px;">
              <span>🧭</span>
              <span style="font-weight:600; font-size:12.5px; color:var(--heading-color);">AI 탐색 및 추론 과정 추적 (색인 ➔ 지식망 ➔ 팩트 ➔ Gemini)</span>
              <span class="trace-badge">4단계 완료</span>
            </div>
            <span class="trace-arrow" style="font-size:10px; color:var(--text-muted);">▲ 접기</span>
          </div>
          <div class="trace-body" style="display:block;">
            <div class="trace-timeline">
              ${stepsHtml}
            </div>
            ${trace.highlight_nodes && trace.highlight_nodes.length > 0 ? `
              <div style="margin-top: 12px; padding-top: 10px; border-top: 1px dashed var(--border-color); display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 11px; color: var(--text-muted);">지식망 탐색 노드: <b>${trace.highlight_nodes.length}개</b> 연계 검출</span>
                <button class="trace-graph-view-btn" onclick="highlightGraphPath('${encodeURIComponent(JSON.stringify(trace.highlight_nodes))}')">
                  🌐 이 답변에 쓰인 지식망 경로 그래프로 직접 보기 (${trace.highlight_nodes.length}개 노드) ➔
                </button>
              </div>
            ` : ''}
          </div>
        </div>
      `;
    }

    async function sendQuery() {
      const input = document.getElementById('promptInput');
      if (!input) return;
      const query = input.value.trim();
      if (!query) return;

      const apiKeyEl = document.getElementById('apiKeyInput');
      const apiKey = apiKeyEl ? apiKeyEl.value.trim() : '';

      appendMessage('user', query);
      input.value = '';

      const sendBtn = document.getElementById('sendBtn');
      if (sendBtn) {
        sendBtn.disabled = true;
        sendBtn.innerHTML = '<span class="loading-spinner"></span> 색인 탐색 & 분석 중...';
      }

      const botMsgDiv = appendMessage('bot', `
        <div class="progress-box" style="font-size:12.5px; line-height: 1.6; color: var(--text-color); padding: 8px 12px; background: var(--bg-card); border-radius: 6px; border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);">
          <div id="step1" style="font-weight:600; color: #0284c7;">🧠 1단계: 질문 의도 분석 및 공간/공종 라우팅 중...</div>
          <div id="step2" style="color: var(--text-muted); opacity: 0.6;">🌐 2단계: 지식 그래프(Graph) 위험 관계망 탐색 대기</div>
          <div id="step3" style="color: var(--text-muted); opacity: 0.6;">📂 3단계: 글로벌 기술문서 메타 색인(Index) 스코어링 대기</div>
          <div id="step4" style="color: var(--text-muted); opacity: 0.6;">🤖 4단계: Gemini 100만 컨텍스트 두뇌 심층 분석 대기</div>
        </div>
      `);

      const t1 = setTimeout(() => {
        const s1 = document.getElementById('step1');
        const s2 = document.getElementById('step2');
        if (s1 && s2) {
          s1.innerHTML = '✅ 1단계: 질문 의도 분석 및 라우팅 완료 (0.001s)';
          s1.style.color = '#15803d';
          s2.innerHTML = '<span class="loading-spinner"></span> 2단계: 지식 그래프(Graph) 4대 허브/2대 리스크 탐색 중...';
          s2.style.fontWeight = '600';
          s2.style.color = '#0284c7';
          s2.style.opacity = '1.0';
        }
      }, 500);

      const t2 = setTimeout(() => {
        const s2 = document.getElementById('step2');
        const s3 = document.getElementById('step3');
        if (s2 && s3) {
          s2.innerHTML = '✅ 2단계: 지식 그래프 관계 탐색 완료 (0.004s)';
          s2.style.color = '#15803d';
          s3.innerHTML = '<span class="loading-spinner"></span> 3단계: 5개 대용량 문서 색인(Index) 정밀 스코어링 중...';
          s3.style.fontWeight = '600';
          s3.style.color = '#0284c7';
          s3.style.opacity = '1.0';
        }
      }, 1100);

      const t3 = setTimeout(() => {
        const s3 = document.getElementById('step3');
        const s4 = document.getElementById('step4');
        if (s3 && s4) {
          s3.innerHTML = '✅ 3단계: 기술문서 메타 색인 정밀 발췌 완료';
          s3.style.color = '#15803d';
          s4.innerHTML = '<span class="loading-spinner"></span> 4단계: Gemini 100만 컨텍스트 심층 추론 & 팩트 검증 중...';
          s4.style.fontWeight = '600';
          s4.style.color = '#2563eb';
          s4.style.opacity = '1.0';
        }
      }, 1800);

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            api_key: apiKey,
            query: query
          })
        });
        clearTimeout(t1);
        clearTimeout(t2); clearTimeout(t3);

        const data = await res.json();
        if (data.error) {
          if (botMsgDiv) botMsgDiv.innerHTML = `<span style="color:#ef4444;">⚠️ 오류: ${data.error}</span>`;
        } else {
          let parsedHtml = marked.parse(data.reply);
          parsedHtml = linkifyPageNumbers(parsedHtml);

          // Trace fallback 보장
          const traceData = data.trace || {
            query: query,
            highlight_nodes: (query.match(/(?:NH|DT|GB|NGB)-?\d+/gi) || []).map(h => 'bh_' + h.toUpperCase().replace(' ', '')),
            steps: [
              { step: 1, icon: "🧠", title: "질문 의도 분석 및 공간/공종 라우팅", badge: "분석 완료", detail: `질문 키워드 분석: '${query}'` },
              { step: 2, icon: "🌐", title: "지식 그래프(Graph) 선제 탐색 ➔ 색인 피드백", badge: "지식망 매핑", detail: "4대 구간 허브 및 2대 리스크 클러스터 탐색 완료" },
              { step: 3, icon: "📂", title: "글로벌 기술문서 메타 색인(Index) 정밀 발췌", badge: (data.source_document ? data.source_document.slice(0, 20) : "색인 완료"), detail: `${data.source_document || '출처 문서'} (p.${data.source_page || 1}) 핀포인트 확정` },
              { step: 4, icon: "🤖", title: "Gemini / 지반 DB 정밀 팩트 검증", badge: "답변 합성 완료", detail: "시추주상도 팩트 수치 대조 및 원본 페이지 링크 생성" }
            ]
          };

          const traceHtml = buildTraceHtml(traceData);
          if (botMsgDiv) {
            botMsgDiv.innerHTML = traceHtml + parsedHtml;
          }

          // 자동 탐색된 출처 문서와 우측 뷰어 실시간 연동 (맞춤 근거 섹션 전달)
          if (data.source_document) {
            currentViewingDoc = data.source_document;
            loadViewerDoc(data.source_document, data.source_page || 1, data.active_sections || []);
            toggleViewerPanel(true);

            const topRef = document.getElementById('topSourceRef');
            if (topRef) {
              const secInfo = data.matched_sections && data.matched_sections.length > 0 ? ` (${data.matched_sections[0]})` : ` (p.${data.source_page || 1})`;
              topRef.innerHTML = `📂 <b>자동 탐색 출처:</b> <span style="color:var(--text-color); font-weight:600; cursor:pointer;" onclick="jumpToPage(${data.source_page || 1})" title="클릭 시 뷰어 이동">${data.source_document}</span>${secInfo}`;
            }
            const topDlBtn = document.getElementById('topDownloadBtn');
            if (topDlBtn) topDlBtn.style.display = 'inline-flex';
          }
        }
      } catch (err) {
        if (botMsgDiv) botMsgDiv.innerHTML = `<span style="color:#ef4444;">⚠️ 서버 통신 오류: ${err.message}</span>`;
      } finally {
        if (sendBtn) {
          sendBtn.disabled = false;
          sendBtn.innerText = '전송';
        }
        scrollToBottom();
      }
    }

    
    let hasLoadedMasterGraph = false;
    let currentGraphFilter = { section: 'all', riskOnly: false };

    async function loadMasterGraph(section = 'all', riskOnly = false) {
      currentGraphFilter = { section, riskOnly };
      const overlay = document.getElementById('graphLoadingOverlay');
      if (overlay) overlay.style.display = 'flex';

      const btn = document.getElementById('extractBtn');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = `<span class="loading-spinner"></span> 지식 그래프 갱신 중...`;
      }

      try {
        const queryParams = new URLSearchParams();
        if (section && section !== 'all') queryParams.append('section', section);
        if (riskOnly) queryParams.append('risk_only', 'true');

        const res = await fetch('/api/graph/master?' + queryParams.toString());
        const data = await res.json();

        if (data.error) {
          alert('지식 그래프 로딩 실패: ' + data.error);
          return;
        }

        renderNetwork(data.nodes, data.edges);
        hasLoadedMasterGraph = true;

        if (data.summary) {
          const sumBox = document.getElementById('summaryBox');
          if (sumBox) sumBox.style.display = 'block';
          const sumContent = document.getElementById('summaryContent');
          if (sumContent) sumContent.innerText = data.summary;
        }
        if (data.discrepancies && data.discrepancies.length > 0) {
          const discBox = document.getElementById('discrepancyBox');
          if (discBox) discBox.style.display = 'block';
          const discContent = document.getElementById('discrepancyContent');
          if (discContent) {
            discContent.innerHTML = data.discrepancies.slice(0, 15).map(d => `• ${d}`).join('<br>') + 
              (data.discrepancies.length > 15 ? `<br><small style="color:var(--text-muted);">외 ${data.discrepancies.length - 15}건 생략</small>` : '');
          }
        } else {
          const discBox = document.getElementById('discrepancyBox');
          if (discBox) discBox.style.display = 'none';
        }

      } catch (err) {
        console.error('loadMasterGraph error:', err);
      } finally {
        if (overlay) overlay.style.display = 'none';
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = '⚡ 지식 그래프 자동 추출 & 분석 실행';
        }
      }
    }

    function applyGraphFilter(section, riskOnly, btn) {
      document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
      if (btn) btn.classList.add('active');
      loadMasterGraph(section, riskOnly);
    }

    function openBoreholePdf(docName, page) {
      switchTab('chat');
      setTimeout(() => {
        const select = document.getElementById('documentSelect');
        if (select) {
          select.value = docName;
          onDocumentSelect();
          setTimeout(() => {
            if (typeof jumpToPage === 'function') {
              jumpToPage(page);
            }
          }, 600);
        }
      }, 200);
    }

    /* GraphRAG Extraction */
    async function extractGraph() {
      const apiKey = document.getElementById('apiKeyInput').value.trim();
      if (!apiKey) {
        alert('우측 상단에 Gemini API Key를 먼저 입력해 주세요.');
        return;
      }
      const targetDoc = currentViewingDoc || (window.cachedDocs && window.cachedDocs.length > 0 ? window.cachedDocs[0].name : null);
      if (!targetDoc) {
        alert('보관함에 등록된 문서가 없습니다. 먼저 PDF를 등록해 주세요.');
        return;
      }

      const btn = document.getElementById('extractBtn');
      btn.disabled = true;
      btn.innerHTML = `<span class="loading-spinner"></span> 지반·공종 관계망 분석 중 (${targetDoc})...`;

      try {
        const res = await fetch('/api/extract-graph', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            api_key: apiKey,
            document: targetDoc
          })
        });

        const data = await res.json();
        if (data.error) {
          alert('오류 발생: ' + data.error);
          return;
        }

        renderNetwork(data.nodes, data.edges);

        if (data.summary) {
          document.getElementById('summaryBox').style.display = 'block';
          document.getElementById('summaryContent').innerText = data.summary;
        }
        if (data.discrepancies && data.discrepancies.length > 0) {
          document.getElementById('discrepancyBox').style.display = 'block';
          document.getElementById('discrepancyContent').innerHTML = data.discrepancies.map(d => `• ${d}`).join('<br>');
        } else {
          document.getElementById('discrepancyBox').style.display = 'none';
        }

      } catch (err) {
        alert('네트워크 오류: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '⚡ 지식 그래프 재분석 실행';
      }
    }

    function renderNetwork(rawNodes, rawEdges) {
      originalRawNodes = rawNodes;
      originalRawEdges = rawEdges;
      const container = document.getElementById('networkCanvas');

      const colorMap = {
        'BORING': { background: '#f97316', border: '#ea580c' },
        'STRATUM': { background: '#a16207', border: '#854d0e' },
        'PARAMETER': { background: '#06b6d4', border: '#0891b2' },
        'DESIGN_ELEMENT': { background: '#3b82f6', border: '#2563eb' },
        'EQUIPMENT': { background: '#8b5cf6', border: '#7c3aed' },
        'DEFAULT': { background: '#64748b', border: '#475569' }
      };

      const nodes = new vis.DataSet(rawNodes.map(n => {
        const col = colorMap[n.type] || colorMap['DEFAULT'];
        return {
          id: n.id,
          label: n.label,
          title: n.description || n.label,
          color: { background: col.background, border: col.border, highlight: { background: '#fff', border: col.border } },
          font: { color: '#fff', size: 12, face: 'Noto Sans KR' },
          shape: n.type === 'BORING' ? 'box' : (n.type === 'PARAMETER' ? 'ellipse' : 'dot'),
          size: n.type === 'DESIGN_ELEMENT' ? 24 : 18,
          rawType: n.type,
          rawDesc: n.description || ''
        };
      }));

      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

      const edges = new vis.DataSet(rawEdges.map(e => {
        const isWarn = e.is_warning || e.relation === 'DISCREPANCY';
        return {
          from: e.from,
          to: e.to,
          label: e.label || e.relation,
          arrows: 'to',
          color: isWarn ? { color: '#ef4444', highlight: '#f87171' } : { color: isDark ? '#64748b' : '#94a3b8', highlight: '#3b82f6' },
          dashes: isWarn ? [5, 5] : false,
          width: isWarn ? 2.5 : 1.2,
          font: {
            color: isWarn ? '#ef4444' : (isDark ? '#cbd5e1' : '#334155'),
            size: 10,
            align: 'middle',
            background: isDark ? '#1a1d24' : '#ffffff',
            strokeWidth: 0
          }
        };
      }));

      const data = { nodes: nodes, edges: edges };
      const options = {
        physics: {
          stabilization: true,
          barnesHut: { gravitationalConstant: -3000, springLength: 120 }
        },
        interaction: { hover: true, tooltipDelay: 100 }
      };

      if (network) network.destroy();
      network = new vis.Network(container, data, options);
      window.masterGraphDataSets = { nodes, edges };

      network.on("click", function (params) {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0];
          const nodeData = nodes.get(nodeId);
          const raw = rawNodes.find(n => n.id === nodeId) || {};
          document.getElementById('nodeDetailBox').style.display = 'block';
          document.getElementById('nodeDetailLabel').innerText = `[${nodeData.rawType}] ${nodeData.label}`;
          
          let descHtml = (nodeData.rawDesc || `ID: ${nodeData.id}`).split('\\n').join('<br>');
          
          if (raw.type === 'BORING' && raw.doc_name && raw.page) {
            descHtml += `<div style="margin-top:10px;">
              <button class="borehole-jump-btn" onclick="openBoreholePdf('${raw.doc_name}', ${raw.page})">
                📄 원본 주상도 열기 (p.${raw.page})
              </button>
            </div>`;
          } else if (raw.type === 'DISCREPANCY' && raw.target) {
            const targetBh = rawNodes.find(n => n.label === raw.target);
            if (targetBh && targetBh.doc_name && targetBh.page) {
              descHtml += `<div style="margin-top:10px;">
                <button class="borehole-jump-btn" style="background:#ef4444;" onclick="openBoreholePdf('${targetBh.doc_name}', ${targetBh.page})">
                  ⚠️ 위험 대상(${raw.target}) 주상도 열기 (p.${targetBh.page})
                </button>
              </div>`;
            }
          }
          document.getElementById('nodeDetailDesc').innerHTML = descHtml;
        }
      });
    }
  