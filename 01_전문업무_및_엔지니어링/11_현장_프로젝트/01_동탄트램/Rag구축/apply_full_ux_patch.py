import re
import sys

target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(target_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS: remove .doc-item.active and style .doc-view-btn
old_css_part = """.doc-item {
      padding: 10px 12px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      font-size: 13px;
      display: flex;
      align-items: center;
      gap: 10px;
      cursor: pointer;
      transition: all 0.15s;
      box-shadow: var(--card-shadow);
    }
    .doc-item:hover {
      border-color: var(--accent);
      background: var(--bot-msg-bg);
    }"""

new_css_part = """.doc-item {
      padding: 10px 12px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      font-size: 13px;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.15s;
      box-shadow: var(--card-shadow);
    }
    .doc-item:hover {
      border-color: #cbd5e1;
      background: var(--bot-msg-bg);
    }
    .doc-view-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 3px 8px;
      border-radius: 4px;
      border: 1px solid #bfdbfe;
      background: #eff6ff;
      color: #2563eb;
      cursor: pointer;
      font-size: 11px;
      font-weight: 600;
      transition: all 0.15s;
      flex-shrink: 0;
    }
    .doc-view-btn:hover {
      background: #2563eb;
      color: #ffffff;
      border-color: #2563eb;
    }"""

if old_css_part in content:
    content = content.replace(old_css_part, new_css_part)
    print("CSS updated successfully")
else:
    print("Warning: old CSS part not exact match")

# 2. Update initial bot greeting message
old_greeting = """<div class="message bot">
              <div class="avatar bot">🤖</div>
              <div class="message-content">
                <strong>현장 기술보고서 및 시방서 AI 어시스턴트입니다.</strong><br><br>
                왼쪽 보관함에서 질의할 <strong>PDF 문서를 선택</strong>한 뒤 질문을 입력하세요.<br>
                • 오른쪽 공간에서 <strong>출처 원본 PDF를 실시간으로 확인하고 다운로드</strong>할 수 있습니다.<br>
                • 문서를 쪼개지 않고 <strong>수백 페이지 원본 전체를 한 번에 스캔</strong>하여 표, 제원, 수식을 100% 원문 그대로 분석합니다.<br>
                • 상단 <strong>[🌐 지반·공종 지식 그래프]</strong> 탭을 누르면, 조사보고서와 설계보고서 간의 <strong>정합성 및 상충(불일치) 위험 관계망</strong>을 직접 눈으로 시각화할 수 있습니다!
              </div>
            </div>"""

new_greeting = """<div class="message bot">
              <div class="avatar bot">🤖</div>
              <div class="message-content">
                <strong>⚡ 동탄트램 통합 지능형 색인 RAG 어시스턴트입니다.</strong><br><br>
                문서를 일일이 선택하실 필요가 전혀 없습니다! 아래 질문창에 궁금하신 기술 사항을 바로 입력하세요.<br>
                • <strong>전체 문서 자동 색인:</strong> 시추주상도(1·2공구), 토질 증빙자료, 기술제안서, 비탈면 안정성 검토 등 보관소 내 모든 문서를 AI가 실시간으로 분석하여 <strong>최적의 출처 문서와 해당 페이지를 스스로 찾아내어 답변</strong>합니다.<br>
                • <strong>실시간 출처 뷰어 연동:</strong> AI가 답변을 작성함과 동시에 <strong>오른쪽 뷰어에 해당 원본 문서와 페이지가 자동으로 열려</strong> 원문을 즉시 검증 및 다운로드할 수 있습니다.<br>
                • 언제든 왼쪽 보관함의 <strong>[열람]</strong> 버튼을 누르면 원하시는 문서를 뷰어에서 직접 확인하실 수도 있습니다.
              </div>
            </div>"""

if old_greeting in content:
    content = content.replace(old_greeting, new_greeting)
    print("Greeting updated successfully")
else:
    print("Warning: old greeting not exact match")

# 3. Update JavaScript logic (fetchDocs, selectDoc, loadViewerDoc, sendQuery, downloadActiveDoc, etc.)
js_start_marker = "async function fetchDocs() {"
js_end_marker = "function scrollToBottom() {"

js_start = content.find(js_start_marker)
js_end = content.find(js_end_marker)

if js_start == -1 or js_end == -1:
    print(f"JS markers not found: {js_start}, {js_end}")
    sys.exit(1)

new_js = """async function fetchDocs() {
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
      const msg = `'${name}' 문서를 보관함에서 내리시겠습니까?\\n\\n※ 프로젝트 원본 파일은 안전하게 보존되며, 웹 화면(서버)에 업로드된 복사본 파일만 제거되어 디스크 용량이 확보됩니다.`;
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

    function loadViewerDoc(name, targetPage) {
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

      if (docObj && docObj.sections && docObj.sections.length > 0 && pillsContainer) {
        pillsContainer.innerHTML = '';
        docObj.sections.slice(0, 12).forEach(sec => {
          const pill = document.createElement('button');
          pill.className = 'page-pill';
          const shortTitle = sec.title.replace(' 시추주상도', '').replace(' 구조계산서', '');
          pill.innerText = `${shortTitle} (p.${sec.start_page})`;
          pill.title = `${sec.title} (p.${sec.start_page}~${sec.end_page})`;
          pill.onclick = () => jumpToPage(sec.start_page);
          pillsContainer.appendChild(pill);
        });
        if (pageBar) pageBar.style.display = 'flex';
      } else if (pageBar) {
        pageBar.style.display = 'none';
      }

      const pageParam = targetPage ? `#page=${targetPage}` : '#page=1';
      if (iframe) {
        iframe.src = `/api/view?document=${encodeURIComponent(name)}${pageParam}`;
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
        iframe.src = `/api/view?document=${encodeURIComponent(currentViewingDoc)}#page=${pageNum}`;
      }
    }

    function jumpToDirectPage() {
      const input = document.getElementById('pageJumpInput');
      if (!input) return;
      const val = parseInt(input.value);
      if (val && val > 0) {
        jumpToPage(val);
        input.value = '';
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
      window.open(`/api/view?document=${encodeURIComponent(currentViewingDoc)}`, '_blank');
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

    async function sendQuery() {
      const input = document.getElementById('promptInput');
      const query = input.value.trim();
      const apiKey = document.getElementById('apiKeyInput').value.trim();

      if (!query) return;
      if (!apiKey) {
        alert('우측 상단에 Gemini API Key를 입력해 주세요 (Google AI Studio에서 발급)');
        return;
      }

      appendMessage('user', query);
      input.value = '';

      const sendBtn = document.getElementById('sendBtn');
      sendBtn.disabled = true;
      sendBtn.innerHTML = '<span class="loading-spinner"></span> 색인 탐색 & 분석 중...';

      const botMsgDiv = appendMessage('bot', '<em>전체 문서 색인을 탐색하여 최적의 출처를 분석 중입니다 (수초 소요)...</em>');

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            api_key: apiKey,
            query: query
          })
        });

        const data = await res.json();
        if (data.error) {
          botMsgDiv.innerHTML = `<span style="color:#ef4444;">⚠️ 오류: ${data.error}</span>`;
        } else {
          botMsgDiv.innerHTML = marked.parse(data.reply);

          // 자동 탐색된 출처 문서와 우측 뷰어 실시간 연동
          if (data.source_document) {
            currentViewingDoc = data.source_document;
            loadViewerDoc(data.source_document, data.source_page || 1);
            toggleViewerPanel(true);

            const topRef = document.getElementById('topSourceRef');
            if (topRef) {
              const secInfo = data.matched_sections && data.matched_sections.length > 0 ? ` (${data.matched_sections[0]})` : ` (p.${data.source_page || 1})`;
              topRef.innerHTML = `📂 <b>자동 탐색 출처:</b> <span style="color:var(--text-color); font-weight:600;">${data.source_document}</span>${secInfo}`;
            }
            const topDlBtn = document.getElementById('topDownloadBtn');
            if (topDlBtn) topDlBtn.style.display = 'inline-flex';
          }
        }
      } catch (err) {
        botMsgDiv.innerHTML = `<span style="color:#ef4444;">⚠️ 서버 통신 오류: ${err.message}</span>`;
      } finally {
        sendBtn.disabled = false;
        sendBtn.innerText = '전송';
        scrollToBottom();
      }
    }

    """

content = content[:js_start] + new_js + content[js_end:]
print("JavaScript updated successfully")

with open(target_path, "w", encoding="utf-8") as f:
    f.write(content)

print("All updates saved into server.py")
