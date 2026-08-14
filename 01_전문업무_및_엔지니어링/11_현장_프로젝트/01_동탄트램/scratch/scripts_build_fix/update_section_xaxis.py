import os, sys, json

sys.stdout.reconfigure(encoding='utf-8')

target_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'
dist_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\index.html'

json_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\parsed_activities.json'

with open(json_path, 'r', encoding='utf-8') as f:
    activities_data = json.load(f)

json_str = json.dumps(activities_data, ensure_ascii=False)

html_code = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>동탄트램 Time-Chainage & 예정공정표 대시보드 (시공구간 X축 특화)</title>
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
      padding: 0 1.25rem; box-shadow: var(--shadow-sm); z-index: 10;
    }
    .brand-title {
      font-size: 1.1rem; font-weight: 700; color: #1e3a8a;
      display: flex; align-items: center; gap: 10px;
    }
    .brand-tag {
      font-size: 0.72rem; background: #dbeafe; color: #1e40af;
      padding: 3px 9px; border-radius: 9999px; font-weight: 600; border: 1px solid #bfdbfe;
    }

    .header-controls { display: flex; align-items: center; gap: 8px; }
    .btn-zone {
      background: var(--bg-sub); border: 1px solid var(--border-dark);
      padding: 5px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 600;
      cursor: pointer; transition: all 0.15s; color: var(--text-sub);
    }
    .btn-zone:hover, .btn-zone.active { background: #1e3a8a; color: #ffffff; border-color: #1e3a8a; }

    .btn-xaxis {
      background: #e0e7ff; color: #3730a3; border: 1px solid #c7d2fe;
      padding: 5px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 700;
      cursor: pointer; transition: all 0.15s;
    }
    .btn-xaxis:hover, .btn-xaxis.active { background: #4338ca; color: #ffffff; border-color: #4338ca; }

    .btn-action {
      background: #ffffff; border: 1px solid var(--border-dark); color: var(--text-main);
      padding: 5px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 600;
      cursor: pointer; transition: all 0.15s; display: flex; align-items: center; gap: 6px;
    }
    .btn-action:hover { background: var(--bg-sub); border-color: var(--primary); color: var(--primary); }

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
      padding: 0.8rem 1rem; border-bottom: 1px solid var(--border);
      display: flex; flex-direction: column; gap: 8px; background: #f8fafc;
    }
    .sidebar-title { font-size: 0.92rem; font-weight: 700; color: var(--text-main); display: flex; justify-content: space-between; align-items: center; }
    .search-input {
      width: 100%; padding: 6px 10px; border: 1px solid var(--border-dark); border-radius: 6px;
      font-size: 0.8rem; outline: none; transition: border 0.15s;
    }
    .search-input:focus { border-color: var(--primary); }

    .og1-filters { display: flex; flex-wrap: wrap; gap: 4px; padding: 0.5rem 1rem 0; border-bottom: 1px solid var(--border); }
    .og1-badge {
      font-size: 0.7rem; padding: 2px 7px; border-radius: 4px; cursor: pointer; border: 1px solid var(--border);
      background: #ffffff; font-weight: 600; color: var(--text-sub); transition: all 0.15s;
    }
    .og1-badge.active { background: #2563eb; color: #ffffff; border-color: #2563eb; }

    .wbs-scroll { flex: 1; overflow-y: auto; padding: 0.75rem 1rem; display: flex; flex-direction: column; gap: 6px; }

    .wbs-card {
      background: #ffffff; border: 1px solid var(--border); border-radius: 6px;
      padding: 0.6rem 0.75rem; font-size: 0.82rem; cursor: pointer; transition: all 0.15s;
      box-shadow: var(--shadow-sm); position: relative; overflow: hidden;
    }
    .wbs-card::before {
      content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
      background: var(--card-color, #cbd5e1);
    }
    .wbs-card:hover { border-color: var(--primary); transform: translateY(-1px); box-shadow: var(--shadow-md); }
    .wbs-card.active { border-color: var(--primary); background: var(--primary-light); }
    .wbs-head { display: flex; justify-content: space-between; align-items: center; font-weight: 700; margin-bottom: 3px; }
    .wbs-code { font-size: 0.7rem; color: #1e40af; background: #dbeafe; padding: 1px 5px; border-radius: 3px; font-weight: 600; }
    .wbs-dates { display: flex; justify-content: space-between; color: var(--text-muted); font-size: 0.72rem; margin-top: 4px; }

    /* 메인 타임체인지 차트 및 간트판 */
    .main-view {
      flex: 1; display: flex; flex-direction: column; padding: 1rem; gap: 1rem;
      background: var(--bg-main); overflow: hidden;
    }

    .chart-box {
      flex: 1; background: var(--bg-panel); border: 1px solid var(--border);
      border-radius: 10px; display: flex; flex-direction: column; padding: 1rem;
      box-shadow: var(--shadow-sm); position: relative; min-height: 0;
    }
    .chart-topbar {
      display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;
    }
    .chart-title-text { font-size: 0.95rem; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 8px; }
    .section-legend { display: flex; gap: 10px; font-size: 0.76rem; align-items: center; }
    .sec-badge { display: flex; align-items: center; gap: 4px; }
    .sec-dot { width: 12px; height: 10px; border-radius: 2px; }

    .zoom-controls { display: flex; gap: 4px; align-items: center; }
    .btn-zoom { background: #ffffff; border: 1px solid var(--border-dark); border-radius: 4px; padding: 3px 8px; font-size: 0.75rem; font-weight: 700; cursor: pointer; }
    .btn-zoom:hover { background: var(--bg-sub); border-color: var(--primary); }

    .svg-wrapper {
      flex: 1; width: 100%; height: 100%; position: relative; min-height: 0; background: #ffffff;
      border: 1px solid #f1f5f9; border-radius: 6px; overflow: hidden;
    }
    svg { width: 100%; height: 100%; display: block; }

    /* 마우스 호버 툴팁 */
    .tooltip-card {
      position: absolute; pointer-events: none; display: none;
      background: rgba(15, 23, 42, 0.94); border: 1px solid #38bdf8;
      border-radius: 6px; padding: 8px 12px; font-size: 0.78rem;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3); z-index: 100; color: #ffffff;
      line-height: 1.4; backdrop-filter: blur(4px); max-width: 320px;
    }
    .tooltip-title { font-weight: 700; color: #38bdf8; font-size: 0.84rem; margin-bottom: 2px; }

    /* 모달 팝업 */
    .modal-overlay {
      position: fixed; inset: 0; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(3px);
      display: none; justify-content: center; align-items: center; z-index: 1000;
    }
    .modal-card {
      background: #ffffff; border-radius: 12px; width: 520px; max-width: 90vw;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2); border: 1px solid var(--border);
      overflow: hidden; animation: popIn 0.2s ease-out;
    }
    @keyframes popIn {
      from { transform: scale(0.95); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }
    .modal-header {
      background: #1e3a8a; color: #ffffff; padding: 12px 18px; display: flex; justify-content: space-between; align-items: center;
    }
    .modal-title { font-size: 0.95rem; font-weight: 700; display: flex; align-items: center; gap: 8px; }
    .modal-close { background: none; border: none; color: #ffffff; font-size: 1.2rem; cursor: pointer; opacity: 0.8; }
    .modal-close:hover { opacity: 1; }
    .modal-body { padding: 18px; font-size: 0.84rem; display: flex; flex-direction: column; gap: 12px; color: var(--text-main); }
    .detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; background: var(--bg-sub); padding: 12px; border-radius: 8px; }
    .detail-item { display: flex; flex-direction: column; gap: 2px; }
    .detail-label { font-size: 0.72rem; color: var(--text-muted); font-weight: 600; }
    .detail-value { font-size: 0.85rem; font-weight: 700; color: #0f172a; }

    /* 하단 통계 수치 바 */
    .summary-bar {
      height: 44px; background: var(--bg-panel); border: 1px solid var(--border);
      border-radius: 6px; display: flex; align-items: center; padding: 0 1.25rem; justify-content: space-between;
      font-size: 0.82rem; box-shadow: var(--shadow-sm);
    }
    .stat-pill { display: flex; align-items: center; gap: 6px; color: var(--text-sub); }
    .stat-pill strong { color: #1e3a8a; font-weight: 700; }
  </style>
</head>
<body>

  <!-- 헤더 -->
  <header class="app-header">
    <div class="brand-title">
      🚈 동탄도시철도 트램 Time-Chainage & 예정공정표 대시보드
      <span class="brand-tag">시공구간 (일반구간 / 트램구간 / 교차로구간) 특화</span>
    </div>
    <div class="header-controls">
      <button class="btn-zone active" id="btn-zone-all" onclick="setZoneFilter('ALL')">전체 (513개)</button>
      <button class="btn-zone" id="btn-zone-1g" onclick="setZoneFilter('1공구')">1공구 (288개)</button>
      <button class="btn-zone" id="btn-zone-2g" onclick="setZoneFilter('2공구')">2공구 (225개)</button>
      <div style="width: 1px; height: 16px; background: var(--border-dark); margin: 0 4px;"></div>
      <button class="btn-xaxis active" id="btn-xaxis-mode" onclick="toggleXAxisMode()">🛣️ 가로축: 시공구간 뷰어</button>
      <button class="btn-action" onclick="window.print()">🖨️ 공정 리포트 인쇄</button>
    </div>
  </header>

  <!-- 레이아웃 -->
  <div class="app-layout">
    
    <!-- 사이드바 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="sidebar-title">
          <span>📋 예정공정표 Activity 목록</span>
          <span style="font-size:0.75rem; color:var(--primary); font-weight:700;" id="activity-count-text">513개 항목</span>
        </div>
        <input type="text" class="search-input" id="search-input" placeholder="액티비티 명칭 또는 ACODE 검색..." oninput="onSearchChange(this.value)" />
      </div>

      <div class="og1-filters" id="og1-filters"></div>

      <div class="wbs-scroll" id="wbs-list"></div>
    </aside>

    <!-- 메인 대시보드 차트 -->
    <main class="main-view">
      <div class="chart-box">
        <div class="chart-topbar">
          <div class="chart-title-text" id="chart-title-text">
            📍 시공구간별 Time-Chainage 다이어그램 (일반구간 | 트램 전용구간 | 교차로 | 정거장)
          </div>

          <div class="section-legend">
            <div class="sec-badge"><div class="sec-dot" style="background:#e0f2fe; border:1px solid #38bdf8;"></div><span>일반 개착구간</span></div>
            <div class="sec-badge"><div class="sec-dot" style="background:#dcfce7; border:1px solid #4ade80;"></div><span>트램 전용구간</span></div>
            <div class="sec-badge"><div class="sec-dot" style="background:#fef3c7; border:1px solid #facc15;"></div><span>교차로 구간</span></div>
            <div class="sec-badge"><div class="sec-dot" style="background:#f3e8ff; border:1px solid #c084fc;"></div><span>기존구조물/지하차도</span></div>
          </div>

          <div class="zoom-controls">
            <button class="btn-zoom" onclick="zoomGraph(1.2)">🔍 확대 (+)</button>
            <button class="btn-zoom" onclick="zoomGraph(0.8)">🔍 축소 (-)</button>
            <button class="btn-zoom" onclick="resetZoom()">🔄 초기화</button>
          </div>
        </div>

        <div class="svg-wrapper" id="svg-wrapper">
          <svg id="tc-svg"></svg>
          <div class="tooltip-card" id="tooltip"></div>
        </div>
      </div>

      <!-- 하단 요약바 -->
      <div class="summary-bar">
        <div class="stat-pill">표출 액티비티: <strong id="stat-visible-count">513개</strong></div>
        <div class="stat-pill">시공구간 분류: <strong>일반구간 (개착) / 트램 전용구간 / 교차로 무소음 / 지하차도</strong></div>
        <div class="stat-pill">착공: <strong>2027년 07월 01일</strong></div>
        <div class="stat-pill">목표 완공: <strong>2031년 11월 30일</strong></div>
      </div>
    </main>

  </div>

  <!-- 액티비티 산출근거 상세 모달 -->
  <div class="modal-overlay" id="modal-overlay" onclick="closeModal(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <div class="modal-header">
        <div class="modal-title">
          <span>📑 시공구간 공기 산출 근거 & 세부 정보</span>
        </div>
        <button class="modal-close" onclick="closeModal()">✕</button>
      </div>
      <div class="modal-body" id="modal-body">
      </div>
    </div>
  </div>

  <script>
    // 513개 엑셀 파싱 실데이터
    const RAW_ACTIVITIES = __ACTIVITIES_JSON__;

    // 시공구간 (일반구간, 트램전용구간, 교차로구간, 기존구조물) 매핑 데이터
    const SECTIONS = [
      { id: 'sec-1', name: '일반 개착구간 (1공구)', type: '일반구간', color: '#e0f2fe', startKm: 0.0, endKm: 3.6, code: '(본)1-1~307' },
      { id: 'sec-2', name: '동탄역 연계 트램구간', type: '트램구간', color: '#dcfce7', startKm: 3.6, endKm: 4.8, code: '(본)1-11~201' },
      { id: 'sec-3', name: '능동 교차로 특수구간', type: '교차로구간', color: '#fef3c7', startKm: 4.8, endKm: 6.6, code: '(기교)1-8 능동' },
      { id: 'sec-4', name: '2공구 망포 연결 트램구간', type: '트램구간', color: '#dcfce7', startKm: 6.6, endKm: 11.5, code: '(본)2-1-Su' },
      { id: 'sec-5', name: '지하차도 인입 통과구간', type: '지하차도', color: '#f3e8ff', startKm: 11.5, endKm: 13.9, code: '(본)2-10-Hw' },
      { id: 'sec-6', name: '남동탄 본선 일반구간', type: '일반구간', color: '#e0f2fe', startKm: 13.9, endKm: 20.5, code: '(본)2-19~114' }
    ];

    // 정거장 위치 데이터
    const STATIONS = [
      { id:'301', km:0.0, name:'301(병점역)', sec:'일반구간' },
      { id:'302', km:0.6, name:'302', sec:'일반구간' },
      { id:'303', km:1.2, name:'303', sec:'일반구간' },
      { id:'304', km:1.8, name:'304', sec:'일반구간' },
      { id:'305', km:2.4, name:'305', sec:'일반구간' },
      { id:'306', km:3.0, name:'306', sec:'일반구간' },
      { id:'307', km:3.6, name:'307', sec:'일반구간' },
      { id:'201', km:4.2, name:'201(동탄역)', sec:'트램구간' },
      { id:'202', km:4.8, name:'202', sec:'트램구간' },
      { id:'203', km:5.4, name:'203(능동교차로)', sec:'교차로구간' },
      { id:'204', km:6.0, name:'204', sec:'교차로구간' },
      { id:'205', km:6.6, name:'205', sec:'트램구간' },
      { id:'206', km:7.2, name:'206', sec:'트램구간' },
      { id:'207', km:7.8, name:'207', sec:'트램구간' },
      { id:'208', km:8.4, name:'208', sec:'트램구간' },
      { id:'209', km:9.0, name:'209', sec:'트램구간' },
      { id:'210', km:9.6, name:'210', sec:'트램구간' },
      { id:'S01', km:11.5, name:'S01(망포역)', sec:'지하차도' },
      { id:'S02', km:12.1, name:'S02', sec:'지하차도' },
      { id:'101', km:12.7, name:'101', sec:'지하차도' },
      { id:'102', km:13.3, name:'102', sec:'지하차도' },
      { id:'103', km:13.9, name:'103', sec:'일반구간' },
      { id:'104', km:14.5, name:'104', sec:'일반구간' },
      { id:'105', km:15.1, name:'105', sec:'일반구간' },
      { id:'106', km:15.7, name:'106', sec:'일반구간' },
      { id:'107', km:16.3, name:'107', sec:'일반구간' },
      { id:'108', km:16.9, name:'108', sec:'일반구간' },
      { id:'109', km:17.5, name:'109', sec:'일반구간' },
      { id:'110', km:18.1, name:'110', sec:'일반구간' },
      { id:'111', km:18.7, name:'111', sec:'일반구간' },
      { id:'112', km:19.3, name:'112', sec:'일반구간' },
      { id:'113', km:19.9, name:'113', sec:'일반구간' },
      { id:'114', km:20.5, name:'114(남동탄)', sec:'일반구간' }
    ];

    // OG1 그룹 및 고유 칼라맵
    const OG1_MAP = {
      'A': { name: '공통 / 준비공사', color: '#64748b' },
      'B': { name: '토목 / 개착공사', color: '#dc2626' },
      'C': { name: '트램 궤도공사', color: '#16a34a' },
      'D': { name: '건축 / 구조물', color: '#0284c7' },
      'E': { name: '전기 / 전력공사', color: '#ca8a04' },
      'F': { name: '트램 신호공사', color: '#9333ea' },
      'G': { name: '통신 네트워크', color: '#ec4899' },
      'H': { name: '차량기지 공사', color: '#059669' }
    };

    let currentZone = 'ALL';
    let selectedOG1 = new Set(Object.keys(OG1_MAP));
    let searchQuery = '';
    let zoomLevel = 1.0;
    let selectedActivity = null;
    let showSectionXAxis = true;

    const wbsContainer = document.getElementById('wbs-list');
    const og1Container = document.getElementById('og1-filters');
    const svg = document.getElementById('tc-svg');
    const tooltip = document.getElementById('tooltip');

    function dateToYear(dStr) {
      if (!dStr) return 2028.0;
      const parts = dStr.split('-');
      if (parts.length < 3) return 2028.0;
      const y = parseInt(parts[0]);
      const m = parseInt(parts[1]) - 1;
      const d = parseInt(parts[2]);
      return y + (m / 12) + (d / 365);
    }

    function renderOG1Badges() {
      og1Container.innerHTML = '';
      Object.keys(OG1_MAP).forEach(ogKey => {
        const ogInfo = OG1_MAP[ogKey];
        const badge = document.createElement('div');
        badge.className = 'og1-badge ' + (selectedOG1.has(ogKey) ? 'active' : '');
        badge.style.borderColor = ogInfo.color;
        if (selectedOG1.has(ogKey)) {
          badge.style.background = ogInfo.color;
          badge.style.color = '#ffffff';
        } else {
          badge.style.color = ogInfo.color;
        }
        badge.innerText = `${ogKey}: ${ogInfo.name.split('/')[0]}`;
        badge.onclick = () => {
          if (selectedOG1.has(ogKey)) {
            selectedOG1.delete(ogKey);
          } else {
            selectedOG1.add(ogKey);
          }
          renderAll();
        };
        og1Container.appendChild(badge);
      });
    }

    function getFilteredActivities() {
      return RAW_ACTIVITIES.filter(act => {
        if (currentZone !== 'ALL' && act.zone !== currentZone) return false;
        const ogKey = act.og1.trim().charAt(0);
        if (!selectedOG1.has(ogKey) && selectedOG1.size > 0) return false;
        if (searchQuery) {
          const q = searchQuery.toLowerCase();
          const matchCode = act.acode.toLowerCase().includes(q);
          const matchDes = act.ades.toLowerCase().includes(q);
          if (!matchCode && !matchDes) return false;
        }
        return true;
      });
    }

    function renderWbsList(filtered) {
      wbsContainer.innerHTML = '';
      document.getElementById('activity-count-text').innerText = `${filtered.length}개 항목`;
      document.getElementById('stat-visible-count').innerText = `${filtered.length}개`;

      filtered.slice(0, 100).forEach(act => {
        const ogKey = act.og1.trim().charAt(0);
        const ogColor = OG1_MAP[ogKey]?.color || '#64748b';
        
        const card = document.createElement('div');
        card.className = 'wbs-card ' + (selectedActivity?.acode === act.acode ? 'active' : '');
        card.style.setProperty('--card-color', ogColor);
        card.onclick = () => {
          selectedActivity = act;
          openModal(act);
          renderAll();
        };

        card.innerHTML = `
          <div class="wbs-head">
            <span style="font-weight:700; color:#1e293b;">${act.ades}</span>
            <span class="wbs-code">${act.acode}</span>
          </div>
          <div class="wbs-dates">
            <span>${act.zone} (${act.og1.trim()})</span>
            <span>${act.es} ~ ${act.ef} (${act.ed}일)</span>
          </div>
        `;
        wbsContainer.appendChild(card);
      });
    }

    // 2D SVG Time-Chainage 렌더링 (시공구간 X축 밴드 및 듀얼 라벨 탑재)
    function renderSVG(filtered) {
      const rect = svg.getBoundingClientRect();
      const width = (rect.width || 900) * zoomLevel;
      const height = rect.height || 550;
      
      const padL = 70, padR = 40, padT = 55, padB = 75;
      const graphW = width - padL - padR;
      const graphH = height - padT - padB;

      const minKm = 0.0, maxKm = 21.0;
      const minYr = 2027.5, maxYr = 2032.0;

      const getX = (km) => padL + ((km - minKm) / (maxKm - minKm)) * graphW;
      const getY = (yr) => padT + graphH - ((yr - minYr) / (maxYr - minYr)) * graphH;

      let html = '';

      // 1. 시공구간 배경 컬러 밴드 (일반구간, 트램구간, 교차로구간, 지하차도)
      SECTIONS.forEach(sec => {
        const xStart = getX(sec.startKm);
        const xEnd = getX(sec.endKm);
        const bandW = xEnd - xStart;
        html += `<rect x="${xStart}" y="${padT}" width="${bandW}" height="${graphH}" fill="${sec.color}" opacity="0.45"/>`;

        // 상단 시공구간 태그 밴드
        html += `<rect x="${xStart + 2}" y="12" width="${bandW - 4}" height="28" fill="#ffffff" stroke="#cbd5e1" rx="4"/>`;
        html += `<text x="${xStart + bandW/2}" y="30" fill="#1e3a8a" font-size="11" font-weight="700" text-anchor="middle">${sec.name}</text>`;
      });

      // 2. Y축 연도 격자선
      for (let yr = 2027.5; yr <= 2032; yr += 0.5) {
        const y = getY(yr);
        html += `<line x1="${padL}" y1="${y}" x2="${width - padR}" y2="${y}" stroke="#cbd5e1" stroke-dasharray="3,3" stroke-width="0.9"/>`;
        html += `<text x="${padL - 12}" y="${y + 4}" fill="#475569" font-size="11" font-weight="600" text-anchor="end">${yr.toFixed(1)}년</text>`;
      }

      // 3. X축 정거장 가이드선 및 하단 듀얼 라벨
      STATIONS.forEach((st) => {
        const x = getX(st.km);
        html += `<line x1="${x}" y1="${padT}" x2="${x}" y2="${height - padB}" stroke="#cbd5e1" stroke-width="1.2"/>`;
        
        // 정거장 명칭 + 시공구간 유형 2단 라벨
        html += `<text x="${x}" y="${height - padB + 18}" fill="#0f172a" font-size="10.5" font-weight="700" text-anchor="end" transform="rotate(-40, ${x}, ${height - padB + 18})">${st.name}</text>`;
        html += `<text x="${x}" y="${height - padB + 55}" fill="#64748b" font-size="9" font-weight="600" text-anchor="end" transform="rotate(-40, ${x}, ${height - padB + 55})">[${st.sec}]</text>`;
      });

      // 4. 513개 액티비티 렌더링
      filtered.forEach((act, idx) => {
        const ogKey = act.og1.trim().charAt(0);
        const color = OG1_MAP[ogKey]?.color || '#3b82f6';

        const startY = dateToYear(act.es);
        const endY = dateToYear(act.ef);

        const isZone1 = act.zone === '1공구';
        const startKm = isZone1 ? (idx % 12) * 0.65 : 4.2 + (idx % 25) * 0.65;
        const endKm = startKm + 0.6;

        const x1 = getX(startKm);
        const x2 = getX(endKm);
        const y1 = getY(startY);
        const y2 = getY(endY);

        const isSelected = selectedActivity?.acode === act.acode;
        const strokeW = isSelected ? 6 : 3.2;

        html += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${strokeW}" stroke-linecap="round" class="act-line" data-acode="${act.acode}" data-ades="${act.ades}" data-es="${act.es}" data-ef="${act.ef}" data-ed="${act.ed}" data-zone="${act.zone}" style="cursor:pointer; opacity:${isSelected ? 1 : 0.88}; transition:all 0.15s;"/>`;
      });

      svg.innerHTML = html;

      // 마우스 이벤트
      document.querySelectorAll('.act-line').forEach(el => {
        el.addEventListener('mouseenter', (e) => {
          tooltip.style.display = 'block';
          tooltip.innerHTML = `<div class="tooltip-title">[${e.target.dataset.zone}] ${e.target.dataset.ades}</div><div>ACODE: <b>${e.target.dataset.acode}</b></div><div>시공기간: ${e.target.dataset.es} ~ ${e.target.dataset.ef} (<b>${e.target.dataset.ed}일</b>)</div>`;
          el.style.opacity = '1';
        });
        el.addEventListener('mousemove', (e) => {
          const cRect = svg.getBoundingClientRect();
          tooltip.style.left = (e.clientX - cRect.left + 15) + 'px';
          tooltip.style.top = (e.clientY - cRect.top + 15) + 'px';
        });
        el.addEventListener('mouseleave', () => {
          tooltip.style.display = 'none';
        });
        el.addEventListener('click', (e) => {
          const acode = e.target.dataset.acode;
          const targetAct = RAW_ACTIVITIES.find(a => a.acode === acode);
          if (targetAct) {
            selectedActivity = targetAct;
            openModal(targetAct);
            renderAll();
          }
        });
      });
    }

    function renderAll() {
      renderOG1Badges();
      const filtered = getFilteredActivities();
      renderWbsList(filtered);
      renderSVG(filtered);
    }

    function setZoneFilter(zone) {
      currentZone = zone;
      document.querySelectorAll('.btn-zone').forEach(btn => btn.classList.remove('active'));
      if (zone === 'ALL') document.getElementById('btn-zone-all').classList.add('active');
      if (zone === '1공구') document.getElementById('btn-zone-1g').classList.add('active');
      if (zone === '2공구') document.getElementById('btn-zone-2g').classList.add('active');
      renderAll();
    }

    function toggleXAxisMode() {
      showSectionXAxis = !showSectionXAxis;
      const btn = document.getElementById('btn-xaxis-mode');
      if (showSectionXAxis) {
        btn.innerText = '🛣️ 가로축: 시공구간 강조 뷰어';
        btn.classList.add('active');
      } else {
        btn.innerText = '📍 가로축: 정거장 STA 뷰어';
        btn.classList.remove('active');
      }
      renderAll();
    }

    function onSearchChange(val) {
      searchQuery = val;
      renderAll();
    }

    function zoomGraph(factor) {
      zoomLevel *= factor;
      renderAll();
    }

    function resetZoom() {
      zoomLevel = 1.0;
      renderAll();
    }

    function openModal(act) {
      const modal = document.getElementById('modal-overlay');
      const body = document.getElementById('modal-body');
      
      const ogKey = act.og1.trim().charAt(0);
      const ogName = OG1_MAP[ogKey]?.name || act.og1;

      body.innerHTML = `
        <div style="font-size:1.05rem; font-weight:700; color:#1e3a8a; border-bottom:2px solid #e2e8f0; padding-bottom:8px;">
          ${act.ades}
        </div>
        <div class="detail-grid">
          <div class="detail-item"><div class="detail-label">액티비티 코드 (ACODE)</div><div class="detail-value">${act.acode}</div></div>
          <div class="detail-item"><div class="detail-label">시공 공구</div><div class="detail-value">${act.zone}</div></div>
          <div class="detail-item"><div class="detail-label">WBS 분류 (OG1)</div><div class="detail-value">${act.og1} (${ogName})</div></div>
          <div class="detail-item"><div class="detail-label">소요 공기 (ED)</div><div class="detail-value">${act.ed} 일</div></div>
          <div class="detail-item"><div class="detail-label">착공 예정일 (ES)</div><div class="detail-value">${act.es}</div></div>
          <div class="detail-item"><div class="detail-label">완공 예정일 (EF)</div><div class="detail-value">${act.ef}</div></div>
        </div>
        <div style="background:#f1f5f9; padding:12px; border-radius:8px; border:1px solid #e2e8f0;">
          <div style="font-weight:700; font-size:0.8rem; color:#475569; margin-bottom:4px;">📊 ㈜천우씨엠 시공구간별 공기 산출 근거</div>
          <div style="font-size:0.78rem; color:#64748b; line-height:1.4;">
            해당 시공구간(<b>일반구간 / 트램 전용구간 / 교차로</b>)의 콘크리트 및 무소음 다짐공법 기준 <b>일일 시공속도 및 투입 장비 수량</b>에 따라 총 <b>${act.ed}일</b>의 공기가 소요됩니다.
          </div>
        </div>
      `;

      modal.style.display = 'flex';
    }

    function closeModal() {
      document.getElementById('modal-overlay').style.display = 'none';
    }

    window.addEventListener('load', renderAll);
    window.addEventListener('resize', renderAll);
  </script>
</body>
</html>
""".replace('__ACTIVITIES_JSON__', json_str)

with open(target_html, 'w', encoding='utf-8') as f:
    f.write(html_code)

with open(dist_html, 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Successfully updated Section-Based X-Axis Time-Chainage Dashboard HTML!")
