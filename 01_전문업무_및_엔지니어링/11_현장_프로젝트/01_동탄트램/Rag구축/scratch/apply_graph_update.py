import re
from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

print(f"Original server.py length: {len(content)} chars")

# 1. CSS 추가
css_to_add = """
    /* GraphRAG Custom UI */
    .graph-toolbar {
      position: absolute;
      top: 14px;
      left: 16px;
      z-index: 10;
      display: flex;
      align-items: center;
      gap: 6px;
      background: var(--bg-card);
      padding: 6px 12px;
      border-radius: 8px;
      border: 1px solid var(--border-color);
      box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .filter-chip {
      padding: 5px 11px;
      font-size: 12px;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      background: var(--bg-main);
      color: var(--text-main);
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .filter-chip:hover {
      border-color: var(--accent);
      color: var(--accent);
    }
    .filter-chip.active {
      background: var(--accent);
      color: #fff !important;
      border-color: var(--accent);
      font-weight: 600;
    }
    .filter-chip-risk.active {
      background: #ef4444 !important;
      border-color: #ef4444 !important;
      color: #fff !important;
    }
    .graph-loading {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(255, 255, 255, 0.7);
      backdrop-filter: blur(2px);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 12px;
      z-index: 20;
    }
    [data-theme="dark"] .graph-loading {
      background: rgba(15, 23, 42, 0.75);
    }
    .borehole-jump-btn {
      margin-top: 10px;
      padding: 8px 12px;
      background: var(--accent);
      color: #fff;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 12px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      width: 100%;
      transition: background 0.15s;
    }
    .borehole-jump-btn:hover {
      filter: brightness(1.1);
    }
"""

if ".graph-toolbar" not in content:
    content = content.replace("/* Graph View */", css_to_add + "\n    /* Graph View */")
    print("CSS added.")

# 2. HTML: graph-canvas-area 에 toolbar 및 loading overlay 추가
canvas_area_old = """        <div class="graph-canvas-area">
          <div id="networkCanvas"></div>
        </div>"""

canvas_area_new = """        <div class="graph-canvas-area">
          <div class="graph-toolbar">
            <span style="font-size: 12px; font-weight: 600; color: var(--text-muted); margin-right: 4px;">구간 필터:</span>
            <button class="filter-chip active" onclick="applyGraphFilter('all', false, this)">전체 현장 (72공)</button>
            <button class="filter-chip" onclick="applyGraphFilter('depot', false, this)">차량기지 (GB)</button>
            <button class="filter-chip" onclick="applyGraphFilter('1', false, this)">1공구 본선 (NH)</button>
            <button class="filter-chip" onclick="applyGraphFilter('2', false, this)">2공구 본선 (DT)</button>
            <button class="filter-chip filter-chip-risk" onclick="applyGraphFilter('all', true, this)">⚠️ 연약층 위험구간 (25공)</button>
          </div>
          <div id="graphLoadingOverlay" class="graph-loading" style="display:none;">
            <div class="loading-spinner" style="width:28px; height:28px; border-width:3px;"></div>
            <div style="font-size: 13px; font-weight: 600; color: var(--text-main);">지반-공종 지식 그래프 로딩 중...</div>
          </div>
          <div id="networkCanvas"></div>
        </div>"""

if "graph-toolbar" not in content and canvas_area_old in content:
    content = content.replace(canvas_area_old, canvas_area_new)
    print("Canvas Area Toolbar added.")

# 3. JavaScript: switchTab 개선
old_switch_graph = """        document.querySelector('.tab-btn:nth-child(2)').classList.add('active');
        document.getElementById('graphTab').classList.add('active');
        if (network) {
          setTimeout(() => network.fit(), 200);
        }"""

new_switch_graph = """        document.querySelector('.tab-btn:nth-child(2)').classList.add('active');
        document.getElementById('graphTab').classList.add('active');
        if (!hasLoadedMasterGraph) {
          loadMasterGraph();
        } else if (network) {
          setTimeout(() => network.fit(), 200);
        }"""

