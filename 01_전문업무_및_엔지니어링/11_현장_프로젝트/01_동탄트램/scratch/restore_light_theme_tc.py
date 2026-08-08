import os

target_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'
dist_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\index.html'

html_code = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>동탄도시철도 트램 Time-Chainage & 예정공정표 엔지니어링 대시보드</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-main: #f8fafc;
      --bg-panel: #ffffff;
      --bg-sub: #f1f5f9;
      --border: #e2e8f0;
      --border-dark: #cbd5e1;
      --text-main: #0f172a;
      --text-sub: #475569;
      --text-muted: #64748b;
      --primary: #2563eb;
      --primary-light: #eff6ff;
      --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
      --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      width: 100vw; height: 100vh;
      background-color: var(--bg-main);
      color: var(--text-main);
      font-family: 'Noto Sans KR', 'Inter', -apple-system, sans-serif;
      overflow: hidden;
    }

    /* 상단 통합 헤더 */
    .app-header {
      height: 56px; background: #ffffff;
      border-bottom: 1px solid var(--border);
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 1.5rem; box-shadow: var(--shadow-sm); z-index: 10;
    }
    .brand-title {
      font-size: 1.15rem; font-weight: 700; color: #1e3a8a;
      display: flex; align-items: center; gap: 10px;
    }
    .brand-tag {
      font-size: 0.72rem; background: #dbeafe; color: #1e40af;
      padding: 3px 9px; border-radius: 9999px; font-weight: 600; border: 1px solid #bfdbfe;
    }
    .header-actions { display: flex; align-items: center; gap: 12px; font-size: 0.85rem; color: var(--text-sub); }
    .btn-action {
      background: #ffffff; border: 1px solid var(--border-dark); color: var(--text-main);
      padding: 6px 14px; border-radius: 6px; font-size: 0.82rem; font-weight: 600;
      cursor: pointer; transition: all 0.15s; display: flex; align-items: center; gap: 6px;
    }
    .btn-action:hover { background: var(--bg-sub); border-color: var(--primary); color: var(--primary); }
    .btn-primary { background: var(--primary); color: #ffffff; border: none; }
    .btn-primary:hover { background: #1d4ed8; color: #ffffff; }

    /* 메인 2열 레이아웃 */
    .app-layout {
      height: calc(100vh - 56px); display: flex; width: 100vw;
    }

    /* 좌측 WBS 사이드바 */
    .sidebar {
      width: 360px; background: var(--bg-panel);
      border-right: 1px solid var(--border);
      display: flex; flex-direction: column; overflow: hidden;
    }
    .sidebar-header {
      padding: 1.1rem 1.25rem 0.8rem; border-bottom: 1px solid var(--border);
      display: flex; justify-content: space-between; align-items: center;
    }
    .sidebar-title { font-size: 0.98rem; font-weight: 700; color: var(--text-main); }
    .wbs-scroll { flex: 1; overflow-y: auto; padding: 1rem 1.25rem; display: flex; flex-direction: column; gap: 8px; }

    .wbs-card {
      background: #ffffff; border: 1px solid var(--border); border-radius: 8px;
      padding: 0.8rem 1rem; font-size: 0.86rem; cursor: pointer; transition: all 0.2s;
      box-shadow: var(--shadow-sm); position: relative; overflow: hidden;
    }
    .wbs-card::before {
      content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
      background: var(--card-color, #cbd5e1);
    }
    .wbs-card:hover { border-color: var(--primary); transform: translateY(-1px); box-shadow: var(--shadow-md); }
    .wbs-card.active { border-color: var(--primary); background: var(--primary-light); }
    .wbs-head { display: flex; justify-content: space-between; align-items: center; font-weight: 700; margin-bottom: 4px; }
    .wbs-code { font-size: 0.72rem; color: #475569; background: #e2e8f0; padding: 2px 6px; border-radius: 4px; font-weight: 600; }
    .wbs-sub { color: var(--text-muted); font-size: 0.78rem; }

    /* 메인 타임체인지 차트 및 간트판 */
    .main-view {
      flex: 1; display: flex; flex-direction: column; padding: 1.25rem; gap: 1.25rem;
      background: var(--bg-main); overflow: hidden;
    }

    .chart-box {
      flex: 1; background: var(--bg-panel); border: 1px solid var(--border);
      border-radius: 12px; display: flex; flex-direction: column; padding: 1.25rem;
      box-shadow: var(--shadow-sm); position: relative; min-height: 0;
    }
    .chart-topbar {
      display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;
    }
    .chart-title-text { font-size: 1.05rem; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 8px; }
    .chart-legend-group { display: flex; gap: 16px; font-size: 0.8rem; font-weight: 500; }
    .legend-item { display: flex; align-items: center; gap: 6px; }
    .legend-indicator { width: 12px; height: 12px; border-radius: 3px; }

    .svg-wrapper {
      flex: 1; width: 100%; height: 100%; position: relative; min-height: 0; background: #ffffff;
      border: 1px solid #f1f5f9; border-radius: 8px; overflow: hidden;
    }
    svg { width: 100%; height: 100%; display: block; }

    /* 마우스 호버 툴팁 */
    .tooltip-card {
      position: absolute; pointer-events: none; display: none;
      background: rgba(15, 23, 42, 0.92); border: 1px solid #0284c7;
      border-radius: 8px; padding: 10px 14px; font-size: 0.82rem;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3); z-index: 100; color: #ffffff;
      line-height: 1.5; backdrop-filter: blur(4px);
    }
    .tooltip-title { font-weight: 700; color: #38bdf8; font-size: 0.88rem; margin-bottom: 2px; }

    /* 하단 통계 수치 바 */
    .summary-bar {
      height: 48px; background: var(--bg-panel); border: 1px solid var(--border);
      border-radius: 8px; display: flex; align-items: center; padding: 0 1.5rem; justify-content: space-between;
      font-size: 0.85rem; box-shadow: var(--shadow-sm);
    }
    .stat-pill { display: flex; align-items: center; gap: 8px; color: var(--text-sub); }
    .stat-pill strong { color: #1e3a8a; font-weight: 700; }
  </style>
</head>
<body>

  <!-- 헤더 -->
  <header class="app-header">
    <div class="brand-title">
      🚈 동탄도시철도 트램 Time-Chainage & 예정공정표 대시보드
      <span class="brand-tag">엔지니어링 표준 뷰어 (Light Theme)</span>
    </div>
    <div class="header-actions">
      <button class="btn-action" onclick="alert('추후 전달해주실 공정엑셀 데이터를 선택해 반영할 수 있습니다.')">
        📁 엑셀 데이터 불러오기
      </button>
      <button class="btn-action btn-primary" onclick="alert('현재 공정 다이어그램 고화질 리포트 인쇄 준비 완료')">
        🖨️ 공정 리포트 인쇄
      </button>
    </div>
  </header>

  <!-- 레이아웃 -->
  <div class="app-layout">
    
    <!-- 사이드바 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="sidebar-title">📋 WBS 공종 체계 목록</div>
        <span style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">5개 핵심 공종</span>
      </div>
      <div class="wbs-scroll" id="wbs-list"></div>
    </aside>

    <!-- 메인 대시보드 차트 -->
    <main class="main-view">
      <div class="chart-box">
        <div class="chart-topbar">
          <div class="chart-title-text">
            📍 Time-Chainage 종합 다이어그램
            <span style="font-size:0.78rem; font-weight:400; color:var(--text-muted);">(X축: 노선 위치 STA / Y축: 시공 일정 Timeline)</span>
          </div>
          <div class="chart-legend-group" id="chart-legend"></div>
        </div>

        <div class="svg-wrapper" id="svg-wrapper">
          <svg id="tc-svg"></svg>
          <div class="tooltip-card" id="tooltip"></div>
        </div>
      </div>

      <!-- 하단 요약바 -->
      <div class="summary-bar">
        <div class="stat-pill">총 시공연장: <strong>34.4km (1공구 + 2공구)</strong></div>
        <div class="stat-pill">정거장 수: <strong>총 34개 역 (지상 33 / 지하 1)</strong></div>
        <div class="stat-pill">1공구 구간: <strong>301역 ~ 201역 (동탄역 연계)</strong></div>
        <div class="stat-pill">2공구 구간: <b>201역 ~ S01/114역 (망포/남동탄)</b></div>
        <div class="stat-pill">목표 준공: <strong>2031년 12월</strong></div>
      </div>
    </main>

  </div>

  <script>
    // ─────────────────────────────────────────────
    // 동탄트램 노정 정거장 데이터 (km 위치)
    // ─────────────────────────────────────────────
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
      { id:'114', km:20.5, name:'114(남동탄)' }
    ];

    // WBS 분류 체계 (라이트 테마 팔레트)
    const WBS_ITEMS = [
      { id:'wbs-1-1', name:'토목 / 개착공사', color:'#dc2626', desc:'본선 개착 굴착 및 토공사 타임라인' },
      { id:'wbs-1-2', name:'정거장 구조물공사', color:'#0284c7', desc:'34개 정거장 본체 및 승강장 구조물' },
      { id:'wbs-1-3', name:'트램 궤도공사', color:'#16a34a', desc:'자갈/콘크리트 매립형 궤도 포설' },
      { id:'wbs-1-4', name:'건축 / 차량기지', color:'#ca8a04', desc:'종합관리동 및 검수고 건축' },
      { id:'wbs-1-5', name:'전기 / 신호 / 시스템', color:'#9333ea', desc:'전차선, 트램 신호, 통신 네트워크' }
    ];

    // 예정공정 액티비티 샘플 데이터
    const ACTIVITIES = [
      { id:'act-1', wbsId:'wbs-1-1', name:'1공구 토목 개착공사 (병점역~동탄역)', startStn:'301', endStn:'201', startYr:2027.2, endYr:2028.8, color:'#dc2626' },
      { id:'act-2', wbsId:'wbs-1-1', name:'2공구 본선 토목공사 (동탄역~남동탄)', startStn:'201', endStn:'114', startYr:2027.5, endYr:2029.5, color:'#dc2626' },
      { id:'act-3', wbsId:'wbs-1-3', name:'1공구 궤도 포설공사', startStn:'301', endStn:'201', startYr:2028.9, endYr:2029.8, color:'#16a34a' },
      { id:'act-4', wbsId:'wbs-1-3', name:'2공구 궤도 포설공사', startStn:'201', endStn:'114', startYr:2029.5, endYr:2030.7, color:'#16a34a' },
      { id:'act-5', wbsId:'wbs-1-5', name:'전 구간 전차선 및 신호 시스템 포설', startStn:'301', endStn:'114', startYr:2030.0, endYr:2031.5, color:'#9333ea' }
    ];

    // 정거장 블록 시공 기간 추가
    STATIONS.forEach((st, idx) => {
      const startY = 2028.0 + (idx * 0.08);
      ACTIVITIES.push({
        id: `st-${st.id}`,
        wbsId: 'wbs-1-2',
        name: `${st.name} 정거장 구조물 시공`,
        stnId: st.id,
        km: st.km,
        startYr: startY,
        endYr: startY + 0.55,
        color: '#0284c7',
        isBlock: true
      });
    });

    const wbsContainer = document.getElementById('wbs-list');
    const legendContainer = document.getElementById('chart-legend');
    const svg = document.getElementById('tc-svg');
    const tooltip = document.getElementById('tooltip');

    // WBS 사이드바 카드 구성
    WBS_ITEMS.forEach(wbs => {
      const card = document.createElement('div');
      card.className = 'wbs-card active';
      card.style.setProperty('--card-color', wbs.color);
      card.innerHTML = `
        <div class="wbs-head">
          <span>${wbs.name}</span>
          <span class="wbs-code" style="background:${wbs.color}15; color:${wbs.color}; border:1px solid ${wbs.color}40">${wbs.id}</span>
        </div>
        <div class="wbs-sub">${wbs.desc}</div>
      `;
      wbsContainer.appendChild(card);

      const legend = document.createElement('div');
      legend.className = 'legend-item';
      legend.innerHTML = `<div class="legend-indicator" style="background:${wbs.color}"></div><span>${wbs.name}</span>`;
      legendContainer.appendChild(legend);
    });

    // Time-Chainage 2D SVG 렌더링 함수
    function renderSVG() {
      const rect = svg.getBoundingClientRect();
      const width = rect.width || 900;
      const height = rect.height || 550;
      
      const padL = 70, padR = 40, padT = 30, padB = 65;
      const graphW = width - padL - padR;
      const graphH = height - padT - padB;

      const minKm = 0.0, maxKm = 21.0;
      const minYr = 2027.0, maxYr = 2032.0;

      const getX = (km) => padL + ((km - minKm) / (maxKm - minKm)) * graphW;
      const getY = (yr) => padT + graphH - ((yr - minYr) / (maxYr - minYr)) * graphH;

      let html = '';

      // Y축 연도 격자선 (Light theme #e2e8f0)
      for (let yr = 2027; yr <= 2032; yr += 0.5) {
        const y = getY(yr);
        html += `<line x1="${padL}" y1="${y}" x2="${width - padR}" y2="${y}" stroke="#e2e8f0" stroke-dasharray="4,4" stroke-width="1"/>`;
        html += `<text x="${padL - 14}" y="${y + 4}" fill="#64748b" font-size="11" font-weight="500" text-anchor="end">${yr.toFixed(1)}년</text>`;
      }

      // X축 정거장 수직 가이드선 및 텍스트
      STATIONS.forEach((st) => {
        const x = getX(st.km);
        html += `<line x1="${x}" y1="${padT}" x2="${x}" y2="${height - padB}" stroke="#f1f5f9" stroke-width="1.2"/>`;
        html += `<text x="${x}" y="${height - padB + 20}" fill="#475569" font-size="10.5" font-weight="500" text-anchor="end" transform="rotate(-45, ${x}, ${height - padB + 20})">${st.name}</text>`;
      });

      // 공정 라인 및 블록 렌더링
      ACTIVITIES.forEach(act => {
        if (act.isBlock) {
          const x = getX(act.km);
          const y1 = getY(act.startYr);
          const y2 = getY(act.endYr);
          html += `<rect x="${x - 6}" y="${Math.min(y1, y2)}" width="12" height="${Math.abs(y2 - y1)}" fill="${act.color}" opacity="0.85" rx="3" class="act-element" data-title="${act.name}" data-time="${act.startYr.toFixed(1)}년 ~ ${act.endYr.toFixed(1)}년" style="cursor:pointer; transition:all 0.2s;"/>`;
        } else {
          const stA = STATIONS.find(s => s.id === act.startStn) || STATIONS[0];
          const stB = STATIONS.find(s => s.id === act.endStn) || STATIONS[STATIONS.length - 1];
          const x1 = getX(stA.km);
          const y1 = getY(act.startYr);
          const x2 = getX(stB.km);
          const y2 = getY(act.endYr);
          html += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${act.color}" stroke-width="5" stroke-linecap="round" class="act-element" data-title="${act.name}" data-time="${act.startYr.toFixed(1)}년 ~ ${act.endYr.toFixed(1)}년" style="cursor:pointer; transition:all 0.2s;"/>`;
        }
      });

      svg.innerHTML = html;

      // 마우스 툴팁 이벤트
      document.querySelectorAll('.act-element').forEach(el => {
        el.addEventListener('mouseenter', (e) => {
          tooltip.style.display = 'block';
          tooltip.innerHTML = `<div class="tooltip-title">${e.target.dataset.title}</div><div>시공 예정기간: <b>${e.target.dataset.time}</b></div>`;
          el.style.opacity = '1';
          el.style.filter = 'drop-shadow(0 4px 6px rgba(0,0,0,0.15))';
        });
        el.addEventListener('mousemove', (e) => {
          const cRect = svg.getBoundingClientRect();
          tooltip.style.left = (e.clientX - cRect.left + 15) + 'px';
          tooltip.style.top = (e.clientY - cRect.top + 15) + 'px';
        });
        el.addEventListener('mouseleave', (e) => {
          tooltip.style.display = 'none';
          e.target.style.opacity = e.target.tagName === 'rect' ? '0.85' : '1';
          e.target.style.filter = 'none';
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

print("Successfully restored Premium Light-Theme Time-Chainage Dashboard HTML!")
