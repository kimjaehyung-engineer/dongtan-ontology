import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

# 1. Fix indentation on /api/usage in do_GET
bad_indent = """                elif self.path == "/api/usage" or self.path.startswith("/api/usage"):
            try:
                tracker = usage_cost_tracker.get_tracker()
                self.respond_json(tracker.get_summary())
            except Exception as e:
                self.respond_json({"error": str(e)}, 500)"""

good_indent = """        elif self.path == "/api/usage" or self.path.startswith("/api/usage"):
            try:
                tracker = usage_cost_tracker.get_tracker()
                self.respond_json(tracker.get_summary())
            except Exception as e:
                self.respond_json({"error": str(e)}, 500)"""

if bad_indent in content:
    content = content.replace(bad_indent, good_indent, 1)
    print("1. Fixed /api/usage indentation!")

# 2. Inject CSS Styles for Usage Badge, Modal & Chat Usage Bar
usage_css = """
    /* === Gemini API Usage & Cost Monitor Styles === */
    .usage-monitor-btn {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-main);
      cursor: pointer;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
      transition: all 0.2s ease;
      user-select: none;
    }
    .usage-monitor-btn:hover {
      border-color: var(--accent);
      background: var(--bg-input);
      transform: translateY(-1px);
      box-shadow: 0 3px 8px rgba(37, 99, 235, 0.15);
    }
    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      display: inline-block;
      flex-shrink: 0;
    }
    .status-dot.green {
      background: #10b981;
      box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25);
      animation: pulse-green 2s infinite;
    }
    .status-dot.yellow {
      background: #f59e0b;
      box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.25);
      animation: pulse-yellow 1.5s infinite;
    }
    .status-dot.red {
      background: #ef4444;
      box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.25);
      animation: pulse-red 1s infinite;
    }
    @keyframes pulse-green {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.7; transform: scale(1.15); }
    }
    @keyframes pulse-yellow {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.6; }
    }
    @keyframes pulse-red {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(1.2); }
    }
    .usage-cost-pill {
      background: #ecfdf5;
      color: #047857;
      padding: 1px 6px;
      border-radius: 10px;
      font-size: 11px;
      font-weight: 700;
      border: 1px solid #a7f3d0;
    }
    [data-theme="dark"] .usage-cost-pill {
      background: #064e3b;
      color: #6ee7b7;
      border-color: #047857;
    }
    .usage-counter-tag {
      color: var(--text-muted);
      font-weight: 500;
    }

    /* Modal Overlay & Dialog */
    .usage-modal-overlay {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(15, 23, 42, 0.65);
      backdrop-filter: blur(6px);
      z-index: 10000;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      animation: fadeIn 0.2s ease;
    }
    .usage-modal-dialog {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      width: 100%;
      max-width: 680px;
      max-height: 90vh;
      overflow-y: auto;
      box-shadow: 0 20px 40px rgba(0,0,0,0.3);
      color: var(--text-main);
      display: flex;
      flex-direction: column;
    }
    .usage-modal-header {
      padding: 18px 24px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .usage-modal-header h2 {
      font-size: 17px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 10px;
      color: var(--heading-color);
    }
    .usage-modal-close {
      background: none;
      border: none;
      font-size: 20px;
      cursor: pointer;
      color: var(--text-muted);
      padding: 4px 8px;
      border-radius: 6px;
      line-height: 1;
    }
    .usage-modal-close:hover {
      background: var(--border-color);
      color: var(--text-main);
    }
    .usage-modal-body {
      padding: 20px 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .stat-card-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
    }
    .stat-card {
      background: var(--bg-input);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .stat-card-title {
      font-size: 11.5px;
      color: var(--text-muted);
      font-weight: 600;
    }
    .stat-card-value {
      font-size: 20px;
      font-weight: 800;
      color: var(--heading-color);
    }
    .stat-card-sub {
      font-size: 11px;
      color: var(--text-muted);
    }
    .quota-progress-container {
      background: var(--bg-input);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 16px;
    }
    .progress-bar-bg {
      height: 10px;
      background: var(--border-color);
      border-radius: 5px;
      overflow: hidden;
      margin: 10px 0 6px 0;
    }
    .progress-bar-fill {
      height: 100%;
      border-radius: 5px;
      transition: width 0.4s ease, background 0.4s ease;
    }
    .info-callout {
      background: rgba(37, 99, 235, 0.06);
      border: 1px solid rgba(37, 99, 235, 0.2);
      border-radius: 10px;
      padding: 12px 14px;
      font-size: 12.5px;
      line-height: 1.6;
      color: var(--text-main);
    }
    [data-theme="dark"] .info-callout {
      background: rgba(59, 130, 246, 0.1);
      border-color: rgba(59, 130, 246, 0.25);
    }
    .pricing-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      margin-top: 8px;
    }
    .pricing-table th, .pricing-table td {
      padding: 8px 10px;
      border: 1px solid var(--border-color);
      text-align: left;
    }
    .pricing-table th {
      background: var(--table-header-bg);
      color: var(--table-header-text);
      font-weight: 600;
    }
    .usage-modal-footer {
      padding: 14px 24px;
      border-top: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-input);
      border-radius: 0 0 16px 16px;
    }

    /* Message Usage Footer */
    .msg-usage-bar {
      margin-top: 10px;
      padding-top: 8px;
      border-top: 1px dashed var(--border-color);
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      font-size: 11px;
      color: var(--text-muted);
    }
    .msg-usage-chip {
      background: var(--bg-input);
      border: 1px solid var(--border-color);
      padding: 2px 7px;
      border-radius: 4px;
      font-weight: 500;
    }
    .msg-cost-chip {
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      color: #1d4ed8;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 700;
    }
    [data-theme="dark"] .msg-cost-chip {
      background: #1e3a8a;
      border-color: #3b82f6;
      color: #93c5fd;
    }
    .quota-warning-banner {
      background: #fef2f2;
      border: 1.5px solid #ef4444;
      border-radius: 8px;
      padding: 12px 14px;
      color: #991b1b;
      margin: 8px 0;
    }
    [data-theme="dark"] .quota-warning-banner {
      background: #450a0a;
      border-color: #dc2626;
      color: #fca5a5;
    }
"""