if old_switch_graph in content:
    content = content.replace(old_switch_graph, new_switch_graph)
    print("switchTab updated to auto-load graph.")

# 4. JavaScript: loadMasterGraph, applyGraphFilter, openBoreholePdf 함수 및 extractGraph 보강
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
          document.getElementById('summaryBox').style.display = 'block';
          document.getElementById('summaryContent').innerText = data.summary;
        }
        if (data.discrepancies && data.discrepancies.length > 0) {
          document.getElementById('discrepancyBox').style.display = 'block';
          document.getElementById('discrepancyContent').innerHTML = data.discrepancies.slice(0, 15).map(d => `• ${d}`).join('<br>') + (data.discrepancies.length > 15 ? `<br><small style="color:var(--text-muted);">외 ${data.discrepancies.length - 15}건 생략</small>` : '');
        } else {
          document.getElementById('discrepancyBox').style.display = 'none';
        }

      } catch (err) {
        console.error('loadMasterGraph error:', err);
      } finally {
        if (overlay) overlay.style.display = 'none';
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = '⚡ 지식 그래프 재분석 / 새로고침';
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
      // 문서 로드 및 페이지 점프
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

if "hasLoadedMasterGraph" not in content:
    content = content.replace("/* GraphRAG Extraction */", js_to_insert + "\n    /* GraphRAG Extraction */")
    print("Graph Master JS functions inserted.")

# 5. renderNetwork 클릭 이벤트에 PDF 바로가기 버튼 및 노드 속성 연동
old_click_handler = """      network.on("click", function (params) {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0];
          const nodeData = nodes.get(nodeId);
          document.getElementById('nodeDetailBox').style.display = 'block';
          document.getElementById('nodeDetailLabel').innerText = `[${nodeData.rawType}] ${nodeData.label}`;
          document.getElementById('nodeDetailDesc').innerText = nodeData.rawDesc || `ID: ${nodeData.id}`;
        }
      });"""

new_click_handler = """      network.on("click", function (params) {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0];
          const nodeData = nodes.get(nodeId);
          const raw = rawNodes.find(n => n.id === nodeId) || {};
          document.getElementById('nodeDetailBox').style.display = 'block';
          document.getElementById('nodeDetailLabel').innerText = `[${nodeData.rawType}] ${nodeData.label}`;
          
          let descHtml = (nodeData.rawDesc || `ID: ${nodeData.id}`).replace(/\\n/g, '<br>');
          
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
      });"""

if old_click_handler in content:
    content = content.replace(old_click_handler, new_click_handler)
    print("renderNetwork click handler upgraded.")

# 6. do_GET에 /api/graph/master 엔드포인트 추가
old_doget_branch = """        elif self.path.startswith("/api/download") or self.path.startswith("/api/view"):"""

new_doget_branch = """        elif self.path.startswith("/api/graph/master"):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            section = params.get("section", [None])[0]
            risk_only = params.get("risk_only", ["false"])[0].lower() in ("true", "1")
            try:
                import graph_engine
                data = graph_engine.build_master_graph(section=section, risk_only=risk_only)
                self.respond_json(data)
            except Exception as e:
                self.respond_json({"error": str(e)}, 500)

        elif self.path.startswith("/api/download") or self.path.startswith("/api/view"):"""

if "/api/graph/master" not in content and old_doget_branch in content:
    content = content.replace(old_doget_branch, new_doget_branch)
    print("do_GET /api/graph/master endpoint added.")

# 7. extractGraph 버튼 텍스트 변경
content = content.replace("onclick=\"extractGraph()\">", "onclick=\"loadMasterGraph(currentGraphFilter.section, currentGraphFilter.riskOnly)\">")

server_path.write_text(content, encoding="utf-8")
print(f"Updated server.py successfully! New length: {len(content)} chars")
