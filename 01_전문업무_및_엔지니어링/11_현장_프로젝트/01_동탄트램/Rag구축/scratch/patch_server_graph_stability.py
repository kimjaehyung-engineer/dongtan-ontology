# -*- coding: utf-8 -*-
"""
server.py 지식망 물리 시뮬레이션 안정화 및 툴바·도메인 클러스터 UI 뷰 업그레이드
1. physics: stabilization 완료 시 즉시 physics.enabled=false 처리하여 흔들림/진동 100% 제거
2. 물리 고정/재배치 원클릭 토글 버튼 제공 (⏹️ 물리 고정됨)
3. 툴바에 '관점 모드 (전체 / 지반·시추공 중심 / 9대 기술제안 & 인터페이스)' 추가
4. 시추공 노드를 간결한 원형 dot으로 정돈하고, 9대 기술제안 도메인 노드를 에메랄드 박스로 강조
5. 기술제안 도메인 클릭 시 우측 상세 패널에 과제별 테이블 및 원본 페이지 바로 열람 버튼 표출
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

SERVER_PATH = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")

with open(SERVER_PATH, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# 1. Update toolbar HTML
old_toolbar = '''          <div class="graph-toolbar">
            <span style="font-size: 12px; font-weight: 600; color: var(--text-muted); margin-right: 4px;">구간 필터:</span>
            <button class="filter-chip active" onclick="applyGraphFilter('all', false, this)">전체 현장 (77공)</button>
            <button class="filter-chip" onclick="applyGraphFilter('depot', false, this)">차량기지 전체 (GB+NGB)</button>
            <button class="filter-chip" onclick="applyGraphFilter('prop', false, this)">제안설계 기지 (NGB)</button>
            <button class="filter-chip" onclick="applyGraphFilter('1', false, this)">1공구 본선 (NH)</button>
            <button class="filter-chip" onclick="applyGraphFilter('2', false, this)">2공구 본선 (DT)</button>
            <button class="filter-chip filter-chip-risk" onclick="applyGraphFilter('all', true, this)">⚠️ 연약층 위험구간 (28공)</button>
          </div>'''

new_toolbar = '''          <div class="graph-toolbar" style="display:flex; flex-wrap:wrap; gap:6px; align-items:center;">
            <span style="font-size: 12px; font-weight: 700; color: var(--text-main); margin-right: 2px;">👁️ 관점:</span>
            <button class="filter-chip active" onclick="applyGraphFilter('all', false, this)">🌐 전체 통합</button>
            <button class="filter-chip" onclick="applyGraphFilter('geotech', false, this)">⛏️ 지반·시추공 중심 (77공)</button>
            <button class="filter-chip" onclick="applyGraphFilter('proposals', false, this)">📋 9대 기술제안 & 인터페이스</button>

            <span style="font-size: 12px; font-weight: 700; color: var(--text-main); margin-left: 10px; margin-right: 2px;">📍 구간:</span>
            <button class="filter-chip" onclick="applyGraphFilter('depot', false, this)">차량기지</button>
            <button class="filter-chip" onclick="applyGraphFilter('1', false, this)">1공구(NH)</button>
            <button class="filter-chip" onclick="applyGraphFilter('2', false, this)">2공구(DT)</button>
            <button class="filter-chip filter-chip-risk" onclick="applyGraphFilter('all', true, this)">⚠️ 연약층(28공)</button>

            <div style="flex:1;"></div>
            <button id="freezePhysicsBtn" class="filter-chip active" onclick="togglePhysics(this)" style="font-weight:700; border-color:var(--primary); background:var(--primary); color:#fff;">⏹️ 물리 고정됨 (흔들림 멈춤)</button>
          </div>'''

if old_toolbar in code:
    code = code.replace(old_toolbar, new_toolbar, 1)
    print("SUCCESS: Updated graph-toolbar in server.py")
else:
    print("WARNING: old_toolbar not found!")

# 2. Update renderNetwork & physics
old_render = '''      const colorMap = {
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
      });'''

new_render = '''      const colorMap = {
        'BORING': { background: '#ea580c', border: '#c2410c' },
        'STRATUM': { background: '#a16207', border: '#854d0e' },
        'PARAMETER': { background: '#06b6d4', border: '#0891b2' },
        'DESIGN_ELEMENT': { background: '#2563eb', border: '#1d4ed8' },
        'EQUIPMENT': { background: '#8b5cf6', border: '#7c3aed' },
        'PROPOSAL_HUB': { background: '#7c3aed', border: '#5b21b6' },
        'PROPOSAL_DOMAIN': { background: '#059669', border: '#047857' },
        'SPEC': { background: '#4f46e5', border: '#3730a3' },
        'BOQ': { background: '#0284c7', border: '#0369a1' },
        'RISK': { background: '#ef4444', border: '#dc2626' },
        'DEFAULT': { background: '#64748b', border: '#475569' }
      };

      const nodes = new vis.DataSet(rawNodes.map(n => {
        const col = colorMap[n.type] || colorMap['DEFAULT'];
        let nodeShape = 'dot';
        let nodeSize = 14;
        let fontConf = { color: '#fff', size: 12, face: 'Noto Sans KR' };

        if (n.type === 'PROPOSAL_DOMAIN') {
          nodeShape = 'box';
          nodeSize = 22;
          fontConf = { color: '#fff', size: 12, face: 'Noto Sans KR', bold: true };
        } else if (n.type === 'PROPOSAL_HUB') {
          nodeShape = 'diamond';
          nodeSize = 26;
          fontConf = { color: '#fff', size: 13, face: 'Noto Sans KR', bold: true };
        } else if (n.type === 'DESIGN_ELEMENT') {
          nodeShape = 'ellipse';
          nodeSize = 20;
        } else if (n.type === 'BORING') {
          nodeShape = 'dot';
          nodeSize = 10;
        }

        return {
          id: n.id,
          label: n.label,
          title: n.description || n.label,
          color: { background: col.background, border: col.border, highlight: { background: '#fff', border: col.border } },
          font: fontConf,
          shape: nodeShape,
          size: nodeSize,
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
          enabled: true,
          solver: 'barnesHut',
          barnesHut: {
            gravitationalConstant: -2400,
            centralGravity: 0.25,
            springLength: 90,
            springConstant: 0.04,
            damping: 0.25,
            avoidOverlap: 0.35
          },
          stabilization: {
            enabled: true,
            iterations: 130,
            updateInterval: 25,
            fit: true
          },
          maxVelocity: 25,
          minVelocity: 0.5
        },
        interaction: { hover: true, tooltipDelay: 100, dragNodes: true }
      };

      if (network) network.destroy();
      network = new vis.Network(container, data, options);
      window.masterGraphDataSets = { nodes, edges };

      // [물리 안정화 완료 시 즉각 고정: 흔들림/진동 100% 차단]
      network.once("stabilizationIterationsDone", function () {
        network.setOptions({ physics: { enabled: false } });
        const fBtn = document.getElementById('freezePhysicsBtn');
        if (fBtn) {
          fBtn.innerHTML = '⏹️ 물리 고정됨 (흔들림 멈춤)';
          fBtn.style.background = 'var(--primary)';
          fBtn.style.color = '#fff';
        }
      });

      network.on("click", function (params) {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0];
          const nodeData = nodes.get(nodeId);
          const raw = rawNodes.find(n => n.id === nodeId) || {};
          document.getElementById('nodeDetailBox').style.display = 'block';
          document.getElementById('nodeDetailLabel').innerText = `[${nodeData.rawType}] ${nodeData.label}`;
          
          let descHtml = (nodeData.rawDesc || `ID: ${nodeData.id}`).split('\\n').join('<br>');
          
          if (raw.type === 'PROPOSAL_DOMAIN') {
            const extraProps = raw.extra || {};
            const items = extraProps.items || [];
            if (items.length > 0) {
              descHtml += `<div style="margin-top:14px; border-top:1px solid var(--border-color); padding-top:10px;">
                <div style="font-weight:700; font-size:13px; margin-bottom:8px; color:var(--text-main);">📑 세부 제안과제 목록 (${items.length}건):</div>
                <div style="max-height:240px; overflow-y:auto; border:1px solid var(--border-color); border-radius:6px; background:var(--bg-card, #f8fafc);">
                  <table style="width:100%; border-collapse:collapse; font-size:11px;">
                    <tbody>`;
              items.forEach((item, idx) => {
                descHtml += `
                  <tr style="border-bottom:1px solid var(--border-subtle); padding:6px;">
                    <td style="padding:6px; font-weight:700; color:var(--primary); white-space:nowrap;">${item.task_id || ('과제' + (idx+1))}</td>
                    <td style="padding:6px; line-height:1.4;">${item.title || ''}</td>
                    <td style="padding:6px; text-align:right; white-space:nowrap;">
                      <button class="borehole-jump-btn" style="padding:2px 8px; font-size:10px; margin:0;" onclick="openBoreholePdf('${extraProps.doc_name}', ${item.start_page})">p.${item.start_page} 열기</button>
                    </td>
                  </tr>`;
              });
              descHtml += `</tbody></table></div></div>`;
            }
          } else if (raw.type === 'BORING' && raw.doc_name && raw.page) {
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
      });'''

if old_render in code:
    code = code.replace(old_render, new_render, 1)
    print("SUCCESS: Updated renderNetwork in server.py")
else:
    print("WARNING: old_render not found!")

# 3. Add togglePhysics helper function
toggle_func = '''    function togglePhysics(btn) {
      if (!network) return;
      const isEnabled = network.physics.physicsEnabled;
      if (isEnabled) {
        network.setOptions({ physics: { enabled: false } });
        if (btn) {
          btn.innerHTML = '⏹️ 물리 고정됨 (흔들림 멈춤)';
          btn.style.background = 'var(--primary)';
          btn.style.color = '#fff';
        }
      } else {
        network.setOptions({ physics: { enabled: true } });
        if (btn) {
          btn.innerHTML = '▶️ 물리 재배치 중...';
          btn.style.background = 'var(--accent-orange, #ea580c)';
          btn.style.color = '#fff';
        }
        setTimeout(() => {
          network.setOptions({ physics: { enabled: false } });
          if (btn) {
            btn.innerHTML = '⏹️ 물리 고정됨 (흔들림 멈춤)';
            btn.style.background = 'var(--primary)';
            btn.style.color = '#fff';
          }
        }, 2500);
      }
    }
'''

if "function togglePhysics(btn)" not in code:
    anchor = "    function applyGraphFilter(section, riskOnly, btn) {"
    if anchor in code:
        code = code.replace(anchor, toggle_func + "\n" + anchor, 1)
        print("SUCCESS: Injected togglePhysics function in server.py")
    else:
        print("WARNING: applyGraphFilter anchor not found!")

with open(SERVER_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved updated server.py successfully!")
