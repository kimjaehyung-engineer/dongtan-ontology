
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
        if (network) {
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
        const listEl = document.getElementById('docList');
        listEl.innerHTML = '';
        if (docs.length === 0) {
          listEl.innerHTML = '<div style="font-size:12px; color:var(--text-muted); padding:8px;">등록된 문서가 없습니다.</div>';
          return;
        }
        docs.forEach((doc, idx) => {
          const item = document.createElement('div');
          item.className = 'doc-item' + (doc.name === activeDoc || (!activeDoc && idx === 0) ? ' active' : '');
          item.innerHTML = `
            <div class="doc-icon">📄</div>
            <div class="doc-info">
              <div class="doc-name" title="${doc.name}">${doc.name}</div>
              <div class="doc-size">${doc.size_mb} MB</div>
            </div>
            <button class="doc-del-btn" title="보관함에서 내리기 (업로드본만 제거)" onclick="deleteDoc(event, '${doc.name}')">내리기</button>
          `;
          item.onclick = () => selectDoc(doc.name);
          listEl.appendChild(item);
          if (!activeDoc && idx === 0) {
            selectDoc(doc.name);
          }
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
          if (activeDoc === name) {
            activeDoc = null;
            const titleEl = document.getElementById('activeDocTitle');
            if (titleEl) titleEl.innerText = '문서를 선택하세요';
          }
          await fetchDocs();
        } else {
          alert('내리기 실패: ' + (data.error || '오류 발생'));
        }
      } catch(e) {
        alert('서버 요청 중 오류: ' + e);
      }
    }
      try {
        const res = await fetch('/api/delete', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ document: name })
        });
        const data = await res.json();
        if (res.ok) {
          if (activeDoc === name) {
            activeDoc = null;
            const titleEl = document.getElementById('activeDocTitle');
            if (titleEl) titleEl.innerText = '문서를 선택하세요';
          }
          await fetchDocs();
        } else {
          alert('삭제 실패: ' + (data.error || '오류 발생'));
        }
      } catch(e) {
        alert('삭제 요청 중 오류가 발생했습니다: ' + e);
      }
    }

    function selectDoc(name) {
      activeDoc = name;
      document.getElementById('activeDocTitle').innerText = name;
      document.querySelectorAll('.doc-item').forEach(el => {
        el.classList.toggle('active', el.querySelector('.doc-name').innerText === name);
      });
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
          } else {
            console.error('업로드 응답 에러:', file.name, res.status);
          }
        } catch (e) {
          console.error('업로드 통신 오류:', file.name, e);
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
        selectDoc(lastUploadedName);
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

    async function sendQuery() {
      const input = document.getElementById('promptInput');
      const query = input.value.trim();
      const apiKey = document.getElementById('apiKeyInput').value.trim();

      if (!query) return;
      if (!activeDoc) {
        alert('왼쪽 보관함에서 문서를 먼저 선택하세요.');
        return;
      }
      if (!apiKey) {
        alert('우측 상단에 Gemini API Key를 입력해 주세요 (Google AI Studio에서 발급)');
        return;
      }

      appendMessage('user', query);
      input.value = '';

      const sendBtn = document.getElementById('sendBtn');
      sendBtn.disabled = true;
      sendBtn.innerHTML = '<span class="loading-spinner"></span> 분석 중...';

      const botMsgDiv = appendMessage('bot', '<em>문서 전체를 스캔하여 분석 중입니다 (수초 소요)...</em>');

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            api_key: apiKey,
            document: activeDoc,
            query: query
          })
        });

        const data = await res.json();
        if (data.error) {
          botMsgDiv.innerHTML = `<span style="color:#ef4444;">⚠️ 오류: ${data.error}</span>`;
        } else {
          botMsgDiv.innerHTML = marked.parse(data.reply);
        }
      } catch (err) {
        botMsgDiv.innerHTML = `<span style="color:#ef4444;">⚠️ 서버 통신 오류: ${err.message}</span>`;
      } finally {
        sendBtn.disabled = false;
        sendBtn.innerText = '전송';
        scrollToBottom();
      }
    }

    function appendMessage(role, text) {
      const chatBody = document.getElementById('chatBody');
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
      chatBody.scrollTop = chatBody.scrollHeight;
    }

    function escapeHtml(str) {
      return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    /* GraphRAG Extraction */
    async function extractGraph() {
      const apiKey = document.getElementById('apiKeyInput').value.trim();
      if (!apiKey) {
        alert('우측 상단에 Gemini API Key를 먼저 입력해 주세요.');
        return;
      }
      if (!activeDoc) {
        alert('왼쪽 보관함에서 분석할 문서를 먼저 선택하세요.');
        return;
      }

      const btn = document.getElementById('extractBtn');
      btn.disabled = true;
      btn.innerHTML = '<span class="loading-spinner"></span> 지반·공종 관계망 분석 중...';

      try {
        const res = await fetch('/api/extract-graph', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            api_key: apiKey,
            document: activeDoc
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
          document.getElementById('nodeDetailBox').style.display = 'block';
          document.getElementById('nodeDetailLabel').innerText = `[${nodeData.rawType}] ${nodeData.label}`;
          document.getElementById('nodeDetailDesc').innerText = nodeData.rawDesc || `ID: ${nodeData.id}`;
        }
      });
    }
  