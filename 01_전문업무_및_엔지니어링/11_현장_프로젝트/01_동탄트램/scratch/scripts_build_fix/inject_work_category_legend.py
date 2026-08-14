import os, sys, json

sys.stdout.reconfigure(encoding='utf-8')

target_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'
dist_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\index.html'

with open(target_html, 'r', encoding='utf-8') as f:
    html = f.read()

# Add legend box CSS styles and legend UI components
legend_style = """
    /* 공종 범례 스타일 */
    .legend-bar {
      display: flex; align-items: center; gap: 14px; background: #ffffff;
      border: 1px solid var(--border-dark); border-radius: 8px; padding: 6px 14px;
      font-size: 0.78rem; font-weight: 600; box-shadow: var(--shadow-sm);
    }
    .legend-item { display: flex; align-items: center; gap: 6px; }
    .legend-badge {
      width: 14px; height: 14px; border-radius: 4px; display: inline-block;
    }
    .badge-red { background: #dc2626; border: 1px solid #b91c1c; }
    .badge-green { background: #16a34a; border: 1px solid #15803d; }
    .badge-blue { background: #2563eb; border: 1px solid #1d4ed8; }
"""

# Inject legend CSS if not present
if '.legend-bar' not in html:
    html = html.replace('</style>', legend_style + '\n</style>')

# Inject Legend Bar into Topbar & Chart Box
chart_topbar_old = '<div class="chart-title-text" id="chart-title-text">\n            📍 Time-Chainage 2D 다이어그램 (선택 구간 화면 100% 줌인 뷰)\n          </div>'
chart_topbar_new = """<div style="display:flex; flex-direction:column; gap:4px;">
            <div class="chart-title-text" id="chart-title-text">
              📍 Time-Chainage 2D 다이어그램 (선택 구간 화면 100% 줌인 뷰)
            </div>
            <!-- 공종 색상 범례 표시 (Work Category Legend) -->
            <div class="legend-bar">
              <span style="color:#1e3a8a; font-weight:700;">🏷️ 공종 색상 범례:</span>
              <div class="legend-item"><span class="legend-badge badge-red"></span> <span><strong>🔴 빨간색 선</strong>: 일반부지 공종 (토공·노반·상부강화노반)</span></div>
              <div class="legend-item"><span class="legend-badge badge-green"></span> <span><strong>🟢 초록색 선</strong>: 트램부지 공종 (궤도·전력·신호·시스템)</span></div>
              <div class="legend-item"><span class="legend-badge badge-blue"></span> <span><strong>🔵 파란색 선</strong>: 513개 세부 액티비티</span></div>
            </div>
          </div>"""

if '공종 색상 범례' not in html:
    html = html.replace(chart_topbar_old, chart_topbar_new)

# Update Summary Bar with Legend Info
summary_old = '<div class="stat-pill">목표완공: <strong>2031년 11월 30일</strong></div>'
summary_new = """<div class="stat-pill">범례: <strong style="color:#dc2626;">🔴 일반부지(토공/노반)</strong> | <strong style="color:#16a34a;">🟢 트램부지(궤도/시스템)</strong></div>
        <div class="stat-pill">목표완공: <strong>2031년 11월 30일</strong></div>"""

if '범례:' not in html:
    html = html.replace(summary_old, summary_new)

with open(target_html, 'w', encoding='utf-8') as f:
    f.write(html)

with open(dist_html, 'w', encoding='utf-8') as f:
    f.write(html)

print("✓ Successfully injected Work Category Color Legend bar into HTML dashboard!")