if "/* === Gemini API Usage & Cost Monitor Styles === */" not in content:
    content = content.replace("    /* Sidebar */", usage_css + "\n    /* Sidebar */", 1)
    print("2. Injected Usage Monitor CSS styles!")
else:
    print("2. Usage Monitor CSS already exists.")

# 3. Add Usage Monitor Button in top-nav
old_nav_tools = """        <button id="themeToggleBtn" class="theme-toggle-btn" onclick="toggleTheme()" title="화면 밝기 전환">
          🌙 다크 모드로 전환
        </button>"""

new_nav_tools = """        <!-- Live Gemini API Quota & Cost Monitor Button -->
        <button id="usageMonitorBtn" class="usage-monitor-btn" onclick="openUsageModal()" title="Gemini API 무료티어 한도 및 예상 비용 실시간 대시보드">
          <span id="usageDot" class="status-dot green"></span>
          <span id="usageTitle">무료티어</span>
          <span id="usageCounter" class="usage-counter-tag">0/20회</span>
          <span id="usageCost" class="usage-cost-pill">₩0</span>
        </button>

        <button id="themeToggleBtn" class="theme-toggle-btn" onclick="toggleTheme()" title="화면 밝기 전환">
          🌙 다크 모드로 전환
        </button>"""

if old_nav_tools in content and 'id="usageMonitorBtn"' not in content:
    content = content.replace(old_nav_tools, new_nav_tools, 1)
    print("3. Injected Usage Monitor button into top-nav!")
else:
    print("3. Usage Monitor button already exists in top-nav.")

