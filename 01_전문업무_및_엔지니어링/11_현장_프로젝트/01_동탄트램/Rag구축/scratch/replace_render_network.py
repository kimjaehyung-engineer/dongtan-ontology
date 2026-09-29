# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

SERVER_PATH = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")

with open(SERVER_PATH, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

start_idx = None
end_idx = None

for i, l in enumerate(lines):
    if "function renderNetwork(rawNodes, rawEdges) {" in l:
        start_idx = i
    if start_idx is not None and i > start_idx and l.strip() == "}" and lines[i+1].strip() == "</script>":
        end_idx = i
        break

print(f"renderNetwork found: lines {start_idx+1} to {end_idx+1}")

new_func = """    function renderNetwork(rawNodes, rawEdges) {
      originalRawNodes = rawNodes;
      originalRawEdges = rawEdges;
      const container = document.getElementById('networkCanvas');

      const colorMap = {
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
          rawDesc: n.description || '',
          extra: n.extra || {}
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
      });
    }
"""

new_lines = lines[:start_idx] + [new_func] + lines[end_idx+1:]

with open(SERVER_PATH, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Successfully updated renderNetwork in server.py!")
