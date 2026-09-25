
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

    async function fetchDocs() {
      try {
        const res = await fetch('/api/documents');
        const docs = await res.json();
        window.cachedDocs = docs;
        const listEl = document.getElementById('docList');
        listEl.innerHTML = '';
        if (docs.length === 0) {
          listEl.innerHTML = '<div style="font-size:12px; color:var(--text-muted); padding:8px;">등록된 문서가 없습니다.</div>';
          return;
        }
        docs.forEach(doc => {
          const item = document.createElement('div');
          item.className = 'doc-item';
          item.innerHTML = `
            <div class="doc-icon">📄</div>
            <div class="doc-info" style="flex: 1; min-width: 0;">
              <div class="doc-name" title="${doc.name}" style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-weight: 500;">${doc.name}</div>
              <div class="doc-size" style="font-size: 11px; color: var(--text-muted);">${doc.size_mb} MB${doc.total_pages ? ' · ' + doc.total_pages + 'p' : ''}</div>
            </div>
            <div class="doc-item-actions" style="display: flex; gap: 4px; align-items: center; flex-shrink: 0;">
              <button class="doc-view-btn" title="우측 뷰어에서 원본 문서 열람" onclick="viewDoc('${doc.name}')">열람</button>
              <button class="doc-del-btn" title="보관함에서 내리기 (업로드본만 제거)" onclick="deleteDoc(event, '${doc.name}')">내리기</button>
            </div>
          `;
          listEl.appendChild(item);
        });
      } catch(e) {
        console.error(e);
      }
    }

    async function deleteDoc(event, name) {
      event.stopPropagation();
      const msg = `'${name}' 문서를 보관함에서 내리시겠습니까?

※ 프로젝트 원본 파일은 안전하게 보존되며, 웹 화면(서버)에 업로드된 복사본 파일만 제거되어 디스크 용량이 확보됩니다.`;
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
        <div class="progress-box" style="font-size:12.5px; line-height: 1.6; color: var(--text-color);">
          <div id="step1" style="font-weight:600; color: #0284c7;">⚡ 1단계: 5개 문서 메타데이터 색인 탐색 중...</div>
          <div id="step2" style="color: var(--text-muted); opacity: 0.6;">📂 2단계: 최적 출처 문서 매칭 및 핵심 섹션 정밀 발췌 대기</div>
          <div id="step3" style="color: var(--text-muted); opacity: 0.6;">🤖 3단계: 수석 엔지니어 AI 도표/제원 정밀 분석 대기</div>
        </div>
      `);

      const t1 = setTimeout(() => {
        const s1 = document.getElementById('step1');
        const s2 = document.getElementById('step2');
        if (s1 && s2) {
          s1.innerHTML = '✅ 1단계: 5개 문서 메타데이터 색인 탐색 완료 (0.002s)';
          s1.style.color = '#15803d';
          s2.innerHTML = '📂 2단계: 최적 문서 핵심 섹션 정밀 발췌 완료 (초고속 슬라이싱)';
          s2.style.fontWeight = '600';
          s2.style.color = '#0284c7';
          s2.style.opacity = '1.0';
        }
      }, 700);

      const t2 = setTimeout(() => {
        const s2 = document.getElementById('step2');
        const s3 = document.getElementById('step3');
        if (s2 && s3) {
          s2.innerHTML = '✅ 2단계: 최적 출처 문서 핵심 섹션 발췌 완료';
          s2.style.color = '#15803d';
          s3.innerHTML = '<span class="loading-spinner"></span> 3단계: Gemini 고속 멀티모달 AI 분석 중...';
          s3.style.fontWeight = '600';
          s3.style.color = '#2563eb';
          s3.style.opacity = '1.0';
        }
      }, 1500);

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
        clearTimeout(t2);

        const data = await res.json();
        if (data.error) {
          if (botMsgDiv) botMsgDiv.innerHTML = `<span style="color:#ef4444;">⚠️ 오류: ${data.error}</span>`;
        } else {
          let parsedHtml = marked.parse(data.reply);
          parsedHtml = linkifyPageNumbers(parsedHtml);
          if (botMsgDiv) botMsgDiv.innerHTML = parsedHtml;
          parsedHtml = linkifyPageNumbers(parsedHtml);
          botMsgDiv.innerHTML = parsedHtml;

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
  