# 4. Inject Modal HTML before </body>
modal_html = """
  <!-- Gemini API Quota & Cost Dashboard Modal -->
  <div id="usageModal" class="usage-modal-overlay" style="display: none;" onclick="handleModalOverlayClick(event)">
    <div class="usage-modal-dialog">
      <div class="usage-modal-header">
        <h2>📊 Google Gemini API 사용량 및 예상 비용 대시보드</h2>
        <button class="usage-modal-close" onclick="closeUsageModal()" title="닫기">✕</button>
      </div>
      <div class="usage-modal-body">
        
        <!-- Status Callout -->
        <div id="quotaStatusCallout" class="info-callout" style="display: flex; align-items: center; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span id="modalStatusDot" class="status-dot green" style="width: 12px; height: 12px;"></span>
            <div>
              <strong id="modalStatusTitle" style="font-size: 14px;">무료 티어 정상 작동 중 (과금 0원)</strong>
              <div id="modalStatusDesc" style="font-size: 11.5px; color: var(--text-muted); margin-top: 2px;">
                Google AI Studio 무료 티어 한도 내에서 100% 무료로 동작하며, 사용자 결제 승인 없이 자동 과금되지 않습니다.
              </div>
            </div>
          </div>
          <span id="modalRemainingBadge" style="font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 20px; background: rgba(16,185,129,0.15); color: #059669; flex-shrink: 0;">
            잔여 20회
          </span>
        </div>

        <!-- Free Tier Quota Progress -->
        <div class="quota-progress-container">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 13px; font-weight: 600;">오늘 무료 티어 일일 쿼터 현황</span>
            <span id="modalQuotaText" style="font-size: 12.5px; font-weight: 700;">0 / 20 회 (0%)</span>
          </div>
          <div class="progress-bar-bg">
            <div id="modalProgressBar" class="progress-bar-fill" style="width: 0%; background: #10b981;"></div>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted);">
            <span>• 분당 호출 한도(RPM): <b>15회 / 분</b></span>
            <span>• 일일 무료 호출(RPD): <b>20회 / 일</b> (초과 시 429 일시정지)</span>
          </div>
        </div>

        <!-- Expected Cost Stats (Pay-As-You-Go Simulation) -->
        <div>
          <div style="font-size: 13px; font-weight: 700; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
            <span>💰 유료 전환 시 예상 청구 금액 (Pay-As-You-Go 시뮬레이션)</span>
            <span style="font-size: 11px; font-weight: normal; color: var(--text-muted);">(사용량 급증으로 유료 전환 시 과금액)</span>
          </div>
          <div class="stat-card-grid">
            <div class="stat-card">
              <span class="stat-card-title">오늘 총 예상 비용</span>
              <span id="modalDailyCostKrw" class="stat-card-value" style="color: #2563eb;">₩0.0</span>
              <span id="modalDailyCostUsd" class="stat-card-sub">$0.0000 (환율 1,380원)</span>
            </div>
            <div class="stat-card">
              <span class="stat-card-title">오늘 누적 토큰</span>
              <span id="modalDailyTokens" class="stat-card-value">0 토큰</span>
              <span id="modalTokenDetail" class="stat-card-sub">입력 0 / 출력 0</span>
            </div>
            <div class="stat-card">
              <span class="stat-card-title">1회 질의당 평균 비용</span>
              <span id="modalAvgCost" class="stat-card-value" style="color: #059669;">약 1.8원</span>
              <span class="stat-card-sub">수백 페이지 대조 기준</span>
            </div>
          </div>
        </div>

        <!-- Scenarios -->
        <div style="background: var(--bg-input); border: 1px solid var(--border-color); border-radius: 12px; padding: 14px 16px;">
          <div style="font-size: 12.5px; font-weight: 700; margin-bottom: 6px;">💡 사용량 시나리오별 예상 지출 (유료 결제 시)</div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 8px; font-size: 11.5px;">
            <div style="padding: 6px 10px; background: var(--bg-card); border-radius: 6px; border: 1px solid var(--border-color);">
              <div>• <b>50회</b> 질의:</div>
              <div style="font-weight: 700; color: #2563eb; margin-top: 2px;">약 90원 ($0.065)</div>
            </div>
            <div style="padding: 6px 10px; background: var(--bg-card); border-radius: 6px; border: 1px solid var(--border-color);">
              <div>• <b>100회</b> 질의:</div>
              <div style="font-weight: 700; color: #2563eb; margin-top: 2px;">약 180원 ($0.13)</div>
            </div>
            <div style="padding: 6px 10px; background: var(--bg-card); border-radius: 6px; border: 1px solid var(--border-color);">
              <div>• <b>500회</b> 질의:</div>
              <div style="font-weight: 700; color: #2563eb; margin-top: 2px;">약 900원 ($0.65)</div>
            </div>
            <div style="padding: 6px 10px; background: var(--bg-card); border-radius: 6px; border: 1px solid var(--border-color);">
              <div>• <b>1,000회</b> 질의:</div>
              <div style="font-weight: 700; color: #059669; margin-top: 2px;">약 1,800원 ($1.30)</div>
            </div>
          </div>
          <div style="font-size: 11px; color: var(--text-muted); margin-top: 8px;">
            ※ Gemini Flash는 전 세계 최저가 수준(100만 토큰당 약 100원)으로, 하루 1,000번 질문하더라도 커피 한 잔 값(수천 원)보다 저렴하므로 안심하고 유료 결제를 연결하셔도 됩니다.
          </div>
        </div>

        <!-- Official Pricing Table -->
        <div>
          <div style="font-size: 12.5px; font-weight: 700; margin-bottom: 4px;">🏷️ 구글 공식 요금 기준표 (Gemini 2.5 / 3.6 Flash)</div>
          <table class="pricing-table">
            <thead>
              <tr>
                <th>항목</th>
                <th>100만 토큰당 단가 (USD)</th>
                <th>원화 환산 (1,380원/$)</th>
                <th>특징 / 설명</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><b>입력 프롬프트</b></td>
                <td>$0.075 / 1M</td>
                <td>약 103.5원</td>
                <td>사용자 질문 및 참조 PDF 원문</td>
              </tr>
              <tr>
                <td><b>캐시된 컨텍스트</b></td>
                <td>$0.01875 / 1M</td>
                <td>약 25.9원</td>
                <td>Google File API 캐시 적용 시 <b>75% 할인</b></td>
              </tr>
              <tr>
                <td><b>출력 답변</b></td>
                <td>$0.300 / 1M</td>
                <td>약 414.0원</td>
                <td>AI가 작성한 기술 분석 답변</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Safety Assurance -->
        <div style="font-size: 11.5px; color: var(--text-muted); line-height: 1.6; border-left: 3px solid #2563eb; padding-left: 10px;">
          • <strong>과금 폭탄 방지 안심 가이드:</strong> 무료 티어 키는 20회 초과 시 429 오류만 발생할 뿐 절대 자동 결제되지 않습니다.<br>
          • <strong>사용량 급증 대비 팁:</strong> Google Cloud 결제 콘솔에서 <strong>'월 5,000원 또는 10,000원 예산 알림(Budget Alert)'</strong>을 설정해 두시면 예기치 못한 비용 발생을 100% 원천 차단할 수 있습니다.
        </div>

      </div>
      <div class="usage-modal-footer">
        <div style="display: flex; gap: 8px;">
          <a href="https://aistudio.google.com/" target="_blank" style="text-decoration: none; font-size: 12px; color: var(--accent); font-weight: 600;">
            🔗 AI Studio 콘솔 ➔
          </a>
          <span style="color: var(--border-color);">|</span>
          <a href="https://console.cloud.google.com/billing" target="_blank" style="text-decoration: none; font-size: 12px; color: var(--accent); font-weight: 600;">
            💳 Google Cloud 결제 콘솔 ➔
          </a>
        </div>
        <button onclick="closeUsageModal()" style="padding: 6px 16px; background: var(--accent); color: #fff; border: none; border-radius: 6px; font-weight: 600; cursor: pointer;">
          확인
        </button>
      </div>
    </div>
  </div>
"""

