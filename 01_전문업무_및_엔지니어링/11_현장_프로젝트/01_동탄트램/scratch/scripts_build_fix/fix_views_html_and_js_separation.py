import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Separate HTML Views
pure_views_html = """  <!-- ============================================================================ -->
  <!-- 👷 뷰 2: 자원 투입 & 최적화 (Resource Leveling) 컨테이너 -->
  <!-- ============================================================================ -->
  <div id="container-resource-view" style="display: none; padding: 1.2rem; background: #0f172a; color: #f8fafc; overflow-y: auto; height: calc(100vh - 65px);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem;">
      <div>
        <h2 style="font-size: 1.3rem; font-weight: 900; color: #38bdf8; margin: 0 0 0.3rem 0;">👷 액티비티별 자원(인력·장비·자재) 투입 & 자원 최적화(Resource Leveling)</h2>
        <p style="font-size: 0.85rem; color: #94a3b8; margin: 0;">동탄트램 전 공정 액티비티별 일일 필요 인력/장비/자재 부하를 실시간 모니터링하고 피크(Peak) 부하를 평준화합니다.</p>
      </div>
      <div style="display: flex; gap: 0.6rem;">
        <button onclick="runResourceOptimization()" style="padding: 0.6rem 1.2rem; background: #0284c7; color: #ffffff; border: none; border-radius: 8px; font-size: 0.88rem; font-weight: 900; cursor: pointer; box-shadow: 0 4px 12px rgba(2,132,199,0.4);">
          ⚡ 자원 피크 평준화/최적화 자동 실행
        </button>
        <button onclick="resetResourceData()" style="padding: 0.6rem 1rem; background: #334155; color: #ffffff; border: none; border-radius: 8px; font-size: 0.85rem; font-weight: 700; cursor: pointer;">
          🔄 자원 초기화
        </button>
      </div>
    </div>

    <!-- 자원 피크 과부하 경보 요약 카드 -->
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
      <div style="background: #1e293b; padding: 1rem; border-radius: 10px; border-left: 4px solid #0284c7;">
        <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 700;">일일 최대 투입 인력</div>
        <div style="font-size: 1.6rem; font-weight: 900; color: #ffffff; margin-top: 0.2rem;" id="res-stat-max-labor">185 명/일</div>
        <div style="font-size: 0.75rem; color: #10b981; margin-top: 0.3rem;">한도 보유량: 220명 (안정적)</div>
      </div>
      <div style="background: #1e293b; padding: 1rem; border-radius: 10px; border-left: 4px solid #f59e0b;">
        <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 700;">일일 주요 중장비 투입</div>
        <div style="font-size: 1.6rem; font-weight: 900; color: #f59e0b; margin-top: 0.2rem;" id="res-stat-max-equip">42 대/일</div>
        <div style="font-size: 0.75rem; color: #f59e0b; margin-top: 0.3rem;">한도 보유량: 45대 (피크 주의)</div>
      </div>
      <div style="background: #1e293b; padding: 1rem; border-radius: 10px; border-left: 4px solid #10b981;">
        <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 700;">주요 궤도 레일 자재 수급</div>
        <div style="font-size: 1.6rem; font-weight: 900; color: #10b981; margin-top: 0.2rem;" id="res-stat-total-rail">41,000 m</div>
        <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.3rem;">50N 표준 레일 수급 100% 확보</div>
      </div>
      <div style="background: #1e293b; padding: 1rem; border-radius: 10px; border-left: 4px solid #8b5cf6;">
        <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 700;">자원 평준화(Leveling) 효율</div>
        <div style="font-size: 1.6rem; font-weight: 900; color: #a78bfa; margin-top: 0.2rem;" id="res-stat-efficiency">94.2 %</div>
        <div style="font-size: 0.75rem; color: #10b981; margin-top: 0.3rem;">부하 변동 계수 18.5% 개선됨</div>
      </div>
    </div>

    <!-- 일별 자원 부하 히스토그램 (Resource Histogram Chart) -->
    <div style="background: #1e293b; padding: 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid #334155;">
      <h3 style="font-size: 1rem; font-weight: 800; color: #f8fafc; margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
        <span>📈 일별/월별 자원 투입 히스토그램 (Resource Load Histogram)</span>
        <span style="font-size: 0.75rem; color: #38bdf8; background: rgba(56,189,248,0.15); padding: 0.2rem 0.5rem; border-radius: 4px;">인력(명) & 장비(대) 실시간 스택</span>
      </h3>
      <div id="resource-histogram-container" style="width: 100%; height: 260px; background: #0f172a; border-radius: 8px; padding: 0.5rem; position: relative;">
        <!-- SVG Histogram Chart rendered by JS -->
      </div>
    </div>

    <!-- 액티비티별 자원 투입 입력 및 관리 테이블 -->
    <div style="background: #1e293b; padding: 1.2rem; border-radius: 12px; border: 1px solid #334155;">
      <h3 style="font-size: 1rem; font-weight: 800; color: #f8fafc; margin: 0 0 1rem 0;">📋 액티비티별 자원 투입 세부 현황표 (Editable Activity Resources)</h3>
      <div style="overflow-x: auto; max-height: 480px;">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.82rem; text-align: left;">
          <thead>
            <tr style="background: #0f172a; color: #94a3b8; border-bottom: 2px solid #334155;">
              <th style="padding: 0.6rem;">공구/구간</th>
              <th style="padding: 0.6rem;">Activity 코드</th>
              <th style="padding: 0.6rem;">Activity 명칭</th>
              <th style="padding: 0.6rem; text-align: center;">공기(일)</th>
              <th style="padding: 0.6rem; text-align: center;">작업자(명/일)</th>
              <th style="padding: 0.6rem; text-align: center;">중장비(대/일)</th>
              <th style="padding: 0.6rem; text-align: center;">노무비(만원)</th>
              <th style="padding: 0.6rem; text-align: center;">장비비(만원)</th>
              <th style="padding: 0.6rem; text-align: center;">재료비(만원)</th>
              <th style="padding: 0.6rem; text-align: right;">총 직접비(만원)</th>
              <th style="padding: 0.6rem; text-align: center;">피크 상태</th>
            </tr>
          </thead>
          <tbody id="resource-table-body">
            <!-- Rendered by JS -->
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- ============================================================================ -->
  <!-- 💰 뷰 3: 투입비 추정 & EVM (S-Curve) 컨테이너 -->
  <!-- ============================================================================ -->
  <div id="container-evm-view" style="display: none; padding: 1.2rem; background: #0f172a; color: #f8fafc; overflow-y: auto; height: calc(100vh - 65px);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem;">
      <div>
        <h2 style="font-size: 1.3rem; font-weight: 900; color: #10b981; margin: 0 0 0.3rem 0;">💰 시공구간 투입비 추정 & EVM (S-Curve) 비교 분석</h2>
        <p style="font-size: 0.85rem; color: #94a3b8; margin: 0;">28개 시공구간별 직접 공사비 추정치와 계획 가치(PV), 획득 가치(EV), 실제 비용(AC) S-Curve 및 수행지수(SPI/CPI)를 분석합니다.</p>
      </div>
      <div style="display: flex; gap: 0.6rem;">
        <button onclick="recalculateEVM()" style="padding: 0.6rem 1.2rem; background: #10b981; color: #ffffff; border: none; border-radius: 8px; font-size: 0.88rem; font-weight: 900; cursor: pointer; box-shadow: 0 4px 12px rgba(16,185,129,0.4);">
          🔄 EVM 지표 실시간 재계산
        </button>
      </div>
    </div>

    <!-- EVM KPI Dashboard Cards -->
    <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
      <div style="background: #1e293b; padding: 1rem; border-radius: 10px; border-left: 4px solid #0284c7;">
        <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 700;">PV (계획 가치)</div>
        <div style="font-size: 1.5rem; font-weight: 900; color: #38bdf8; margin-top: 0.2rem;" id="evm-pv-val">4,850 억원</div>
        <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.3rem;">계획 공정률 100% 예산</div>
      </div>
      <div style="background: #1e293b; padding: 1rem; border-radius: 10px; border-left: 4px solid #10b981;">
        <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 700;">EV (획득 가치)</div>
        <div style="font-size: 1.5rem; font-weight: 900; color: #34d399; margin-top: 0.2rem;" id="evm-ev-val">4,608 억원</div>
        <div style="font-size: 0.75rem; color: #10b981; margin-top: 0.3rem;">실제 진척 공정률 기반 획득</div>
      </div>
      <div style="background: #1e293b; padding: 1rem; border-radius: 10px; border-left: 4px solid #f59e0b;">
        <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 700;">AC (실제 투입비)</div>
        <div style="font-size: 1.5rem; font-weight: 900; color: #fbbf24; margin-top: 0.2rem;" id="evm-ac-val">4,550 억원</div>
        <div style="font-size: 0.75rem; color: #fbbf24; margin-top: 0.3rem;">실제 현장 집행 비용</div>
      </div>
      <div style="background: #1e293b; padding: 1rem; border-radius: 10px; border-left: 4px solid #ea580c;">
        <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 700;">SPI (공정수행지수)</div>
        <div style="font-size: 1.5rem; font-weight: 900; color: #fb923c; margin-top: 0.2rem;" id="evm-spi-val">0.95</div>
        <div style="font-size: 0.75rem; color: #ea580c; margin-top: 0.3rem;">⚠️ 5.0% 공기 지연 주의</div>
      </div>
      <div style="background: #1e293b; padding: 1rem; border-radius: 10px; border-left: 4px solid #8b5cf6;">
        <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 700;">CPI (비용수행지수)</div>
        <div style="font-size: 1.5rem; font-weight: 900; color: #a78bfa; margin-top: 0.2rem;" id="evm-cpi-val">1.01</div>
        <div style="font-size: 0.75rem; color: #10b981; margin-top: 0.3rem;">✅ 예산 1.3% 절감 중</div>
      </div>
    </div>

    <!-- EVM S-Curve 누적 공정률 및 집행비 차트 -->
    <div style="background: #1e293b; padding: 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid #334155;">
      <h3 style="font-size: 1rem; font-weight: 800; color: #f8fafc; margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.6rem;">
        <span>📈 EVM 누적 S-Curve (계획 PV vs 획득 EV vs 실제비용 AC)</span>
        <span style="font-size: 0.75rem; color: #38bdf8; background: rgba(56,189,248,0.15); padding: 0.2rem 0.5rem; border-radius: 4px;">월별 누적 곡선</span>
      </h3>
      <div id="evm-scurve-chart-container" style="width: 100%; height: 280px; background: #0f172a; border-radius: 8px; padding: 0.5rem; position: relative;">
        <!-- EVM S-Curve SVG Rendered by JS -->
      </div>
    </div>

    <!-- 28개 시공구간별 직접 투입비 & 단가 산출 세부 테이블 -->
    <div style="background: #1e293b; padding: 1.2rem; border-radius: 12px; border: 1px solid #334155;">
      <h3 style="font-size: 1rem; font-weight: 800; color: #f8fafc; margin: 0 0 1rem 0;">🏗️ 28개 시공구간별 추정 공사비 및 m당 단가 산출표 (Section Costs)</h3>
      <div style="overflow-x: auto; max-height: 480px;">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.82rem; text-align: left;">
          <thead>
            <tr style="background: #0f172a; color: #94a3b8; border-bottom: 2px solid #334155;">
              <th style="padding: 0.6rem;">시공구간 명칭</th>
              <th style="padding: 0.6rem; text-align: center;">공구</th>
              <th style="padding: 0.6rem; text-align: right;">구간연장(m)</th>
              <th style="padding: 0.6rem; text-align: right;">노무비(억원)</th>
              <th style="padding: 0.6rem; text-align: right;">장비비(억원)</th>
              <th style="padding: 0.6rem; text-align: right;">재료비(억원)</th>
              <th style="padding: 0.6rem; text-align: right;">총 직접공사비(억원)</th>
              <th style="padding: 0.6rem; text-align: right;">m당 공사비(만원/m)</th>
              <th style="padding: 0.6rem; text-align: center;">공정진척률(%)</th>
            </tr>
          </thead>
          <tbody id="evm-sections-table-body">
            <!-- Rendered by JS -->
          </tbody>
        </table>
      </div>
    </div>
  </div>"""

# Clean any invalid HTML injected into JS
script_start = content.find('<script>')
script_end = content.rfind('</script>')
html_part = content[:script_start]
js_part = content[script_start:script_end+9]
tail_part = content[script_end+9:]

# Remove any HTML tags incorrectly placed inside JS
js_part_clean = re.sub(r'<!-- ============================================================================ -->[\s\S]*?</div>\s*</div>', '', js_part)

# Inject pure_views_html right before <script>
new_content = html_part + "\n" + pure_views_html + "\n\n" + js_part_clean + tail_part

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully separated HTML views and JS engine!")
