# -*- coding: utf-8 -*-
"""
지식망 탐색 경로 원클릭 시각화 (Graph Path Highlight & Focus) 통합 스크립트
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

# 1. CSS 추가: 하이라이트 버튼 및 복원 칩
new_css = """
    /* Graph Path Highlight Button & Toolbar */
    .trace-graph-view-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      font-size: 11.5px;
      font-weight: 600;
      color: #fff;
      background: linear-gradient(135deg, #4f46e5 0%, #0284c7 100%);
      border: none;
      border-radius: 6px;
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(79, 70, 229, 0.3);
      transition: all 0.2s ease;
    }
    .trace-graph-view-btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(79, 70, 229, 0.45);
      filter: brightness(1.1);
    }
    .graph-reset-chip {
      padding: 5px 11px;
      font-size: 12px;
      font-weight: 600;
      border: 1px solid #4f46e5;
      border-radius: 6px;
      background: #4f46e5;
      color: #fff;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      animation: pulseHighlight 2s infinite;
    }
    @keyframes pulseHighlight {
      0%, 100% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.6); }
      50% { box-shadow: 0 0 0 8px rgba(79, 70, 229, 0); }
    }
"""

if ".trace-graph-view-btn" not in content:
    content = content.replace("/* Reasoning Trace Accordion & Timeline UI */", new_css + "\n    /* Reasoning Trace Accordion & Timeline UI */")
    print("1. Highlight Button CSS added.")

# 2. JS: renderNetwork에 원본 데이터 캐싱 및 highlightGraphPath, resetGraphHighlight 함수 추가
new_js_functions = """
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
        targetIds = typeof targetNodeIdsJson === 'string' ? JSON.parse(targetNodeIdsJson) : targetNodeIdsJson;
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
"""

if "function highlightGraphPath" not in content:
    content = content.replace("function toggleTrace(el) {", new_js_functions + "\n    function toggleTrace(el) {")
    print("2. highlightGraphPath and resetGraphHighlight functions added.")

# 3. renderNetwork 내부에서 원본 데이터 캐싱 저장
old_rendernetwork_start = """function renderNetwork(rawNodes, rawEdges) {
      const container = document.getElementById('networkCanvas');"""

new_rendernetwork_start = """function renderNetwork(rawNodes, rawEdges) {
      originalRawNodes = rawNodes;
      originalRawEdges = rawEdges;
      const container = document.getElementById('networkCanvas');"""

if old_rendernetwork_start in content:
    content = content.replace(old_rendernetwork_start, new_rendernetwork_start)
    print("3. rawNodes cached in renderNetwork.")

old_network_assign = """      if (network) network.destroy();
      network = new vis.Network(container, data, options);"""

new_network_assign = """      if (network) network.destroy();
      network = new vis.Network(container, data, options);
      window.masterGraphDataSets = { nodes, edges };"""

if old_network_assign in content:
    content = content.replace(old_network_assign, new_network_assign)
    print("4. window.masterGraphDataSets stored.")

# 4. buildTraceHtml에 [🌐 이 답변에 쓰인 지식망 경로 보기] 버튼 추가
old_trace_body_end = """          <div class="trace-body" style="display:none;">
            <div class="trace-timeline">
              ${stepsHtml}
            </div>
          </div>"""

new_trace_body_end = """          <div class="trace-body" style="display:none;">
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
          </div>"""

if old_trace_body_end in content:
    content = content.replace(old_trace_body_end, new_trace_body_end)
    print("5. Highlight button integrated into buildTraceHtml.")

# 5. 백엔드 SQL 및 RAG trace에 highlight_nodes 전달
# SQL 부분
old_sql_trace = """                        sql_res["trace"] = {
                            "query": query,
                            "steps": ["""

new_sql_trace = """                        # SQL 대상 시추공 하이라이트 노드 구성
                        sql_h_nodes = []
                        if "hole_no" in sql_res:
                            sql_h_nodes.append(f"bh_{sql_res['hole_no']}")
                        for h in re.findall(r'(?:NH|DT|GB|NGB)-?\\d+', query, re.IGNORECASE):
                            clean = h.upper().replace(" ", "")
                            if not clean.startswith(("NH-", "DT-", "GB-", "NGB-")):
                                clean = re.sub(r'([A-Z]+)(\\d+)', r'\\1-\\2', clean)
                            sql_h_nodes.append(f"bh_{clean}")
                        if "연약" in query or "n<" in query or "n치" in query:
                            sql_h_nodes.append("risk_cluster_soft")
                        if "지하수" in query:
                            sql_h_nodes.append("risk_cluster_gw")

                        sql_res["trace"] = {
                            "query": query,
                            "highlight_nodes": list(set(sql_h_nodes)),
                            "steps": ["""

if old_sql_trace in content:
    content = content.replace(old_sql_trace, new_sql_trace)
    print("6. SQL trace highlight_nodes integrated.")

# RAG 부분
old_rag_trace_block = """                        rag_trace = {
                            "query": query,
                            "steps": ["""

new_rag_trace_block = """                        # 지식망 하이라이트 타겟 노드 구성
                        rag_h_nodes = [f"bh_{h}" for h in matched_graph_holes]
                        if graph_intel.get("is_soft_ground"):
                            rag_h_nodes.append("risk_cluster_soft")
                        if graph_intel.get("is_high_gw"):
                            rag_h_nodes.append("risk_cluster_gw")
                        if graph_intel.get("is_depot"):
                            rag_h_nodes.extend(["hub_depot", "hub_prop_depot"])
                        if graph_intel.get("is_sec1"):
                            rag_h_nodes.append("hub_sec1")
                        if graph_intel.get("is_sec2"):
                            rag_h_nodes.append("hub_sec2")

                        rag_trace = {
                            "query": query,
                            "highlight_nodes": list(set(rag_h_nodes)),
                            "steps": ["""

if old_rag_trace_block in content:
    content = content.replace(old_rag_trace_block, new_rag_trace_block)
    print("7. RAG trace highlight_nodes integrated.")

# highlightGraphPath URI decode 핸들러 보강
content = content.replace(
    "targetIds = typeof targetNodeIdsJson === 'string' ? JSON.parse(targetNodeIdsJson) : targetNodeIdsJson;",
    "const decoded = typeof targetNodeIdsJson === 'string' ? decodeURIComponent(targetNodeIdsJson) : targetNodeIdsJson;\n        targetIds = typeof decoded === 'string' ? JSON.parse(decoded) : decoded;"
)

server_path.write_text(content, encoding="utf-8")
print("All Graph Highlight & Focus features deployed successfully!")