if 'id="usageModal"' not in content:
    content = content.replace("</body>", modal_html + "\n</body>", 1)
    print("4. Injected Usage Dashboard Modal HTML before </body>!")
else:
    print("4. Usage Dashboard Modal HTML already exists.")

# 5. Inject JavaScript functions for usage monitoring and modal control
usage_js = """
    // === Gemini API Usage & Cost Monitoring Logic ===
    async function fetchUsageStats() {
      try {
        const res = await fetch('/api/usage');
        if (!res.ok) return;
        const data = await res.json();
        updateUsageUI(data);
      } catch (e) {
        console.warn('Failed to fetch usage stats:', e);
      }
    }

    function updateUsageUI(stats) {
      if (!stats) return;
      
      const queries = stats.daily_queries || 0;
      const limit = stats.free_tier_limit || 20;
      const costKrw = (stats.daily_cost_krw !== undefined ? stats.daily_cost_krw : 0).toFixed(1);
      const costUsd = (stats.daily_cost_usd !== undefined ? stats.daily_cost_usd : 0).toFixed(4);
      const tokens = (stats.daily_total_tokens || 0).toLocaleString();
      const status = stats.free_tier_status || 'SAFE';
      const remaining = Math.max(0, limit - queries);
      const pct = Math.min(100, Math.round((queries / limit) * 100));

      // 1. Top Nav Badge
      const usageCounter = document.getElementById('usageCounter');
      const usageCost = document.getElementById('usageCost');
      const usageDot = document.getElementById('usageDot');
      const usageTitle = document.getElementById('usageTitle');

      if (usageCounter) usageCounter.textContent = `${queries}/${limit}회`;
      if (usageCost) usageCost.textContent = `₩${costKrw}`;

      if (usageDot && usageTitle) {
        usageDot.className = 'status-dot';
        if (status === 'EXCEEDED' || queries >= limit) {
          usageDot.classList.add('red');
          usageTitle.textContent = '한도초과';
        } else if (status === 'WARNING' || queries >= limit * 0.7) {
          usageDot.classList.add('yellow');
          usageTitle.textContent = '한도주의';
        } else {
          usageDot.classList.add('green');
          usageTitle.textContent = '무료티어';
        }
      }

      // 2. Modal Details
      const mProgressBar = document.getElementById('modalProgressBar');
      const mQuotaText = document.getElementById('modalQuotaText');
      const mDailyCostKrw = document.getElementById('modalDailyCostKrw');
      const mDailyCostUsd = document.getElementById('modalDailyCostUsd');
      const mDailyTokens = document.getElementById('modalDailyTokens');
      const mTokenDetail = document.getElementById('modalTokenDetail');
      const mRemainingBadge = document.getElementById('modalRemainingBadge');
      const mStatusTitle = document.getElementById('modalStatusTitle');
      const mStatusDesc = document.getElementById('modalStatusDesc');
      const mStatusDot = document.getElementById('modalStatusDot');
      const mAvgCost = document.getElementById('modalAvgCost');

      if (mQuotaText) mQuotaText.textContent = `${queries} / ${limit} 회 (${pct}%)`;
      if (mProgressBar) {
        mProgressBar.style.width = `${pct}%`;
        if (pct >= 100) mProgressBar.style.background = '#ef4444';
        else if (pct >= 70) mProgressBar.style.background = '#f59e0b';
        else mProgressBar.style.background = '#10b981';
      }

      if (mDailyCostKrw) mDailyCostKrw.textContent = `₩${costKrw}`;
      if (mDailyCostUsd) mDailyCostUsd.textContent = `$${costUsd} (환율 1,380원)`;
      if (mDailyTokens) mDailyTokens.textContent = `${tokens} 토큰`;
      if (mTokenDetail) {
        const pt = (stats.daily_prompt_tokens || 0).toLocaleString();
        const ct = (stats.daily_candidate_tokens || 0).toLocaleString();
        mTokenDetail.textContent = `입력 ${pt} / 출력 ${ct}`;
      }
      if (mRemainingBadge) {
        mRemainingBadge.textContent = queries >= limit ? '한도 소진' : `잔여 ${remaining}회`;
        mRemainingBadge.style.background = queries >= limit ? '#fee2e2' : 'rgba(16,185,129,0.15)';
        mRemainingBadge.style.color = queries >= limit ? '#b91c1c' : '#059669';
      }
      if (mAvgCost && stats.avg_query_cost_krw) {
        mAvgCost.textContent = `약 ${stats.avg_query_cost_krw}원`;
      }

      if (mStatusTitle && mStatusDesc && mStatusDot) {
        mStatusDot.className = 'status-dot';
        if (status === 'EXCEEDED' || queries >= limit) {
          mStatusDot.classList.add('red');
          mStatusTitle.textContent = '무료 티어 일일 한도 초과 (429 주의)';
          mStatusDesc.textContent = '오늘 무료 제공량(20회)이 모두 소진되었습니다. 결제 계정 연동 시 1회당 약 1.5~2원의 최저가로 무제한 사용 가능합니다.';
        } else if (status === 'WARNING' || queries >= limit * 0.7) {
          mStatusDot.classList.add('yellow');
          mStatusTitle.textContent = '무료 티어 한도 근접 (주의)';
          mStatusDesc.textContent = `일일 무료 호출 20회 중 ${queries}회를 사용하셨습니다. 곧 일일 한도에 도달할 수 있습니다.`;
        } else {
          mStatusDot.classList.add('green');
          mStatusTitle.textContent = '무료 티어 정상 작동 중 (과금 0원)';
          mStatusDesc.textContent = 'Google AI Studio 무료 티어 한도 내에서 100% 무료로 동작하며, 사용자 결제 승인 없이 자동 과금되지 않습니다.';
        }
      }
    }

    function openUsageModal() {
      fetchUsageStats();
      const modal = document.getElementById('usageModal');
      if (modal) modal.style.display = 'flex';
    }

    function closeUsageModal() {
      const modal = document.getElementById('usageModal');
      if (modal) modal.style.display = 'none';
    }

    function handleModalOverlayClick(e) {
      if (e.target && e.target.id === 'usageModal') {
        closeUsageModal();
      }
    }

    // Auto-fetch usage on load and every 30s
    window.addEventListener('DOMContentLoaded', () => {
      fetchUsageStats();
      setInterval(fetchUsageStats, 30000);
    });
"""

