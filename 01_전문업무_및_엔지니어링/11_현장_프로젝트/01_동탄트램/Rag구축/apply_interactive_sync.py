import re
import sys

target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(target_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add CSS for page-link-badge and page-pill highlights
css_marker = ".page-pill {"
css_pos = code.find(css_marker)
if css_pos != -1:
    new_css = """.page-link-badge {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      padding: 1px 7px;
      margin: 0 2px;
      border-radius: 4px;
      border: 1px solid #93c5fd;
      background: #eff6ff;
      color: #1d4ed8;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
      vertical-align: middle;
      text-decoration: none;
    }
    .page-link-badge:hover {
      background: #2563eb;
      color: #ffffff;
      border-color: #2563eb;
      transform: translateY(-1px);
      box-shadow: 0 2px 4px rgba(37,99,235,0.25);
    }
    .page-pill.highlight {
      background: #f0fdf4 !important;
      color: #15803d !important;
      border-color: #86efac !important;
      font-weight: 600 !important;
    }
    .page-pill.current {
      background: #2563eb !important;
      color: #ffffff !important;
      border-color: #2563eb !important;
      font-weight: 600 !important;
      box-shadow: 0 0 0 2px rgba(37,99,235,0.2);
    }
    """
    code = code[:css_pos] + new_css + code[css_pos:]
    print("Added CSS for page-link-badge and highlights")

# 2. Update loadViewerDoc, jumpToPage and sendQuery in client JavaScript
old_viewer_start = "function loadViewerDoc(name, targetPage) {"
old_viewer_end = "async function uploadDoc() {"

v_start = code.find(old_viewer_start)
v_end = code.find(old_viewer_end)

if v_start == -1 or v_end == -1:
    print(f"Could not find viewer JS boundaries: {v_start}, {v_end}")
    sys.exit(1)

new_viewer_js = """function linkifyPageNumbers(htmlText) {
      if (!htmlText) return '';
      // Linkify occurrences like p.50, p. 50, p.50~51, 페이지 50, (p.50)
      return htmlText.replace(/(?:p\\.|페이지\\s*)(\\d+)(?:\\s*[~-]\\s*(\\d+))?/gi, (match, p1, p2) => {
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

    """

code = code[:v_start] + new_viewer_js + code[v_end:]
print("Updated viewer JS logic with linkify and smart pills")

# 3. Update sendQuery response handling to use linkifyPageNumbers and pass active_sections
old_query_marker = "botMsgDiv.innerHTML = marked.parse(data.reply);"
new_query_marker = """let parsedHtml = marked.parse(data.reply);
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
          }"""

# Find where data.reply is handled
pos_rep = code.find("botMsgDiv.innerHTML = marked.parse(data.reply);")
if pos_rep != -1:
    # replace until topDlBtn.style.display = 'inline-flex'; }
    end_pattern = "topDlBtn.style.display = 'inline-flex';\n          }"
    pos_end_rep = code.find(end_pattern, pos_rep)
    if pos_end_rep != -1:
        code = code[:pos_rep] + new_query_marker + code[pos_end_rep + len(end_pattern):]
        print("Updated sendQuery marked.parse and linkify integration")

# 4. Update backend resp_data to include active_sections
old_resp_block = """                    resp_data = {
                        "reply": source_notice + text,
                        "source_document": target_doc_name,
                        "source_page": target_start_page,
                        "matched_sections": matched_section_titles
                    }"""

new_resp_block = """                    matched_section_objs = [
                        {
                            "title": s.get("title", ""),
                            "start_page": s.get("start_page", 1),
                            "end_page": s.get("end_page", 1),
                            "section_id": s.get("section_id", "")
                        }
                        for sc, dn, fp, s in scored_sections if dn == target_doc_name
                    ][:10]

                    resp_data = {
                        "reply": source_notice + text,
                        "source_document": target_doc_name,
                        "source_page": target_start_page,
                        "matched_sections": matched_section_titles,
                        "active_sections": matched_section_objs
                    }"""

if old_resp_block in code:
    code = code.replace(old_resp_block, new_resp_block)
    print("Updated backend resp_data with active_sections")
else:
    print("Warning: old_resp_block not matched")

with open(target_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved all changes into server.py")
