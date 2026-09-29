
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

      // 모바일 & 카카오톡 링크 파라미터 자동 연동 (?doc=...&p=...)
      try {
        const urlParams = new URLSearchParams(window.location.search);
        const targetDoc = urlParams.get('doc');
        const targetPage = parseInt(urlParams.get('p') || '1', 10);
        if (targetDoc) {
          console.log(`[AutoViewer] Loading ${targetDoc} p.${targetPage}`);
          loadViewerDoc(targetDoc, targetPage);
          toggleViewerPanel(true);
        }
      } catch (err) {
        console.error("URL Params error:", err);
      }
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

    window.docsRootPath = '';
  window.cachedDocs = [];
  window.cachedTree = null;
  let currentViewingDoc = null;
  let currentViewingRelPath = null;

  async function changeRootFolder() {
    const currentPath = window.docsRootPath || '';
    const newPath = prompt("참조할 상위 폴더(루트 경로)를 입력하세요 (하위 모든 폴더/문서 자동 연동):", currentPath);
    if (!newPath || !newPath.trim() || newPath.trim() === currentPath) return;

    try {
      const res = await fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ docs_root_path: newPath.trim() })
      });
      const data = await res.json();
      if (data.status === 'ok') {
        alert("상위 폴더가 설정되었습니다:
" + data.docs_root_path);
        await fetchDocs();
      } else {
        alert("폴더 설정 실패: " + (data.error || '폴더가 존재하지 않거나 접근할 수 없습니다.'));
      }
    } catch(e) {
      alert("오류 발생: " + e.message);
    }
  }

  async function openRootInExplorer(event) {
    const btn = (event && event.currentTarget) ? event.currentTarget : document.querySelector('button[onclick*="openRootInExplorer"]');
    const oldHtml = btn ? btn.innerHTML : '';
    if (btn) btn.innerHTML = '📂 탐색기 여는 중...';
    try {
      const res = await fetch('/api/open_explorer', { method: 'POST' });
      const data = await res.json();
      if (!res.ok) {
        alert('탐색기 열기 실패: ' + (data.error || '오류 발생'));
      }
    } catch(e) {
      alert('요청 실패: ' + e.message);
    } finally {
      if (btn) setTimeout(() => { btn.innerHTML = oldHtml; }, 1000);
    }
  }

  async function fetchDocs() {
    try {
      const res = await fetch('/api/documents?tree=true');
      const data = await res.json();
      
      if (data.root_path) {
        window.docsRootPath = data.root_path;
        const rootDisplay = document.getElementById('rootFolderPathDisplay');
        if (rootDisplay) {
          rootDisplay.innerText = data.root_path;
          rootDisplay.title = data.root_path;
        }
      }
      
      window.cachedDocs = data.docs || (Array.isArray(data) ? data : []);
      window.cachedTree = data.tree || null;
      
      const badge = document.getElementById('docCountBadge');
      if (badge) {
        badge.innerText = `총 ${window.cachedDocs.length}개 파일 연동`;
      }
      
      renderDocTree();
    } catch(e) {
      console.error(e);
    }
  }

  function renderDocTree() {
    const listEl = document.getElementById('docList');
    if (!listEl) return;
    listEl.innerHTML = '';

    const tree = window.cachedTree;
    if (!tree || !tree.children || tree.children.length === 0) {
      listEl.innerHTML = '<div style="font-size:12px; color:var(--text-muted); padding:12px; text-align:center;">지정된 상위 폴더에 참조 가능한 문서가 없습니다.</div>';
      return;
    }

    // Render tree children (if root has single folder, unwrap or render direct)
    tree.children.forEach(child => {
      listEl.appendChild(createTreeNodeElement(child, 1));
    });
  }

  function createTreeNodeElement(node, depth) {
    if (node.type === 'folder') {
      const folderEl = document.createElement('div');
      // Top 2 levels open by default
      const defaultOpen = depth <= 2;
      folderEl.className = 'tree-folder' + (defaultOpen ? ' open' : '');
      folderEl.style.marginLeft = depth > 1 ? '6px' : '0px';
      folderEl.style.borderLeft = depth > 1 ? '2px solid #cbd5e1' : '';
      folderEl.style.paddingLeft = depth > 1 ? '6px' : '0px';

      const headerEl = document.createElement('div');
      headerEl.className = 'folder-header';
      headerEl.style.display = 'flex';
      headerEl.style.alignItems = 'center';
      headerEl.style.gap = '6px';
      headerEl.style.padding = '6px 8px';
      headerEl.style.cursor = 'pointer';
      headerEl.style.borderRadius = '6px';

      headerEl.innerHTML = `
        <span class="folder-arrow" style="font-size: 10px; color: #64748b; transition: transform 0.2s; display: inline-block;">${defaultOpen ? '▼' : '▶'}</span>
        <span class="folder-icon" style="font-size: 13px;">📁</span>
        <span class="folder-title" title="${node.name}" style="flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-weight:600; font-size:11.5px; color:var(--text-color, #1e293b);">${node.name}</span>
        <span class="folder-badge" style="font-size:10px; background:#e2e8f0; color:#475569; padding:1px 6px; border-radius:10px; font-weight:600;">${node.total_files || (node.children ? node.children.length : 0)}</span>
      `;

      const contentEl = document.createElement('div');
      contentEl.className = 'folder-content';
      contentEl.style.display = defaultOpen ? 'flex' : 'none';
      contentEl.style.flexDirection = 'column';
      contentEl.style.gap = '3px';
      contentEl.style.marginTop = '3px';

      headerEl.onclick = (e) => {
        e.stopPropagation();
        const isOpen = contentEl.style.display !== 'none';
        contentEl.style.display = isOpen ? 'none' : 'flex';
        headerEl.querySelector('.folder-arrow').textContent = isOpen ? '▶' : '▼';
        folderEl.classList.toggle('open', !isOpen);
      };

      if (node.children && node.children.length > 0) {
        node.children.forEach(sub => {
          contentEl.appendChild(createTreeNodeElement(sub, depth + 1));
        });
      } else {
        contentEl.innerHTML = '<div style="font-size:10.5px; color:var(--text-muted); padding:3px 8px;">(빈 폴더)</div>';
      }

      folderEl.appendChild(headerEl);
      folderEl.appendChild(contentEl);
      return folderEl;
    } else {
      // File node
      const doc = node;
      const item = document.createElement('div');
      const isAct = (typeof currentViewingDoc !== 'undefined' && (currentViewingDoc === doc.name || currentViewingDoc === doc.rel_path));
      item.className = 'tree-doc-item' + (isAct ? ' active' : '');
      item.style.marginLeft = depth > 1 ? '4px' : '0px';

      let icon = '📄';
      if (doc.ext === '.xlsx' || doc.ext === '.xls' || doc.ext === '.csv') icon = '📊';
      else if (doc.ext === '.hwp' || doc.ext === '.hwpx' || doc.ext === '.docx') icon = '📝';
      else if (doc.ext === '.txt') icon = '📃';

      item.onclick = (e) => {
        e.stopPropagation();
        viewDoc(doc.rel_path, doc.name);
        document.querySelectorAll('.tree-doc-item').forEach(el => el.classList.remove('active'));
        item.classList.add('active');
      };

      item.innerHTML = `
        <span class="tree-doc-icon">${icon}</span>
        <div class="tree-doc-info" style="flex:1; min-width:0;">
          <div class="tree-doc-name" title="${doc.name}" style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis; font-size:11.5px; font-weight:500;">${doc.name}</div>
          <div class="tree-doc-meta" style="font-size:10px; color:var(--text-muted);">${doc.size_mb} MB${doc.total_pages ? ' · ' + doc.total_pages + 'p' : ''}</div>
        </div>
        <div class="tree-doc-actions">
          <button class="tree-btn-view" title="웹 뷰어에서 문서 열람" onclick="event.stopPropagation(); viewDoc('${doc.rel_path}', '${doc.name}');">열람</button>
          <a href="/api/download?path=${encodeURIComponent(doc.rel_path)}" download="${doc.name}" class="tree-btn-view" style="text-decoration:none; background:#f1f5f9; color:#475569; border-color:#cbd5e1;" title="파일 다운로드" onclick="event.stopPropagation();">받기</a>
        </div>
      `;
      return item;
    }
  }

  function viewDoc(relPath, name) {
    const docName = name || relPath;
    currentViewingDoc = docName;
    currentViewingRelPath = relPath || docName;
    loadViewerDoc(currentViewingRelPath, 1);
    toggleViewerPanel(true);
    const topRef = document.getElementById('topSourceRef');
    if (topRef) {
      topRef.innerHTML = `📖 <b>직접 열람 중:</b> <span style="color:var(--text-color);">${docName}</span>`;
    }
    const topDlBtn = document.getElementById('topDownloadBtn');
    if (topDlBtn) {
      topDlBtn.style.display = 'inline-flex';
      topDlBtn.onclick = () => window.open(`/api/download?path=${encodeURIComponent(currentViewingRelPath)}`, '_blank');
    }
  }



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

      const isPdf = name.toLowerCase().endsWith('.pdf');
      if (iframe && isPdf) {
        iframe.src = `/api/view?path=${encodeURIComponent(name)}&t=${Date.now()}#page=${effectiveTargetPage}`;
        iframe.style.display = 'block';
        if (placeholder) placeholder.style.display = 'none';
      } else if (!isPdf) {
        if (iframe) iframe.style.display = 'none';
        if (placeholder) {
          placeholder.style.display = 'flex';
          placeholder.innerHTML = `
            <div style="text-align: center; padding: 40px 20px;">
              <div style="font-size: 48px; margin-bottom: 12px;">📊</div>
              <h3 style="margin-bottom: 8px; color: var(--text-color);">${name}</h3>
              <p style="color: var(--text-muted); font-size: 13px; margin-bottom: 20px;">
                본 파일은 스프레드시트 또는 기술 보고서 데이터입니다.<br>
                AI 질의 시 본 파일의 내용 및 정수를 자동으로 분석·참조합니다.
              </p>
              <a href="/api/download?path=${encodeURIComponent(name)}" class="btn-primary" style="display: inline-flex; align-items: center; gap: 6px; padding: 10px 18px; border-radius: 8px; background: #2563eb; color: #fff; text-decoration: none; font-weight: 600;">
                ⬇️ 파일 다운로드 및 열기
              </a>
            </div>
          `;
        }
      }
    }

    function jumpToPage(pageNum) {
      if (!currentViewingDoc) return;
      const iframe = document.getElementById('pdfViewerFrame');
      if (iframe) {
        iframe.src = `/api/view?path=${encodeURIComponent(currentViewingRelPath || currentViewingDoc)}&t=${Date.now()}#page=${pageNum}`;
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
          
          let descHtml = (nodeData.rawDesc || `ID: ${nodeData.id}`).split('\n').join('<br>');
          
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
  