import os

target_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'
dist_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\index.html'

html_code = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>동탄트램 Time-Chainage & 예정공정표 대시보드 (통합 뷰어)</title>
  <style>
    :root {
      --primary: #3b82f6;
      --bg: #0f172a;
      --panel-bg: #1e293b;
      --panel-border: #334155;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      width: 100vw; height: 100vh;
      background-color: var(--bg);
      color: var(--text-main);
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      overflow: hidden;
    }
    .app-header {
      height: 52px; background: #090d16;
      border-bottom: 1px solid var(--panel-border);
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 1.25rem; font-weight: 700;
    }
    .app-title { font-size: 1.1rem; color: #60a5fa; display: flex; align-items: center; gap: 8px; }
    .header-badge { font-size: 0.72rem; background: #1e3a5f; color: #93c5fd; padding: 2px 8px; border-radius: 4px; border: 1px solid #3b82f640; }
    
    .app-layout {
      height: calc(100vh - 52px);
      display: flex; width: 100vw;
    }
    .sidebar {
      width: 360px; background: var(--panel-bg);
      border-right: 1px solid var(--panel-border);
      display: flex; flex-direction: column; overflow-y: auto; padding: 1rem; gap: 0.75rem;
    }
    .sidebar-title { font-size: 0.95rem; font-weight: 700; color: #e2e8f0; display: flex; justify-content: space-between; align-items: center; }
    
    .wbs-list { display: flex; flex-direction: column; gap: 8px; }
    .wbs-card {
      background: #0f172a; border: 1px solid #334155; border-radius: 6px;
      padding: 0.75rem 0.9rem; font-size: 0.85rem; cursor: pointer; transition: all 0.15s;
    }
    .wbs-card:hover { border-color: var(--primary); background: #1e293b; }
    .wbs-card.active { border-color: #60a5fa; background: #1e3a5f; }
    .wbs-header { display: flex; justify-content: space-between; align-items: center; font-weight: 700; }
    .wbs-code { font-size: 0.72rem; color: #94a3b8; background: #334155; padding: 2px 6px; border-radius: 4px; }
    .wbs-desc { margin-top: 6px; color: #94a3b8; font-size: 0.78rem; line-height: 1.3; }

    .main-view {
      flex: 1; display: flex; flex-direction: column; padding: 1rem; gap: 1rem; background: #090d16;
    }
    .chart-panel {
      flex: 1; background: var(--panel-bg); border: 1px solid var(--panel-border);
      border-radius: 8px; display: flex; flex-direction: column; padding: 1rem; position: relative; min-height: 0;
    }
    .chart-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
    .chart-title { font-size: 0.95rem; font-weight: 700; color: #f1f5f9; }
    .chart-legend { display: flex; gap: 14px; font-size: 0.78rem; flex-wrap: wrap; }
    .legend-item { display: flex; align-items: center; gap: 6px; }
    .legend-dot { width: 12px; height: 12px; border-radius: 3px; }

    .svg-container { flex: 1; width: 100%; height: 100%; position: relative; min-height: 0; }
    svg { width: 100%; height: 100%; display: block; }
    
    .tooltip-box {
      position: absolute; pointer-events: none; display: none;
      background: rgba(15, 23, 42, 0.95); border: 1px solid #38bdf8;
      border-radius: 6px; padding: 10px 14px; font-size: 0.8rem;
      box-shadow: 0 4px 14px rgba(0,0,0,0.6); z-index: 100; color: #f8fafc;
      line-height: 1.4;
    }

    .info-bar {
      height: 42px; background: var(--panel-bg); border: 1px solid var(--panel-border);
      border-radius: 6px; display: flex; align-items: center; padding: 0 1.25rem; gap: 24px; font-size: 0.82rem;
    }
    .info-stat { color: #94a3b8; }
    .info-stat b { color: #38bdf8; }
  </style>
</head>
<body>
  <header class="app-header">
    <div class="app-title">
      ⚡ 동탄도시철도 트램 Time-Chainage & 예정공정표 통합 대시보드
      <span class="header-badge">1공구 / 2공구 실시간 연동</span>
    </div>
    <div style="font-size:0.78rem; color:#94a3b8;">
      시공구간: 병점역 ~ 동탄역 ~ 남동탄 (총 34개 정거장)
    </div>
  </header>

  <div class="app-layout">
    <!-- 좌측 WBS 및 공종 필터 패널 -->
    <aside class="sidebar">
      <div class="sidebar-title">
        <span>📋 WBS 공정 분류 관리자</span>
        <span style="font-size:0.75rem; color:#60a5fa;">5개 공종 체계</span>
      </div>
      <div class="wbs-list" id="wbs-list"></div>
    </aside>

    <!-- 우측 메인 Time-Chainage 2D 그래프 뷰어 -->
    <main class="main-view">
      <div class="chart-panel">
        <div class="chart-header">
          <div class="chart-title">📈 Time-Chainage 다이어그램 (X축: 정거장 STA / Y축: 시공 기간 Time)</div>
          <div class="chart-legend" id="chart-legend"></div>
        </div>
        <div class="svg-container" id="svg-container">
          <svg id="tc-svg"></svg>
          <div class="tooltip-box" id="tooltip"></div>
        </div>
      </div>

      <div class="info-bar">
        <div class="info-stat">총 정거장 수: <b>34개 역</b></div>
        <div class="info-stat">1공구 시공구간: <b>301역 ~ 201역 (7.8km)</b></div>
        <div class="info-stat">2공구 시공구간: <b>201역 ~ S01/114역 (26.6km)</b></div>
        <div class="info-stat">목표 준공연도: <b>2031년 12월</b></div>
      </div>
    </main>
  </div>

  <script>
    // 정거장 위치 (STA / km) 데이터
    const STATIONS = [
      { id:'301', km:0.0, name:'301(병점역)' },
      { id:'302', km:0.6, name:'302' },
      { id:'303', km:1.2, name:'303' },
      { id:'304', km:1.8, name:'304' },
      { id:'305', km:2.4, name:'305' },
      { id:'306', km:3.0, name:'306' },
      { id:'307', km:3.6, name:'307' },
      { id:'201', km:4.2, name:'201(동탄역)' },
      { id:'202', km:4.8, name:'202' },
      { id:'203', km:5.4, name:'203' },
      { id:'204', km:6.0, name:'204' },
      { id:'205', km:6.6, name:'205' },
      { id:'206', km:7.2, name:'206' },
      { id:'207', km:7.8, name:'207' },
      { id:'208', km:8.4, name:'208' },
      { id:'209', km:9.0, name:'209' },
      { id:'210', km:9.6, name:'210' },
      { id:'S01', km:11.5, name:'S01(망포역)' },
      { id:'S02', km:12.1, name:'S02' },
      { id:'101', km:12.7, name:'101' },
      { id:'102', km:13.3, name:'102' },
      { id:'103', km:13.9, name:'103' },
      { id:'104', km:14.5, name:'104' },
      { id:'105', km:15.1, name:'105' },
      { id:'106', km:15.7, name:'106' },
      { id:'107', km:16.3, name:'107' },
      { id:'108', km:16.9, name:'108' },
      { id:'109', km:17.5, name:'109' },
      { id:'110', km:18.1, name:'110' },
      { id:'111', km:18.7, name:'111' },
      { id:'112', km:19.3, name:'112' },
      { id:'113', km:19.9, name:'113' },
      { id:'114', km:20.5, name:'114' }
    ];

    // WBS 분류 체계
    const WBS_ITEMS = [
      { id:'wbs-1-1', name:'토목/개착공사', color:'#ef4444', desc:'본선 개착 굴착 및 토공사' },
      { id:'wbs-1-2', name:'정거장 구조물', color:'#38bdf8', desc:'34개 정거장 본체 및 개집표기' },
      { id:'wbs-1-3', name:'궤도공사', color:'#22c55e', desc:'자갈/콘크리트 트램 궤도 포설' },
      { id:'wbs-1-4', name:'건축/시스템공사', color:'#eab308', desc:'차량기지 및 종합관리동' },
      { id:'wbs-1-5', name:'전기/신호/통신', color:'#c084fc', desc:'전차선, 트램 신호 및 가공선' }
    ];

    // 공정 라인 및 정거장 블록 데이터
    const ACTIVITIES = [
      { id:'c-1', wbsId:'wbs-1-1', name:'1공구 본선 토목 개착공사', startStn:'301', endStn:'201', startYear:2027.2, endYear:2028.8, color:'#ef4444' },
      { id:'c-2', wbsId:'wbs-1-1', name:'2공구 본선 토목공사', startStn:'201', endStn:'114', startYear:2027.5, endYear:2029.5, color:'#ef4444' },
      { id:'c-3', wbsId:'wbs-1-3', name:'1공구 궤도 포설공사', startStn:'301', endStn:'201', startYear:2028.9, endYear:2029.8, color:'#22c55e' },
      { id:'c-4', wbsId:'wbs-1-3', name:'2공구 궤도 포설공사', startStn:'201', endStn:'114', startYear:2029.5, endYear:2030.7, color:'#22c55e' },
      { id:'c-5', wbsId:'wbs-1-5', name:'본선 전차선/신호 포설', startStn:'301', endStn:'114', startYear:2030.0, endYear:2031.5, color:'#c084fc' }
    ];

    // 정거장 블록 시공 기간 추가
    STATIONS.forEach((st, idx) => {
      const startY = 2028.0 + (idx * 0.08);
      ACTIVITIES.push({
        id: `st-${st.id}`,
        wbsId: 'wbs-1-2',
        name: `${st.name} 정거장 구조물`,
        stnId: st.id,
        km: st.km,
        startYear: startY,
        endYear: startY + 0.5,
        color: '#38bdf8',
        isBlock: true
      });
    });

    const wbsContainer = document.getElementById('wbs-list');
    const legendContainer = document.getElementById('chart-legend');
    const svg = document.getElementById('tc-svg');
    const tooltip = document.getElementById('tooltip');

    // WBS 사이드바 렌더링
    WBS_ITEMS.forEach(wbs => {
      const card = document.createElement('div');
      card.className = 'wbs-card active';
      card.innerHTML = `
        <div class="wbs-header">
          <span>${wbs.name}</span>
          <span class="wbs-code" style="background:${wbs.color}25; color:${wbs.color}; border:1px solid ${wbs.color}60">${wbs.id}</span>
        </div>
        <div class="wbs-desc">${wbs.desc}</div>
      `;
      wbsContainer.appendChild(card);

      const legend = document.createElement('div');
      legend.className = 'legend-item';
      legend.innerHTML = `<div class="legend-dot" style="background:${wbs.color}"></div><span>${wbs.name}</span>`;
      legendContainer.appendChild(legend);
    });

    // 2D SVG Time-Chainage 렌더링
    function renderSVG() {
      const rect = svg.getBoundingClientRect();
      const width = rect.width || 800;
      const height = rect.height || 500;
      
      const padL = 65, padR = 40, padT = 30, padB = 60;
      const graphW = width - padL - padR;
      const graphH = height - padT - padB;

      const minKm = 0.0, maxKm = 21.0;
      const minYr = 2027.0, maxYr = 2032.0;

      const getX = (km) => padL + ((km - minKm) / (maxKm - minKm)) * graphW;
      const getY = (yr) => padT + graphH - ((yr - minYr) / (maxYr - minYr)) * graphH;

      let html = '';

      // Y축 격자 그리드 (시공 연도)
      for (let yr = 2027; yr <= 2032; yr += 0.5) {
        const y = getY(yr);
        html += `<line x1="${padL}" y1="${y}" x2="${width - padR}" y2="${y}" stroke="#334155" stroke-dasharray="3,3" stroke-width="0.7"/>`;
        html += `<text x="${padL - 12}" y="${y + 4}" fill="#94a3b8" font-size="11" text-anchor="end" font-weight="500">${yr.toFixed(1)}년</text>`;
      }

      // X축 격자 그리드 및 정거장 라벨
      STATIONS.forEach((st) => {
        const x = getX(st.km);
        html += `<line x1="${x}" y1="${padT}" x2="${x}" y2="${height - padB}" stroke="#1e293b" stroke-width="1"/>`;
        html += `<text x="${x}" y="${height - padB + 18}" fill="#cbd5e1" font-size="10" text-anchor="end" transform="rotate(-40, ${x}, ${height - padB + 18})">${st.name}</text>`;
      });

      // 공정 라인 및 블록 렌더링
      ACTIVITIES.forEach(act => {
        if (act.isBlock) {
          const x = getX(act.km);
          const y1 = getY(act.startYear);
          const y2 = getY(act.endYear);
          html += `<rect x="${x - 6}" y="${Math.min(y1, y2)}" width="12" height="${Math.abs(y2 - y1)}" fill="${act.color}" opacity="0.85" rx="3" class="act-element" data-title="${act.name}" data-time="${act.startYear.toFixed(1)}년 ~ ${act.endYear.toFixed(1)}년" style="cursor:pointer; transition:opacity 0.2s;"/>`;
        } else {
          const stA = STATIONS.find(s => s.id === act.startStn) || STATIONS[0];
          const stB = STATIONS.find(s => s.id === act.endStn) || STATIONS[STATIONS.length - 1];
          const x1 = getX(stA.km);
          const y1 = getY(act.startYear);
          const x2 = getX(stB.km);
          const y2 = getY(act.endYear);
          html += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${act.color}" stroke-width="5" stroke-linecap="round" class="act-element" data-title="${act.name}" data-time="${act.startYear.toFixed(1)}년 ~ ${act.endYear.toFixed(1)}년" style="cursor:pointer; transition:opacity 0.2s;"/>`;
        }
      });

      svg.innerHTML = html;

      // 마우스 툴팁 이벤트
      document.querySelectorAll('.act-element').forEach(el => {
        el.addEventListener('mouseenter', (e) => {
          tooltip.style.display = 'block';
          tooltip.innerHTML = `<strong>${e.target.dataset.title}</strong><br><span style="color:#38bdf8">시공기간: ${e.target.dataset.time}</span>`;
          el.style.opacity = '1';
        });
        el.addEventListener('mousemove', (e) => {
          const cRect = svg.getBoundingClientRect();
          tooltip.style.left = (e.clientX - cRect.left + 15) + 'px';
          tooltip.style.top = (e.clientY - cRect.top + 15) + 'px';
        });
        el.addEventListener('mouseleave', (e) => {
          tooltip.style.display = 'none';
          e.target.style.opacity = e.target.tagName === 'rect' ? '0.85' : '1';
        });
      });
    }

    window.addEventListener('load', renderSVG);
    window.addEventListener('resize', renderSVG);
    setTimeout(renderSVG, 100);
  </script>
</body>
</html>
"""

with open(target_html, 'w', encoding='utf-8') as f:
    f.write(html_code)

with open(dist_html, 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Fixed JavaScript comments and re-generated perfect HTML!")
