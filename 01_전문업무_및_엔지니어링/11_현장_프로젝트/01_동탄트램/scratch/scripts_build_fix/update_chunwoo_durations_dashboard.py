import openpyxl, json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

target_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'
dist_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\index.html'

json_act_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\parsed_activities.json'
json_split_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\section_splits.json'
json_dur_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\chunwoo_durations.json'

with open(json_act_path, 'r', encoding='utf-8') as f:
    activities_data = json.load(f)

with open(json_split_path, 'r', encoding='utf-8') as f:
    splits_data = json.load(f)

with open(json_dur_path, 'r', encoding='utf-8') as f:
    chunwoo_durations = json.load(f)

def classify_work_3cat(text):
    t = str(text).lower()
    if '포장' in t or '아스팔트' in t or '기층' in t or '표층' in t or '동상방지' in t:
        return '포장', '#0284c7' # Blue
    elif '궤도' in t or '레일' in t or '도상' in t or '용접' in t or 'hsb' in t or 'tcl' in t:
        return '궤도', '#16a34a' # Green
    else:
        return '노반', '#ea580c' # Orange

# Bind durations & 3-work-category to splits
for item in splits_data:
    item['splitGroup'] = str(item.get('splitGroup', '')).replace('\n', ' ').replace('  ', ' ').strip()
    sec_name = str(item.get('sectionName', '')).replace('\n', ' ').replace('  ', ' ').strip()
    item['sectionName'] = sec_name
    
    w_cat, w_col = classify_work_3cat(sec_name + ' ' + item['splitGroup'])
    item['workCategory'] = w_cat
    item['workColor'] = w_col

    # Attach Chunwoo CM duration data
    dur_info = chunwoo_durations.get(sec_name, {})
    item['novanDays'] = dur_info.get('novanDays', 20)
    item['gwedoDays'] = dur_info.get('gwedoDays', 30)
    item['pojangDays'] = dur_info.get('pojangDays', 10)
    item['totalDays'] = dur_info.get('totalDays', item['novanDays'] + item['gwedoDays'] + item['pojangDays'])

for act in activities_data:
    act_ades = str(act.get('ades', ''))
    matched_grp = '일반부지 1구간'
    for sp in splits_data:
        if sp.get('zone') == act.get('zone') and (sp.get('sectionName') in act_ades or act_ades in sp.get('sectionName')):
            matched_grp = sp.get('splitGroup')
            break
    act['splitGroup'] = matched_grp
    w_cat, w_col = classify_work_3cat(act_ades)
    act['workCategory'] = w_cat
    act['workColor'] = w_col

act_json_str = json.dumps(activities_data, ensure_ascii=False)
split_json_str = json.dumps(splits_data, ensure_ascii=False)