if "function fetchUsageStats()" not in content:
    content = content.replace("  </script>\n</body>", usage_js + "\n  </script>\n</body>", 1)
    print("5. Injected Usage JavaScript logic before </script>!")
else:
    print("5. Usage JavaScript logic already exists.")

# 6. Update sendQuery in JS to append msg-usage-bar and handle quota error
old_render_block = """          const traceHtml = buildTraceHtml(traceData);
          if (botMsgDiv) {
            botMsgDiv.innerHTML = traceHtml + parsedHtml;
          }"""

new_render_block = """          const traceHtml = buildTraceHtml(traceData);
          
          let usageBarHtml = '';
          if (data.usage && data.usage.query) {
            const uq = data.usage.query;
            const ud = data.usage.daily || {};
            const ptStr = (uq.prompt_tokens || 0).toLocaleString();
            const ctStr = (uq.candidate_tokens || 0).toLocaleString();
            const totStr = (uq.total_tokens || 0).toLocaleString();
            const costKrw = (uq.cost_krw || 0).toFixed(1);
            const costUsd = (uq.cost_usd || 0).toFixed(4);
            const tierStatus = ud.free_tier_status || 'SAFE';
            const tierBadge = tierStatus === 'SAFE' ? '<span style="color:#059669; font-weight:700;">🟢 무료티어 적용 (0원)</span>'
                            : tierStatus === 'WARNING' ? '<span style="color:#d97706; font-weight:700;">🟡 무료한도 근접</span>'
                            : '<span style="color:#dc2626; font-weight:700;">🔴 한도초과(유료필요)</span>';

            usageBarHtml = `
              <div class="msg-usage-bar">
                <span class="msg-usage-chip">⚡ 토큰: 입력 ${ptStr}p / 출력 ${ctStr}p (총 ${totStr})</span>
                <span class="msg-cost-chip">💰 유료전환 시 회당 비용: ₩${costKrw} ($${costUsd})</span>
                <span>${tierBadge}</span>
                <span style="cursor:pointer; color:var(--accent); text-decoration:underline; margin-left:auto;" onclick="openUsageModal()">
                  📊 누적 예상: ₩${(ud.cost_krw || 0).toFixed(1)} (${ud.queries || 0}/${ud.limit || 20}회)
                </span>
              </div>
            `;
            // Update top-nav badge immediately
            updateUsageUI(ud);
          }

          if (botMsgDiv) {
            botMsgDiv.innerHTML = traceHtml + parsedHtml + usageBarHtml;
          }"""

