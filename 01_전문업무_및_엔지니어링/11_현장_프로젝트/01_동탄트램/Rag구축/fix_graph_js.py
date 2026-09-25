# -*- coding: utf-8 -*-
import sys
from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

js_to_insert = """
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
"""

if "function loadMasterGraph" not in content:
    target = "/* GraphRAG Extraction */"
    if target in content:
        content = content.replace(target, js_to_insert + "\n    " + target)
        server_path.write_text(content, encoding="utf-8")
        print("Successfully injected loadMasterGraph and helper JS functions into server.py!")
    else:
        print("Target comment /* GraphRAG Extraction */ not found!")
else:
    print("function loadMasterGraph is already in server.py!")