html_code = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>동탄트램 Time-Chainage 대시보드 (㈜천우씨엠 노반/궤도/포장 소요일수 맵핑)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-main: #f8fafc;
      --bg-panel: #ffffff;
      --bg-sub: #f1f5f9;
      --border: #cbd5e1;
      --border-dark: #94a3b8;
      --text-main: #0f172a;
      --text-sub: #334155;
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
      overflow-x: hidden; overflow-y: auto;
    }

    .app-header {
      height: 56px; background: #ffffff;
      border-bottom: 1px solid var(--border);
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 1.25rem; box-shadow: var(--shadow-sm); z-index: 10;
    }
    .brand-title {
      font-size: 1.05rem; font-weight: 700; color: #1e3a8a;
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

    .btn-viewmode {
      background: #e0e7ff; color: #3730a3; border: 1px solid #c7d2fe;
      padding: 5px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 700;
      cursor: pointer; transition: all 0.15s;
    }
    .btn-viewmode:hover, .btn-viewmode.active { background: #4338ca; color: #ffffff; border-color: #4338ca; }

    .btn-action {
      background: #ffffff; border: 1px solid var(--border-dark); color: var(--text-main);
      padding: 5px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 600;
      cursor: pointer; transition: all 0.15s; display: flex; align-items: center; gap: 6px;
    }
    .btn-action:hover { background: var(--bg-sub); border-color: var(--primary); color: var(--primary); }

    .app-layout {
      min-height: calc(100vh - 56px); height: calc(100vh - 56px); display: flex; width: 100vw;
    }

    .v-filter-tray {
      width: 240px; background: #ffffff; border-right: 1px solid var(--border);
      display: flex; flex-direction: column; overflow: hidden; min-height: 550px;
    }
    .tray-header {
      padding: 0.75rem 1rem; border-bottom: 1px solid var(--border);
      background: #f8fafc; font-size: 0.85rem; font-weight: 700; color: #1e3a8a;
      display: flex; justify-content: space-between; align-items: center;
    }
    .btn-tray-reset {
      font-size: 0.7rem; background: #ffffff; border: 1px solid var(--border-dark);
      padding: 2px 6px; border-radius: 4px; cursor: pointer; color: var(--text-sub); font-weight: 600;
    }
    .btn-tray-reset:hover { background: var(--bg-sub); color: var(--primary); }

    .tray-quick-cats {
      display: flex; flex-wrap: wrap; border-bottom: 1px solid var(--border); background: var(--bg-sub);
    }
    .cat-tab {
      padding: 5px 8px; text-align: center; font-size: 0.72rem; font-weight: 600;
      cursor: pointer; color: var(--text-muted); border-bottom: 2px solid transparent; transition: all 0.15s; flex: 1; min-width: 45px;
    }
    .cat-tab.active { color: #1e3a8a; font-weight: 700; border-bottom-color: #1e3a8a; background: #ffffff; }

    .tray-scroll {
      flex: 1; overflow-y: auto; padding: 0.5rem; display: flex; flex-direction: column; gap: 4px; min-height: 420px;
    }

    .v-sec-item {
      display: flex; align-items: center; gap: 8px; padding: 7px 10px;
      border: 1px solid var(--border); border-radius: 6px; font-size: 0.8rem;
      cursor: pointer; transition: all 0.15s; background: #ffffff; user-select: none;
    }
    .v-sec-item:hover { border-color: var(--primary); background: var(--primary-light); }
    .v-sec-item.active { border-color: #2563eb; background: #dbeafe; font-weight: 700; color: #1e40af; }
    .v-sec-checkbox { width: 14px; height: 14px; accent-color: #2563eb; cursor: pointer; }

    .sidebar {
      width: 320px; background: var(--bg-panel);
      border-right: 1px solid var(--border);
      display: flex; flex-direction: column; overflow: hidden; min-height: 550px;
    }
    .sidebar-header {
      padding: 0.8rem 1rem; border-bottom: 1px solid var(--border);
      display: flex; flex-direction: column; gap: 8px; background: #f8fafc;
    }
    .sidebar-title { font-size: 0.88rem; font-weight: 700; color: var(--text-main); display: flex; justify-content: space-between; align-items: center; }
    
    .tree-toolbar { display: flex; justify-content: space-between; align-items: center; }
    .btn-tree-tool {
      font-size: 0.73rem; background: #ffffff; border: 1px solid var(--border-dark);
      padding: 3px 8px; border-radius: 4px; cursor: pointer; color: var(--text-sub); font-weight: 600;
    }
    .btn-tree-tool:hover { background: var(--bg-sub); color: var(--primary); }

    .search-input {
      width: 100%; padding: 6px 10px; border: 1px solid var(--border-dark); border-radius: 6px;
      font-size: 0.78rem; outline: none; transition: border 0.15s;
    }
    .search-input:focus { border-color: var(--primary); }

    .wbs-scroll { flex: 1; overflow-y: auto; padding: 0.75rem 1rem; display: flex; flex-direction: column; gap: 8px; min-height: 420px; }

    .split-group-card {
      background: #ffffff; border: 1px solid var(--border-dark); border-radius: 8px;
      overflow: hidden; box-shadow: var(--shadow-sm); transition: border-color 0.2s;
    }
    .split-group-card.active { border-color: var(--primary); }
    .group-header {
      background: #f1f5f9; padding: 9px 11px; font-size: 0.83rem; font-weight: 700;
      color: #1e3a8a; display: flex; justify-content: space-between; align-items: center;
      cursor: pointer; user-select: none; transition: background 0.15s;
    }
    .group-header:hover { background: #e2e8f0; }
    .group-title-box { display: flex; align-items: center; gap: 6px; }
    .toggle-icon { font-size: 0.75rem; color: #64748b; transition: transform 0.2s; }
    .split-group-card.expanded .toggle-icon { transform: rotate(90deg); }
    
    .group-body { display: none; padding: 6px 8px; background: #ffffff; flex-direction: column; gap: 4px; border-top: 1px solid var(--border); }
    .split-group-card.expanded .group-body { display: flex; }

    .sub-sec-item {
      background: var(--bg-sub); border: 1px solid var(--border); border-radius: 6px;
      padding: 6px 10px; font-size: 0.78rem; cursor: pointer; transition: all 0.15s;
    }
    .sub-sec-item:hover { border-color: var(--primary); background: #ffffff; }
    .sub-sec-item.selected { border-color: #2563eb; background: var(--primary-light); font-weight: 700; }
    .sub-sec-head { display: flex; justify-content: space-between; align-items: center; color: #0f172a; }
    .sub-sec-info { font-size: 0.71rem; color: var(--text-muted); margin-top: 2px; }

    .main-view {
      flex: 1; display: flex; flex-direction: column; padding: 1rem; gap: 1rem;
      background: var(--bg-main); overflow: hidden; min-height: 550px;
    }

    .chart-box {
      flex: 1; background: var(--bg-panel); border: 1px solid var(--border);
      border-radius: 10px; display: flex; flex-direction: column; padding: 1rem;
      box-shadow: var(--shadow-sm); position: relative; min-height: 480px; height: 100%;
    }
    .chart-topbar {
      display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;
    }
    .chart-title-text { font-size: 0.95rem; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 8px; }
    .zoom-controls { display: flex; gap: 4px; align-items: center; }
    .btn-zoom { background: #ffffff; border: 1px solid var(--border-dark); border-radius: 4px; padding: 3px 8px; font-size: 0.75rem; font-weight: 700; cursor: pointer; }
    .btn-zoom:hover { background: var(--bg-sub); border-color: var(--primary); }

    .legend-bar {
      display: flex; align-items: center; gap: 14px; background: #ffffff;
      border: 1px solid var(--border-dark); border-radius: 8px; padding: 6px 14px;
      font-size: 0.78rem; font-weight: 600; box-shadow: var(--shadow-sm); margin-top: 4px; flex-wrap: wrap;
    }
    .legend-item { display: flex; align-items: center; gap: 6px; }
    .legend-badge {
      width: 14px; height: 14px; border-radius: 4px; display: inline-block;
    }
    .badge-sub { background: #ea580c; border: 1px solid #c2410c; }
    .badge-track { background: #16a34a; border: 1px solid #15803d; }
    .badge-pave { background: #0284c7; border: 1px solid #0369a1; }

    .svg-wrapper {
      flex: 1; width: 100%; height: 100%; position: relative; min-height: 440px; height: 440px; background: #ffffff;
      border: 1.8px solid #94a3b8; border-radius: 6px; overflow: hidden;
    }
    svg { width: 100%; height: 100%; display: block; min-height: 440px; }

    .tooltip-card {
      position: absolute; pointer-events: none; display: none;
      background: rgba(15, 23, 42, 0.94); border: 1px solid #38bdf8;
      border-radius: 6px; padding: 8px 12px; font-size: 0.78rem;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3); z-index: 100; color: #ffffff;
      line-height: 1.4; backdrop-filter: blur(4px); max-width: 340px;
    }
    .tooltip-title { font-weight: 700; color: #38bdf8; font-size: 0.84rem; margin-bottom: 2px; }

    .modal-overlay {
      position: fixed; inset: 0; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(3px);
      display: none; justify-content: center; align-items: center; z-index: 1000;
    }
    .modal-card {
      background: #ffffff; border-radius: 12px; width: 540px; max-width: 90vw;
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

    .summary-bar {
      height: 44px; background: var(--bg-panel); border: 1px solid var(--border);
      border-radius: 6px; display: flex; align-items: center; padding: 0 1.25rem; justify-content: space-between;
      font-size: 0.8rem; box-shadow: var(--shadow-sm); flex-wrap: wrap; gap: 8px;
    }
    .stat-pill { display: flex; align-items: center; gap: 6px; color: var(--text-sub); }
    .stat-pill strong { color: #1e3a8a; font-weight: 700; }
  </style>
</head>
<body>

  <!-- 헤더 -->
  <header class="app-header">
    <div class="brand-title">
      📍 동탄도시철도 트램 Time-Chainage 대시보드
      <span class="brand-tag" id="stat-filter-label">㈜천우씨엠 노반/궤도/포장 소요일수 맵핑</span>
    </div>
    <div class="header-controls">
      <button class="btn-zone active" id="btn-zone-all" onclick="setZoneFilter('ALL')">전체 노선 (0~20.5km)</button>
      <button class="btn-zone" id="btn-zone-1g" onclick="setZoneFilter('1공구')">1공구</button>
      <button class="btn-zone" id="btn-zone-2g" onclick="setZoneFilter('2공구')">2공구</button>
      
      <div style="width: 1px; height: 16px; background: var(--border-dark); margin: 0 4px;"></div>
      
      <button class="btn-viewmode active" id="btn-view-splits" onclick="setViewMode('SPLITS')">🗺️ 시공구간 대표 뷰</button>
      <button class="btn-viewmode" id="btn-view-acts" onclick="setViewMode('ACTS')">📈 513개 액티비티 뷰</button>
      <button class="btn-action" onclick="resetZoom()">🌐 전체 뷰 리셋</button>
      <button class="btn-action" onclick="window.print()">🖨️ 인쇄</button>
    </div>
  </header>

  <!-- 메인 3열 레이아웃 -->
  <div class="app-layout">
    
    <!-- 1열: 세로형 시공구간 필터 트레이 -->
    <aside class="v-filter-tray">
      <div class="tray-header">
        <span>📌 세로형 시공구간 선택</span>
        <button class="btn-tray-reset" onclick="resetSelectedSplits()">전체 해제</button>
      </div>

      <div class="tray-quick-cats">
        <div class="cat-tab active" id="cat-tab-all" onclick="setCategoryTab('ALL')">전체</div>
        <div class="cat-tab" id="cat-tab-gen" onclick="setCategoryTab('일반부지')">일반부지</div>
        <div class="cat-tab" id="cat-tab-tram" onclick="setCategoryTab('트램부지')">트램부지</div>
      </div>

      <div class="tray-scroll" id="v-tray-scroll"></div>
    </aside>

    <!-- 2열: 아코디언 트리 사이드바 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="sidebar-title">
          <span>📋 시공구간 계층 목차</span>
          <div class="tree-toolbar">
            <button class="btn-tree-tool" onclick="expandAllGroups()">📂 펼치기</button>
            <button class="btn-tree-tool" onclick="collapseAllGroups()">📁 접기</button>
          </div>
        </div>
        <input type="text" class="search-input" id="search-input" placeholder="시공구간 명칭 검색..." oninput="onSearchChange(this.value)" />
      </div>

      <div class="wbs-scroll" id="wbs-tree-container"></div>
    </aside>

    <!-- 3열: 메인 차트 뷰 -->
    <main class="main-view">
      <div class="chart-box">
        <div class="chart-topbar">
          <div style="display:flex; flex-direction:column; gap:4px; width:100%;">
            <div class="chart-title-text" id="chart-title-text">
              📍 Time-Chainage 2D 다이어그램 (선택 구간 화면 100% 줌인 뷰)
            </div>

            <!-- ㈜천우씨엠 3대 핵심 공종 색상 범례 (시스템 공정 제외) -->
            <div class="legend-bar">
              <span style="color:#1e3a8a; font-weight:700;">🏷️ ㈜천우씨엠 공기산출 3대 공종 범례:</span>
              <div class="legend-item"><span class="legend-badge badge-sub"></span> <span><strong>🟠 노반 공사</strong> (토공/구조물/다짐)</span></div>
              <div class="legend-item"><span class="legend-badge badge-track"></span> <span><strong>🟢 궤도 공사</strong> (레일/HSB/TCL도상)</span></div>
              <div class="legend-item"><span class="legend-badge badge-pave"></span> <span><strong>🟦 포장 공사</strong> (아스팔트/기층/표층)</span></div>
              <span style="font-size:0.72rem; color:#64748b; margin-left:auto;">※ 시스템 공정은 산정 미완료로 제외</span>
            </div>
          </div>

          <div class="zoom-controls" style="margin-left: 10px;">
            <button class="btn-zoom" onclick="zoomGraph(1.25)">🔍 확대 (+)</button>
            <button class="btn-zoom" onclick="zoomGraph(0.8)">🔍 축소 (-)</button>
            <button class="btn-zoom" onclick="resetZoom()">🔄 전체 리셋</button>
          </div>
        </div>

        <div class="svg-wrapper" id="svg-wrapper">
          <svg id="tc-svg"></svg>
          <div class="tooltip-card" id="tooltip"></div>
        </div>
      </div>

      <!-- 요약바 -->
      <div class="summary-bar">
        <div class="stat-pill">표출 시공구간: <strong id="stat-group-count">28개 구간</strong></div>
        <div class="stat-pill">표출 범위: <strong id="stat-range-label">STA 0.0km ~ 20.5km (전체)</strong></div>
        <div class="stat-pill">소요일수 맵핑: 
          <strong style="color:#ea580c;">🟠 노반</strong> | 
          <strong style="color:#16a34a;">🟢 궤도</strong> | 
          <strong style="color:#0284c7;">🟦 포장</strong>
        </div>
        <div class="stat-pill">목표완공: <strong>2031년 11월 30일</strong></div>
      </div>
    </main>

  </div>

  <!-- 상세 모달 -->
  <div class="modal-overlay" id="modal-overlay" onclick="closeModal(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <div class="modal-header">
        <div class="modal-title">
          <span>📑 ㈜천우씨엠 시공구간별 3대 공종 소요일수 산출 근거</span>
        </div>
        <button class="modal-close" onclick="closeModal()">✕</button>
      </div>
      <div class="modal-body" id="modal-body">
      </div>
    </div>
  </div>

  <script>
    const RAW_ACTIVITIES = __ACTIVITIES_JSON__;
    const SECTION_SPLITS = __SPLITS_JSON__;

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

    let currentZone = 'ALL';
    let currentCategoryTab = 'ALL';
    let selectedSplitKeys = new Set();
    let currentViewMode = 'SPLITS';
    let searchQuery = '';
    let zoomLevel = 1.0;

    let expandedGroups = new Set();
    let selectedSubSec = null;

    const wrapper = document.getElementById('svg-wrapper');
    const trayScroll = document.getElementById('v-tray-scroll');
    const treeContainer = document.getElementById('wbs-tree-container');
    const svg = document.getElementById('tc-svg');
    const tooltip = document.getElementById('tooltip');

    function safeStr(val) {
      return (val === null || val === undefined) ? '' : String(val);
    }

    function dateToYear(dStr) {
      if (!dStr) return 2028.0;
      const parts = String(dStr).split('-');
      if (parts.length < 3) return 2028.0;
      const y = parseInt(parts[0]) || 2028;
      const m = (parseInt(parts[1]) || 1) - 1;
      const d = parseInt(parts[2]) || 1;
      return y + (m / 12) + (d / 365);
    }

    function renderVerticalFilterTray() {
      if (!trayScroll) return;
      trayScroll.innerHTML = '';

      const grpMap = new Map();
      SECTION_SPLITS.forEach(item => {
        const itemZone = safeStr(item.zone);
        const itemGroup = safeStr(item.splitGroup);
        if (currentZone !== 'ALL' && itemZone !== currentZone) return;
        if (currentCategoryTab !== 'ALL' && !itemGroup.includes(currentCategoryTab)) return;
        
        const gKey = `${itemZone}_${itemGroup}`;
        if (!grpMap.has(gKey)) {
          grpMap.set(gKey, { zone: itemZone, groupName: itemGroup, count: 0 });
        }
        grpMap.get(gKey).count += 1;
      });

      const allItem = document.createElement('div');
      const isAllSelected = selectedSplitKeys.size === 0;
      allItem.className = `v-sec-item ${isAllSelected ? 'active' : ''}`;
      allItem.innerHTML = `
        <input type="checkbox" class="v-sec-checkbox" ${isAllSelected ? 'checked' : ''} readonly />
        <span>🌐 전체 시공구간 (All)</span>
      `;
      allItem.onclick = () => {
        selectedSplitKeys.clear();
        selectedSubSec = null;
        renderAll();
      };
      trayScroll.appendChild(allItem);

      Array.from(grpMap.entries()).sort().forEach(([gKey, gInfo]) => {
        const isSelected = selectedSplitKeys.has(gKey);
        const itemEl = document.createElement('div');
        itemEl.className = `v-sec-item ${isSelected ? 'active' : ''}`;
        itemEl.innerHTML = `
          <input type="checkbox" class="v-sec-checkbox" ${isSelected ? 'checked' : ''} readonly />
          <span>[${gInfo.zone}] ${gInfo.groupName}</span>
        `;
        itemEl.onclick = () => {
          if (selectedSplitKeys.has(gKey)) {
            selectedSplitKeys.delete(gKey);
          } else {
            selectedSplitKeys.add(gKey);
            expandedGroups.add(gKey);
          }
          selectedSubSec = null;
          renderAll();
        };
        trayScroll.appendChild(itemEl);
      });
    }

    function resetSelectedSplits() {
      selectedSplitKeys.clear();
      selectedSubSec = null;
      renderAll();
    }

    function setCategoryTab(cat) {
      currentCategoryTab = cat;
      document.querySelectorAll('.cat-tab').forEach(t => t.classList.remove('active'));
      if (cat === 'ALL') document.getElementById('cat-tab-all')?.classList.add('active');
      if (cat === '일반부지') document.getElementById('cat-tab-gen')?.classList.add('active');
      if (cat === '트램부지') document.getElementById('cat-tab-tram')?.classList.add('active');
      renderAll();
    }

    function getGroupedSplits() {
      const groups = {};
      const query = safeStr(searchQuery).toLowerCase();

      SECTION_SPLITS.forEach(item => {
        const itemZone = safeStr(item.zone);
        const itemGroup = safeStr(item.splitGroup);
        const itemSec = safeStr(item.sectionName);

        if (currentZone !== 'ALL' && itemZone !== currentZone) return;
        if (currentCategoryTab !== 'ALL' && !itemGroup.includes(currentCategoryTab)) return;

        const gKey = `${itemZone}_${itemGroup}`;
        if (selectedSplitKeys.size > 0 && !selectedSplitKeys.has(gKey)) return;

        if (!groups[gKey]) {
          groups[gKey] = {
            zone: itemZone,
            groupName: itemGroup,
            items: []
          };
        }
        if (!query || itemSec.toLowerCase().includes(query) || itemGroup.toLowerCase().includes(query)) {
          groups[gKey].items.push(item);
        }
      });
      return Object.values(groups).filter(g => g.items.length > 0);
    }

    function renderSectionTree() {
      if (!treeContainer) return;
      treeContainer.innerHTML = '';
      
      let groups = getGroupedSplits();
      if (groups.length === 0) {
        groups = SECTION_SPLITS_TO_GROUPS(SECTION_SPLITS);
      }

      const grpCntEl = document.getElementById('stat-group-count');
      if (grpCntEl) grpCntEl.innerText = `${groups.length}개 구간`;

      const fltLblEl = document.getElementById('stat-filter-label');
      if (fltLblEl) fltLblEl.innerText = selectedSplitKeys.size > 0 ? `${selectedSplitKeys.size}개 선택됨` : '㈜천우씨엠 노반/궤도/포장 소요일수 맵핑';

      groups.forEach(g => {
        const gKey = `${g.zone}_${g.groupName}`;
        const isExpanded = expandedGroups.has(gKey) || selectedSplitKeys.has(gKey) || selectedSplitKeys.size === 0;

        const card = document.createElement('div');
        card.className = `split-group-card ${isExpanded ? 'expanded' : ''} ${selectedSplitKeys.has(gKey) ? 'active' : ''}`;
        
        const header = document.createElement('div');
        header.className = 'group-header';
        header.innerHTML = `
          <div class="group-title-box">
            <span class="toggle-icon">▶</span>
            <span>[${g.zone}] ${g.groupName}</span>
          </div>
          <span style="font-size:0.7rem; background:#dbeafe; color:#1e40af; padding:1px 6px; border-radius:4px;">${g.items.length}개 항목</span>
        `;
        header.onclick = () => {
          if (expandedGroups.has(gKey)) {
            expandedGroups.delete(gKey);
          } else {
            expandedGroups.add(gKey);
          }
          renderSectionTree();
        };

        const body = document.createElement('div');
        body.className = 'group-body';

        g.items.forEach(sec => {
          const secName = safeStr(sec.sectionName);
          const isSelected = selectedSubSec?.sectionName === secName;
          const itemEl = document.createElement('div');
          itemEl.className = `sub-sec-item ${isSelected ? 'selected' : ''}`;
          
          const nD = sec.novanDays || 20;
          const gD = sec.gwedoDays || 30;
          const pD = sec.pojangDays || 10;
          const totD = sec.totalDays || (nD + gD + pD);

          itemEl.innerHTML = `
            <div class="sub-sec-head">
              <span>${secName}</span>
              <span style="font-size:0.7rem; color:#1e40af; font-weight:700;">총 ${totD}일</span>
            </div>
            <div class="sub-sec-info">🟠노반:${nD}일 | 🟢궤도:${gD}일 | 🟦포장:${pD}일</div>
          `;
          itemEl.onclick = () => {
            selectedSubSec = sec;
            openModalForSection(sec);
            renderAll();
          };
          body.appendChild(itemEl);
        });

        card.appendChild(header);
        card.appendChild(body);
        treeContainer.appendChild(card);
      });
    }

    // 3열: ㈜천우씨엠 3대 핵심 공종 소요일수 2D SVG 다이어그램
    function renderSVG() {
      if (!svg || !wrapper) return;
      
      const rect = wrapper.getBoundingClientRect();
      const rawW = rect.width > 300 ? rect.width : (window.innerWidth - 600);
      const rawH = rect.height > 300 ? rect.height : (window.innerHeight - 150);

      const width = Math.max(950, rawW) * zoomLevel;
      const height = Math.max(520, rawH);
      
      svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
      svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');

      const padL = 85, padR = 50, padT = 50, padB = 70;
      const graphW = width - padL - padR;
      const graphH = height - padT - padB;

      const groups = getGroupedSplits();

      let minKm = 0.0, maxKm = 20.5;
      
      if (selectedSubSec) {
        const sKm = (parseFloat(selectedSubSec.startM) || 0) / 1000.0;
        const eKm = (parseFloat(selectedSubSec.endM) || 0) / 1000.0;
        const span = Math.max(0.3, eKm - sKm);
        minKm = Math.max(0.0, sKm - (span * 0.3));
        maxKm = Math.min(20.5, eKm + (span * 0.3));
      } else if (groups.length > 0 && selectedSplitKeys.size > 0) {
        let allStarts = [], allEnds = [];
        groups.forEach(g => {
          g.items.forEach(it => {
            allStarts.push((parseFloat(it.startM) || 0) / 1000.0);
            allEnds.push((parseFloat(it.endM) || 0) / 1000.0);
          });
        });
        if (allStarts.length > 0 && allEnds.length > 0) {
          const realMin = Math.min(...allStarts);
          const realMax = Math.max(...allEnds);
          const span = Math.max(0.5, realMax - realMin);
          minKm = Math.max(0.0, realMin - (span * 0.2));
          maxKm = Math.min(20.5, realMax + (span * 0.2));
        }
      }

      const rangeLblEl = document.getElementById('stat-range-label');
      if (rangeLblEl) rangeLblEl.innerText = `STA ${minKm.toFixed(2)}km ~ ${maxKm.toFixed(2)}km`;

      const minYr = 2027.0, maxYr = 2032.0;

      const getX = (km) => padL + ((km - minKm) / (maxKm - minKm)) * graphW;
      const getY = (yr) => padT + graphH - ((yr - minYr) / (maxYr - minYr)) * graphH;

      let html = '';

      // 0. 차트 외곽 그리드 테두리 박스
      html += `<rect x="${padL}" y="${padT}" width="${graphW}" height="${graphH}" fill="#ffffff" stroke="#64748b" stroke-width="2" rx="4"/>`;

      // 1. Y축 연도 격자선 (2027.0년 ~ 2032.0년)
      for (let yr = 2027.0; yr <= 2032; yr += 0.5) {
        const y = getY(yr);
        html += `<line x1="${padL}" y1="${y}" x2="${width - padR}" y2="${y}" stroke="#cbd5e1" stroke-dasharray="4,4" stroke-width="1"/>`;
        html += `<text x="${padL - 12}" y="${y + 4}" fill="#334155" font-size="11" font-weight="700" text-anchor="end">${yr.toFixed(1)}년</text>`;
      }

      // 2. X축 정거장 가이드선 및 라벨
      STATIONS.forEach((st) => {
        if (st.km >= minKm - 0.1 && st.km <= maxKm + 0.1) {
          const x = getX(st.km);
          html += `<line x1="${x}" y1="${padT}" x2="${x}" y2="${height - padB}" stroke="#cbd5e1" stroke-dasharray="2,2" stroke-width="1.2"/>`;
          html += `<text x="${x}" y="${height - padB + 22}" fill="#0f172a" font-size="11" font-weight="700" text-anchor="end" transform="rotate(-35, ${x}, ${height - padB + 22})">${st.name}</text>`;
        }
      });

      // 3. ㈜천우씨엠 3대 핵심 공종(노반, 궤도, 포장) 소요일수 공정선 표출
      if (currentViewMode === 'SPLITS') {
        const targetSplitsToDraw = (groups.length > 0) ? groups : SECTION_SPLITS_TO_GROUPS(SECTION_SPLITS);

        let labelIdx = 0;
        targetSplitsToDraw.forEach((g, gIdx) => {
          g.items.forEach((item, itemIdx) => {
            const startKm = ((parseFloat(item.startM) || 0) / 1000.0);
            const endKm = ((parseFloat(item.endM) || 0) / 1000.0);

            const x1 = getX(startKm);
            const x2 = getX(endKm > startKm ? endKm : startKm + 0.35);
            
            const startYr = 2027.6 + ((gIdx % 6) * 0.5) + ((itemIdx % 5) * 0.08);
            const endYr = startYr + 0.65;

            const y1 = getY(startYr);
            const y2 = getY(endYr);

            const secName = safeStr(item.sectionName);
            const grpName = safeStr(item.splitGroup);
            const isSelected = selectedSubSec?.sectionName === secName;

            const nD = item.novanDays || 20;
            const gD = item.gwedoDays || 30;
            const pD = item.pojangDays || 10;
            const totD = item.totalDays || (nD + gD + pD);
            const color = item.workColor || '#ea580c';

            // 시공구간 반투명 배경 밴드
            html += `<rect x="${Math.min(x1, x2)}" y="${padT}" width="${Math.max(5, Math.abs(x2 - x1))}" height="${graphH}" fill="${color}" opacity="${isSelected ? 0.35 : 0.15}"/>`;
            
            // 공종 전용 색상 공정선
            html += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${isSelected ? 9 : 6}" stroke-linecap="round" class="split-line" data-grp="${grpName}" data-sec="${secName}" data-cat="${item.workCategory || '노반'}" data-nd="${nD}" data-gd="${gD}" data-pd="${pD}" data-tot="${totD}" data-dist="${item.distM || 0}" data-sy="${startYr.toFixed(1)}" data-ey="${endYr.toFixed(1)}" style="cursor:pointer; opacity:1; filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.2));"/>`;
            
            // 텍스트 라벨 지그재그 교차 배치
            const midX = (x1 + x2) / 2;
            const midY = (y1 + y2) / 2;
            const yOff = (labelIdx % 2 === 0) ? -16 : 20;

            html += `<g transform="translate(${midX}, ${midY + yOff})">`;
            html += `<rect x="-60" y="-12" width="120" height="20" fill="#ffffff" stroke="${color}" stroke-width="1.6" rx="4" opacity="0.95"/>`;
            html += `<text x="0" y="2" fill="#0f172a" font-size="10" font-weight="700" text-anchor="middle">${secName} (${totD}일)</text>`;
            html += `</g>`;

            labelIdx++;
          });
        });
      } else {
        // 513개 액티비티 뷰어
        RAW_ACTIVITIES.forEach((act, idx) => {
          const actZone = safeStr(act.zone);
          const actGrp = safeStr(act.splitGroup);
          if (currentZone !== 'ALL' && actZone !== currentZone) return;
          if (selectedSplitKeys.size > 0) {
            const gKey = `${actZone}_${actGrp}`;
            if (!selectedSplitKeys.has(gKey)) return;
          }

          const startY = dateToYear(act.es);
          const endY = dateToYear(act.ef);
          const isZone1 = actZone === '1공구';
          const startKm = isZone1 ? (idx % 12) * 0.65 : 4.2 + (idx % 25) * 0.65;
          const color = act.workColor || '#2563eb';

          if (startKm >= minKm - 0.5 && startKm <= maxKm + 0.5) {
            const x1 = getX(startKm);
            const x2 = getX(startKm + 0.6);
            const y1 = getY(startY);
            const y2 = getY(endY);
            html += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="3.5" stroke-linecap="round" opacity="0.85"/>`;
          }
        });
      }

      svg.innerHTML = html;

      // 마우스 이벤트
      document.querySelectorAll('.split-line').forEach(el => {
        el.addEventListener('mouseenter', (e) => {
          if (!tooltip) return;
          tooltip.style.display = 'block';
          tooltip.innerHTML = `
            <div class="tooltip-title">[${e.target.dataset.grp}] ${e.target.dataset.sec}</div>
            <div>대표공종: <b>${e.target.dataset.cat}</b> | 연장: <b>${e.target.dataset.dist}m</b></div>
            <div style="margin-top:4px; padding-top:4px; border-top:1px solid #38bdf840; color:#38bdf8;">
              <b>📊 ㈜천우씨엠 산출 공기 (총 ${e.target.dataset.tot}일):</b><br/>
              - 🟠 노반 공사: <b>${e.target.dataset.nd}일</b><br/>
              - 🟢 궤도 공사: <b>${e.target.dataset.gd}일</b><br/>
              - 🟦 포장 공사: <b>${e.target.dataset.pd}일</b>
            </div>
          `;
        });
        el.addEventListener('mousemove', (e) => {
          if (!tooltip) return;
          const cRect = svg.getBoundingClientRect();
          tooltip.style.left = (e.clientX - cRect.left + 15) + 'px';
          tooltip.style.top = (e.clientY - cRect.top + 15) + 'px';
        });
        el.addEventListener('mouseleave', () => {
          if (tooltip) tooltip.style.display = 'none';
        });
      });
    }

    function SECTION_SPLITS_TO_GROUPS(splits) {
      const groups = {};
      splits.forEach(item => {
        const itemZone = safeStr(item.zone);
        const itemGroup = safeStr(item.splitGroup);
        const gKey = `${itemZone}_${itemGroup}`;
        if (!groups[gKey]) {
          groups[gKey] = { zone: itemZone, groupName: itemGroup, items: [] };
        }
        groups[gKey].items.push(item);
      });
      return Object.values(groups);
    }

    function renderAll() {
      try {
        renderVerticalFilterTray();
        renderSectionTree();
        renderSVG();
      } catch (err) {
        console.error("renderAll Exception caught:", err);
      }
    }

    function setZoneFilter(zone) {
      currentZone = zone;
      selectedSplitKeys.clear();
      selectedSubSec = null;
      document.querySelectorAll('.btn-zone').forEach(btn => btn.classList.remove('active'));
      if (zone === 'ALL') document.getElementById('btn-zone-all')?.classList.add('active');
      if (zone === '1공구') document.getElementById('btn-zone-1g')?.classList.add('active');
      if (zone === '2공구') document.getElementById('btn-zone-2g')?.classList.add('active');
      renderAll();
    }

    function setViewMode(mode) {
      currentViewMode = mode;
      document.querySelectorAll('.btn-viewmode').forEach(btn => btn.classList.remove('active'));
      if (mode === 'SPLITS') document.getElementById('btn-view-splits')?.classList.add('active');
      if (mode === 'ACTS') document.getElementById('btn-view-acts')?.classList.add('active');
      renderAll();
    }

    function expandAllGroups() {
      SECTION_SPLITS.forEach(item => expandedGroups.add(`${safeStr(item.zone)}_${safeStr(item.splitGroup)}`));
      renderSectionTree();
    }

    function collapseAllGroups() {
      expandedGroups.clear();
      renderSectionTree();
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
      selectedSplitKeys.clear();
      selectedSubSec = null;
      renderAll();
    }

    function openModalForSection(sec) {
      const modal = document.getElementById('modal-overlay');
      const body = document.getElementById('modal-body');
      if (!modal || !body) return;

      const secName = safeStr(sec.sectionName);
      const grpName = safeStr(sec.splitGroup);

      const nD = sec.novanDays || 20;
      const gD = sec.gwedoDays || 30;
      const pD = sec.pojangDays || 10;
      const totD = sec.totalDays || (nD + gD + pD);
      
      body.innerHTML = `
        <div style="font-size:1.05rem; font-weight:700; color:#1e3a8a; border-bottom:2px solid #e2e8f0; padding-bottom:8px;">
          ${secName} (${grpName})
        </div>
        <div class="detail-grid">
          <div class="detail-item"><div class="detail-label">시공 공구</div><div class="detail-value">${safeStr(sec.zone)}</div></div>
          <div class="detail-item"><div class="detail-label">대표 공종</div><div class="detail-value" style="color:${sec.workColor || '#ea580c'};">${sec.workCategory || '노반'}</div></div>
          <div class="detail-item"><div class="detail-label">구간 시점 (Start STA)</div><div class="detail-value">STA ${sec.startM || 0} m</div></div>
          <div class="detail-item"><div class="detail-label">구간 종점 (End STA)</div><div class="detail-value">STA ${sec.endM || 0} m</div></div>
          <div class="detail-item"><div class="detail-label">시공 연장 (Distance)</div><div class="detail-value">${sec.distM || 0} m</div></div>
          <div class="detail-item"><div class="detail-label">총 소요일수 (Total)</div><div class="detail-value" style="color:#1e40af; font-size:1.05rem;">총 ${totD} 일</div></div>
        </div>

        <div style="background:#eff6ff; padding:14px; border-radius:8px; border:1px solid #bfdbfe; display:flex; flex-direction:column; gap:8px;">
          <div style="font-weight:700; font-size:0.85rem; color:#1e3a8a;">📊 ㈜천우씨엠 3대 핵심 공종별 산출 소요일수</div>
          <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:8px; font-size:0.82rem; text-align:center;">
            <div style="background:#ffffff; padding:8px; border-radius:6px; border:1px solid #ea580c40;">
              <span style="color:#ea580c; font-weight:700;">🟠 노반 공사</span><br/>
              <strong style="font-size:1.1rem; color:#0f172a;">${nD} 일</strong>
            </div>
            <div style="background:#ffffff; padding:8px; border-radius:6px; border:1px solid #16a34a40;">
              <span style="color:#16a34a; font-weight:700;">🟢 궤도 공사</span><br/>
              <strong style="font-size:1.1rem; color:#0f172a;">${gD} 일</strong>
            </div>
            <div style="background:#ffffff; padding:8px; border-radius:6px; border:1px solid #0284c740;">
              <span style="color:#0284c7; font-weight:700;">🟦 포장 공사</span><br/>
              <strong style="font-size:1.1rem; color:#0f172a;">${pD} 일</strong>
            </div>
          </div>
          <div style="font-size:0.73rem; color:#64748b; margin-top:2px;">
            * 시스템 공정(전력·신호·통신)은 산정 미완료로 제외 처리되었습니다.
          </div>
        </div>
      `;

      modal.style.display = 'flex';
    }

    function closeModal() {
      const modal = document.getElementById('modal-overlay');
      if (modal) modal.style.display = 'none';
    }

    window.addEventListener('DOMContentLoaded', renderAll);
    window.addEventListener('load', renderAll);
    window.addEventListener('resize', renderAll);
  </script>
</body>
</html>
""".replace('__ACTIVITIES_JSON__', act_json_str).replace('__SPLITS_JSON__', split_json_str)

with open(target_html, 'w', encoding='utf-8') as f:
    f.write(html_code)

with open(dist_html, 'w', encoding='utf-8') as f:
    f.write(html_code)

print("✓ Successfully updated Chunwoo CM 3-Work-Category (Novan, Gwedo, Pojang) Duration Dashboard!")