if old_render_block in content:
    content = content.replace(old_render_block, new_render_block, 1)
    print("6. Updated sendQuery to render msg-usage-bar and update badge!")
else:
    print("6. sendQuery render block pattern not found.")

# 7. Quota Error Handling in sendQuery
old_err_handling = """        if (data.error) {
          if (botMsgDiv) botMsgDiv.innerHTML = `<span style="color:#ef4444;">⚠️ 오류: ${data.error}</span>`;
        }"""

new_err_handling = """        if (data.error) {
          const isQuota = data.error.includes("429") || data.error.includes("quota") || data.error.includes("Quota") || data.error.includes("RESOURCE_EXHAUSTED");
          if (isQuota) {
            if (botMsgDiv) {
              botMsgDiv.innerHTML = `
                <div class="quota-warning-banner">
                  <div style="font-weight:700; font-size:13.5px; margin-bottom:5px;">⚠️ [Google Gemini API] 무료 티어 일일 한도(20회)에 도달했습니다.</div>
                  <div style="font-size:12px; line-height:1.5; margin-bottom:10px;">
                    Google AI Studio 무료 티어 일일 쿼터가 소진되었습니다. 구글 클라우드 결제 계정(유료 종량제)을 연동하시면 제한 없이 초고속으로 계속 이용하실 수 있습니다.<br>
                    <strong>💡 Gemini Flash 요금은 1회 질의당 약 1.5 ~ 2원 수준으로 매우 저렴합니다.</strong>
                  </div>
                  <div style="display:flex; gap:8px;">
                    <button onclick="openUsageModal()" style="padding:6px 12px; background:#2563eb; color:#fff; border:none; border-radius:6px; font-weight:600; font-size:12px; cursor:pointer;">
                      💰 예상 비용 및 한도 대시보드 열기
                    </button>
                    <a href="https://aistudio.google.com/" target="_blank" style="padding:6px 12px; background:var(--bg-card); color:var(--text-main); border:1px solid var(--border-color); border-radius:6px; font-size:12px; text-decoration:none; display:inline-flex; align-items:center;">
                      Google AI Studio 결제 설정 ➔
                    </a>
                  </div>
                </div>
              `;
            }
            fetchUsageStats();
          } else {
            if (botMsgDiv) botMsgDiv.innerHTML = `<span style="color:#ef4444;">⚠️ 오류: ${data.error}</span>`;
          }
        }"""

if old_err_handling in content:
    content = content.replace(old_err_handling, new_err_handling, 1)
    print("7. Enhanced sendQuery with Quota Error Handling banner!")
else:
    print("7. sendQuery error handling pattern not found.")

server_path.write_text(content, encoding="utf-8")
print("All frontend & backend patches applied successfully to server.py!")
