import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_header_pattern = r'<header class="app-header">[\s\S]*?</header>'

clean_header_html = """<header class="app-header">
    <div class="brand-title">
      📍 동탄도시철도 트램 Time-Chainage 대시보드
      <span class="brand-tag" id="stat-filter-label">엑셀 노반합계·궤도합계·포장합계 컬럼 100% 연동</span>
    </div>
    <div class="header-controls" style="display: flex; gap: 0.4rem; align-items: center;">
      <!-- Main Dashboard View Mode Tabs -->
      <div class="main-tab-group" style="display: flex; gap: 0.3rem; background: rgba(15,23,42,0.6); padding: 0.25rem; border-radius: 8px; margin-right: 0.5rem;">
        <button class="btn-main-tab active" id="tab-main-tc" onclick="setMainTab('TC')" style="padding: 0.4rem 0.85rem; border: none; border-radius: 6px; font-size: 0.82rem; font-weight: 800; cursor: pointer; background: #0284c7; color: #ffffff; transition: all 0.2s;">
          📊 Time-Chainage 2D 공정표
        </button>
        <button class="btn-main-tab" id="tab-main-res" onclick="setMainTab('RESOURCE')" style="padding: 0.4rem 0.85rem; border: none; border-radius: 6px; font-size: 0.82rem; font-weight: 800; cursor: pointer; background: transparent; color: #94a3b8; transition: all 0.2s;">
          👷 자원 투입 & 최적화 (Resource Leveling)
        </button>
        <button class="btn-main-tab" id="tab-main-evm" onclick="setMainTab('EVM')" style="padding: 0.4rem 0.85rem; border: none; border-radius: 6px; font-size: 0.82rem; font-weight: 800; cursor: pointer; background: transparent; color: #94a3b8; transition: all 0.2s;">
          💰 투입비 추정 & EVM (S-Curve)
        </button>
      </div>

      <div style="width: 1px; height: 16px; background: var(--border-dark); margin: 0 4px;"></div>

      <button class="btn-zone active" id="btn-zone-all" onclick="setZoneFilter('ALL')">전체 노선 (0~20.5km)</button>
      <button class="btn-zone" id="btn-zone-1g" onclick="setZoneFilter('1공구')">1공구</button>
      <button class="btn-zone" id="btn-zone-2g" onclick="setZoneFilter('2공구')">2공구</button>
      
      <div style="width: 1px; height: 16px; background: var(--border-dark); margin: 0 4px;"></div>
      
      <button class="btn-viewmode active" id="btn-view-splits" onclick="setViewMode('SPLITS')">🗺️ 시공구간 대표 뷰</button>
      <button class="btn-viewmode" id="btn-view-acts" onclick="setViewMode('ACTS')">📈 513개 액티비티 뷰</button>
      <button class="btn-action" onclick="resetZoom()">🌐 리셋</button>
      <button class="btn-action" onclick="window.print()">🖨️ 인쇄</button>
    </div>
  </header>"""

if re.search(old_header_pattern, content):
    content = re.sub(old_header_pattern, clean_header_html, content, count=1)
    print("Deduplicated header buttons successfully!")

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished applying header deduplication to HTML!")
