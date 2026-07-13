import os
import shutil
from bs4 import BeautifulSoup

def update_q49_q50(file_path):
    print(f"Updating Question 49 and 50 inside: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_q49_q50"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. Target article with id="q49"
    q49_art = soup.find("article", id="q49")
    if not q49_art:
        print("Error: Could not find article with id='q49'")
        return False
        
    # 2. Target article with id="q50"
    q50_art = soup.find("article", id="q50")
    if not q50_art:
        print("Error: Could not find article with id='q50'")
        return False
        
    # 3. New Q49 HTML (Shut-off Operation & 3 Points)
    new_q49_html = r"""
    <article class="answer-sheet" id="q49">
        <div class="category-path-container">
            <span class="category-path">소방펌프 &gt; 성능시험</span>
            <span class="category-badge">소방펌프</span>
        </div>
        <h2>[소방펌프] Question 49. 소방펌프 성능시험 시 체절운전(Shut-off Operation)의 정의, 체절압력 범위 및 3대 성능 곡선 기준 포인트</h2>
        
        <h3>1. 개요 및 출제 의도</h3>
        <p>소방용 가압송수장치는 화재 시 요구되는 신뢰성 높은 토출량과 수압을 보장하기 위해 가설 시 및 정기 소방점검 시 성능시험 배관망을 통한 정밀 성능 검증을 수행한다. 성능시험의 기준선이 되는 무유량 상태의 체절운전(Shut-off)의 정의와 규정 체절압력 한계를 정의하고, 소방펌프 화재안전기준(NFTC 102)에서 규정하는 펌프 특성곡선 상의 3대 성능 기준 포인트(체절점, 정격점, 최대과부하점)와 수온 상승 방지를 위한 순환배관의 작동 원리를 규명한다.</p>
        
        <h3>2. 종합 모식도: 성능시험 배관 계통 및 펌프 H-Q 성능 특성 3대 기준 곡선</h3>
        <div class="zoomable-media" data-title="펌프성능 곡선 및 시험계통도">
            <svg viewBox="0 0 700 350" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background: var(--bg-secondary); border-radius: 10px; padding: 10px;">
                <defs>
                    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--text-primary)"/>
                    </marker>
                </defs>
                <!-- Outer Border -->
                <rect width="680" height="330" x="10" y="10" rx="8" fill="none" stroke="var(--border)" stroke-width="1.5"/>
                
                <!-- Left: Performance Test Piping (시험 배관 계통) -->
                <g transform="translate(30, 20)">
                    <rect width="280" height="290" rx="8" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1"/>
                    <text x="140" y="25" text-anchor="middle" fill="#2563eb" font-weight="bold" font-size="11">펌프 성능시험 장치 배관 계통</text>
                    
                    <!-- Pump -->
                    <circle cx="60" cy="180" r="22" fill="#94a3b8" stroke="var(--border)" stroke-width="2"/>
                    <text x="60" y="183" text-anchor="middle" fill="#1e293b" font-weight="bold" font-size="9">펌프</text>
                    
                    <!-- Suction and Discharge line -->
                    <path d="M 15 180 L 38 180 M 82 180 L 260 180" stroke="#3b82f6" stroke-width="3" fill="none"/>
                    
                    <!-- Main Control Valve (주개폐밸브) -->
                    <rect width="10" height="20" x="100" y="170" fill="#ef4444" stroke="var(--border)"/>
                    <text x="105" y="162" text-anchor="middle" fill="#ef4444" font-weight="bold" font-size="7">주밸브(폐쇄)</text>
                    
                    <!-- Circulation Line & Relief Valve (순환배관 및 릴리프) -->
                    <path d="M 90 180 L 90 110 L 170 110" stroke="#10b981" stroke-width="2" fill="none"/>
                    <circle cx="170" cy="110" r="8" fill="#f59e0b" stroke="var(--border)"/>
                    <text x="170" y="95" text-anchor="middle" fill="#d97706" font-weight="bold" font-size="7">릴리프 밸브</text>
                    
                    <!-- Test Line (성능시험배관) -->
                    <path d="M 130 180 L 130 240 L 250 240" stroke="#8b5cf6" stroke-width="2.5" fill="none"/>
                    <!-- Flow Meter (유량계) -->
                    <rect width="30" height="15" x="160" y="233" fill="#cbd5e1" stroke="var(--border)"/>
                    <text x="175" y="244" text-anchor="middle" fill="#1e293b" font-size="8">유량계</text>
                    <!-- Flow Control Valve (유량조절밸브) -->
                    <rect width="10" height="20" x="210" y="230" fill="#475569" stroke="var(--border)"/>
                    <text x="215" y="222" text-anchor="middle" fill="#475569" font-size="7">조절밸브</text>
                </g>
                
                <!-- Right: HQ Curve 3 Points (H-Q 특성 곡선) -->
                <g transform="translate(340, 20)">
                    <rect width="310" height="290" rx="8" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1"/>
                    <text x="155" y="25" text-anchor="middle" fill="#dc2626" font-weight="bold" font-size="11">NFTC 규정 3대 운전 성능시험점</text>
                    
                    <!-- Coordinates -->
                    <line x1="40" y1="240" x2="280" y2="240" stroke="var(--text-primary)" stroke-width="1.5"/>
                    <line x1="40" y1="50" x2="40" y2="240" stroke="var(--text-primary)" stroke-width="1.5"/>
                    <text x="35" y="45" text-anchor="end" fill="var(--text-primary)" font-size="8">압력 (H)</text>
                    <text x="270" y="255" fill="var(--text-primary)" font-size="8">유량 (Q)</text>
                    
                    <!-- H-Q Curve -->
                    <path d="M 40 100 Q 140 120 250 220" fill="none" stroke="#2563eb" stroke-width="2.5"/>
                    
                    <!-- 1. Shut-off Point (체절점 Q=0) -->
                    <circle cx="40" cy="100" r="5" fill="#ef4444"/>
                    <text x="50" y="95" fill="#ef4444" font-weight="bold" font-size="8">① 체절점 (Q=0, H ≤ 140%)</text>
                    
                    <!-- 2. Rated Point (정격점 Q=100) -->
                    <circle cx="140" cy="120" r="5" fill="#f59e0b"/>
                    <text x="150" y="115" fill="#d97706" font-weight="bold" font-size="8">② 정격점 (Q=100%, H ≥ 100%)</text>
                    <line x1="140" y1="120" x2="140" y2="240" stroke="var(--text-secondary)" stroke-dasharray="2,2"/>
                    <line x1="40" y1="120" x2="140" y2="120" stroke="var(--text-secondary)" stroke-dasharray="2,2"/>
                    
                    <!-- 3. Peak Point (최대부하점 Q=150) -->
                    <circle cx="210" cy="170" r="5" fill="#10b981"/>
                    <text x="180" y="160" fill="#10b981" font-weight="bold" font-size="8">③ 최대과부하 (Q=150%, H ≥ 65%)</text>
                    <line x1="210" y1="170" x2="210" y2="240" stroke="var(--text-secondary)" stroke-dasharray="2,2"/>
                    <line x1="40" y1="170" x2="210" y2="170" stroke="var(--text-secondary)" stroke-dasharray="2,2"/>
                </g>
            </svg>
            <div class="diagram-explanation">
                <strong>모식도 설명:</strong> 좌측은 주개폐밸브를 차단(Q=0)하고 순환배관과 성능시험 바이패스 배관을 통해 유량을 유기적으로 제어하는 소방펌프 시험부 등가 계통입니다. 우측은 소방 가압송수장치 성능평가 시 도출되어야 하는 H-Q 3대 성능 기준선입니다. 펌프 무부하 기동점인 체절점($Q=0$) 압력 한계는 설계 정격의 $140\%$ 이하이고, 정격점($Q=100\%$)은 정격 압력 $100\%$ 이상이며, 과부하점($Q=150\%$)은 정격 압력의 최소 $65\%$ 이상을 지탱해야 통과합니다.
            </div>
            <div class="key-takeaway">
                <strong>초간단 직관적 이해 (비유법):</strong> 펌프 성능시험은 펌프의 체력 검사입니다. **체절운전은 펌프가 뿜어내는 출구를 완전히 꽉 틀어막고(유량 0%) 힘껏 밀어올릴 때 수압을 재는 무부하 테스트**입니다. 이때 압력이 너무 과도하게 솟구치면 배관이 터지므로 **정격 수압의 140%를 넘지 못하게 제한**합니다. 그리고 펌프가 과도하게 힘을 써서 물이 끓지 않도록 **작은 대피 배관(순환배관)에 달린 안전 밸브(릴리프 밸브)가 과도한 압력을 가로채 물을 뿜어주어 열을 내리는 원리**입니다.
            </div>
        </div>
        
        <h3>3. 체절운전 (Shut-off Operation)의 정의 및 공학적 문제점</h3>
        
        <h4>1) 정의</h4>
        <p>펌프의 토출측 주 밸브를 완전히 밀폐하여 토출 유량을 <strong>영(0)인 상태 ($Q=0\,\text{m}^3/\text{min}$)</strong>로 유지하고 펌프를 운전하는 행위를 말한다. 펌프 성능 곡선 상에서 양정이 최고가 되는 무부하 기동 상태이다.</p>
        
        <h4>2) 공학적 문제점 (수온 상승 메커니즘)</h4>
        <p>체절 운전 시 펌프 내 고여 있는 물(체류수)에 전동기(또는 엔진)의 축 동력 에너지($L_p$)가 지속 공급되나, 외부로 방출되는 유량이 없기 때문에 방출 냉각이 일어나지 않는다. 공급된 역학적 운동 에너지는 100% 열에너지로 소실 치환되어 펌프 케이싱 내 수온을 실시간으로 급상승시킨다.</p>
        <div class="formula-box" style="margin: 10px 0; font-family: monospace; font-size: 0.95rem; text-align: center;">
            \Delta T = \frac{860 \cdot L_p \cdot t}{V_w \cdot C_p} \quad (\text{수온 급상승식})
        </div>
        <p>수온이 포화 온도 이상으로 비등하면 펌프 내부에 공동현상(Cavitation)이 즉각 발생하여 임펠러 궤멸, 진동 파손, 밀봉장치(Mechanical Seal) 열변형 소손을 유발하므로 반드시 운전 시간을 제한하고 순환배관을 설치해야 한다.</p>
        
        <h3>4. 소방펌프의 3대 성능 기준 포인트 (NFTC 102)</h3>
        <table class="comparison-table">
            <thead>
                <tr>
                    <th>운전 포인트</th>
                    <th>요구 유량 (Q)</th>
                    <th>화재안전기준 상 토출압력 (H) 한계</th>
                    <th>공학적 실무 목적</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>① 체절 운전점<br>(Shut-off Point)</strong></td>
                    <td>$Q = 0\%$ (무부하)</td>
                    <td>정격 토출 압력의 <strong>$140\%$ 이하</strong></td>
                    <td>정격 대비 140% 초과 시 소방 고압 배관 파손 방지 및 과압 한계 검증. (순환배관 릴리프 작동 타깃 지점)</td>
                </tr>
                <tr>
                    <td><strong>② 정격 운전점<br>(Rated Point)</strong></td>
                    <td>$Q = 100\%$ (정격 유량)</td>
                    <td>정격 토출 압력의 <strong>$100\%$ 이상</strong></td>
                    <td>최초 소방 설계 조건(헤드 정격 개방 시) 요구되는 설계 방출 유량 및 방출 압력 성능 충족 평가.</td>
                </tr>
                <tr>
                    <td><strong>③ 최대 운전점<br>(Overload Point)</strong></td>
                    <td>$Q = 150\%$ (과부하 유량)</td>
                    <td>정격 토출 압력의 <strong>$65\%$ 이상</strong></td>
                    <td>다량의 스프링클러 헤드 동시 개방 시와 같은 과부하 조건에서 펌프가 급격한 압력 붕괴 없이 소화수 공급 한계 유지 여부 평가.</td>
                </tr>
            </tbody>
        </table>
        
        <h3>5. 순환배관 및 릴리프 밸브(Relief Valve) 개방 메커니즘</h3>
        <ul>
            <li><strong>순환배관 설계 요건</strong>: 펌프 토출측 주 개폐밸브 2차측 이전 분기 지점에서 관경 **$20\,\text{mm}$ 이상**의 관을 분기하여 대기 방출 또는 수조로 복귀시킨다.</li>
            <li><strong>릴리프 밸브의 작동 조율</strong>: 릴리프 밸브는 체절 운전 시 수온 상승을 막기 위해 <strong>체절 압력 미만</strong>의 설정치에서 개방되도록 조정한다.
                - 펌프가 가동되어 체절점($Q=0$) 압력에 도달하면 릴리프 밸브가 즉시 개방되어 미량의 소화수($Q \approx 10\sim 20\,\text{L/min}$)를 방출 순환시킨다.
                - 유체 순환을 통해 케이싱 내 더워진 온수를 버리고 신선한 수원수를 인입함으로써 펌프 비등 파손을 원천 격리한다.
            </li>
        </ul>
        
        <div class="insight-box" style="border-left: 4px solid #ef4444;">
            <strong>실전 답안 작성 전략: 꼬리에 꼬리를 무는 연상 마인드맵</strong>
            <ul>
                <li><strong>중심 이미지</strong>: 주 밸브가 잠긴 채 <strong>붉은색 소방 펌프</strong>가 굉음을 내며 돌고 있을 때, 더워진 물(체온 상승)을 식히기 위해 <strong>순환배관 끝의 릴리프 밸브</strong>가 분수처럼 물을 품어 열을 배출하고, 옆 그래프에는 **140%-100%-65%**라는 안전 속도 제한 표지판이 서 있는 정경</li>
                <li><strong>흐름 설계</strong>: 
                    ① 체절운전 정의 및 수온상승 메커니즘 전개 ➡️ 
                    ② 소방펌프 3대 성능 기준 포인트 수치 규격화(140%, 100%, 65%) ➡️ 
                    ③ 성능시험 배관 계통 및 밸브 차단 절차 서술 ➡️ 
                    ④ 순환배관 릴리프 작동 압력 튜닝 방법 제시
                </li>
            </ul>
        </div>
        
        <h3>관련 기출문제</h3>
        <p class="exam-mapping">
            [제138회 1교시] 소방용 펌프의 체절압력 범위 및 릴리프 밸브 개방압력 설정 방법에 대하여 설명하시오.<br>
            [제119회 2교시] 소방펌프의 성능시험 방법과 3대 특성점에 만족하는 설계 압력 범위에 대하여 기술하시오.
        </p>
    </article>
    """
    
    # 4. New Q50 HTML (Cavitation & Pitting & NPSH)
    new_q50_html = r"""
    <article class="answer-sheet" id="q50">
        <div class="category-path-container">
            <span class="category-path">소방펌프 &gt; 수리학적 안전</span>
            <span class="category-badge">소방펌프</span>
        </div>
        <h2>[소방펌프] Question 50. 소방펌프의 공동현상(Cavitation) 발생 메커니즘, 공학적 장해 양상 및 공학적 예방대책</h2>
        
        <h3>1. 개요 및 출제 의도</h3>
        <p>공동현상(Cavitation)은 원심펌프 내부의 임펠러 고속 회전 시 발생되는 국부 감압 구간에서 액체의 정압이 운전 수온의 포화수증기압 이하로 떨어져 기포가 생성·발발하고, 이 기포들이 고압부에서 급격히 파괴되며 임펠러 날개깃에 물리적 손상(침식, Erosion)을 입히는 유체 파괴 현상이다. 공동현상이 생기는 미시적 작동 단계를 수립하고 성능 저하, 진동, 점식(Pitting) 등 공학적 한계 장해 양상과 설계 단계의 방지 대책을 종합적으로 규명한다.</p>
        
        <h3>2. 종합 모식도: 임펠러 표면 기포 생성(비등) 및 마이크로 제트(Micro-jet) 충격 파쇄 메커니즘</h3>
        <div class="zoomable-media" data-title="공동현상 마이크로 제트 파괴 메커니즘">
            <svg viewBox="0 0 700 350" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background: var(--bg-secondary); border-radius: 10px; padding: 10px;">
                <!-- Outer Border -->
                <rect width="680" height="330" x="10" y="10" rx="8" fill="none" stroke="var(--border)" stroke-width="1.5"/>
                
                <!-- Left: Bubble Evolution & Micro-jet Impact (미시적 파괴 메커니즘) -->
                <g transform="translate(30, 20)">
                    <rect width="320" height="290" rx="8" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1"/>
                    <text x="160" y="25" text-anchor="middle" fill="#dc2626" font-weight="bold" font-size="11">기포 파열에 의한 금속 표면 점식 메커니즘</text>
                    
                    <!-- Metal Wall (Impeller Blade) -->
                    <rect width="280" height="40" x="20" y="220" fill="#64748b" stroke="var(--border)"/>
                    <text x="160" y="245" text-anchor="middle" fill="#ffffff" font-weight="bold" font-size="9">임펠러 블레이드 금속 표면</text>
                    
                    <!-- Step 1: Intact Bubble -->
                    <circle cx="50" cy="120" r="18" fill="rgba(59, 130, 246, 0.2)" stroke="#3b82f6" stroke-width="1.5"/>
                    <text x="50" y="155" text-anchor="middle" fill="var(--text-secondary)" font-size="7">① 기포 이동 (저압부 ➔ 고압부)</text>
                    
                    <!-- Step 2: Asymmetric Collapse -->
                    <path d="M 130 110 C 145 110 155 125 150 135 C 145 145 120 140 120 130 C 120 120 120 110 130 110 Z" fill="rgba(245, 158, 11, 0.2)" stroke="#f59e0b" stroke-width="1.5"/>
                    <text x="150" y="165" text-anchor="middle" fill="var(--text-secondary)" font-size="7">② 비대칭 수축 변형</text>
                    
                    <!-- Step 3: Micro-jet Piercing -->
                    <ellipse cx="250" cy="130" rx="15" ry="12" fill="none" stroke="#ef4444" stroke-width="1.5"/>
                    <path d="M 250 100 L 250 150" stroke="#ef4444" stroke-width="2" marker-end="url(#arrow)"/>
                    <text x="250" y="165" text-anchor="middle" fill="#ef4444" font-weight="bold" font-size="7">③ 고속 마이크로 제트 분사</text>
                    
                    <!-- Pitting Mark -->
                    <path d="M 240 220 Q 250 230 260 220" fill="none" stroke="#ef4444" stroke-width="2"/>
                    <text x="250" y="210" text-anchor="middle" fill="#ef4444" font-weight="bold" font-size="8">침식 발생 (Pitting)</text>
                </g>
                
                <!-- Right: HQ Head drop chart -->
                <g transform="translate(370, 20)">
                    <rect width="280" height="290" rx="8" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1"/>
                    <text x="140" y="25" text-anchor="middle" fill="#2563eb" font-weight="bold" font-size="11">공동현상에 의한 펌프 성능 붕괴</text>
                    
                    <!-- HQ Coordinates -->
                    <line x1="30" y1="230" x2="250" y2="230" stroke="var(--text-primary)" stroke-width="1.2"/>
                    <line x1="30" y1="50" x2="30" y2="230" stroke="var(--text-primary)" stroke-width="1.2"/>
                    <text x="25" y="45" text-anchor="end" fill="var(--text-primary)" font-size="8">H</text>
                    <text x="240" y="245" fill="var(--text-primary)" font-size="8">Q</text>
                    
                    <!-- Normal HQ Curve -->
                    <path d="M 30 100 Q 120 110 240 220" fill="none" stroke="var(--text-secondary)" stroke-width="1.5" stroke-dasharray="3,3"/>
                    
                    <!-- Cavitated HQ Curve (드롭) -->
                    <path d="M 30 100 Q 120 110 150 130 L 155 220" fill="none" stroke="#ef4444" stroke-width="2.5"/>
                    <text x="180" y="150" fill="#ef4444" font-weight="bold" font-size="8">양정 급락 구간 (Drop-off)</text>
                    
                    <rect width="240" height="70" x="20" y="195" rx="4" fill="var(--bg-secondary)" stroke="var(--border)" stroke-width="0.5"/>
                    <text x="30" y="210" fill="var(--text-primary)" font-size="8">💡 공학적 발생 요건:</text>
                    <text x="30" y="225" fill="#ef4444" font-weight="bold" font-size="9">NPSH_av ≤ NPSH_re (발화 시작)</text>
                    <text x="30" y="240" fill="var(--text-secondary)" font-size="8">정압(P) &lt; 포화수증기압(Pv)</text>
                </g>
            </svg>
            <div class="diagram-explanation">
                <strong>모식도 설명:</strong> 좌측은 고압부로 진입한 기포가 순간 찌그러지며 상부에서 하부로 고속의 액체 제트류인 마이크로 제트(Micro-jet)를 형성하여 금속 벽면을 타격하고 금속 조직을 뜯어내 점식(Pitting)을 유발하는 파괴 역학도입니다. 우측은 공동현상 발생 시 펌프의 전양정-유량 곡선이 특정 유량 임계값을 기점으로 낭떠러지처럼 수직 급락(Drop-off)하는 성능 붕괴 양상입니다.
            </div>
            <div class="key-takeaway">
                <strong>초간단 직관적 이해 (비유법):</strong> 공동현상은 펌프 속에서 발생하는 **"초소형 물대포 폭탄 테러"**입니다. 물이 가진 정압이 뚝 떨어져서 기포(물거품)가 생겨났다가, 고압 지대에 가서는 **이 기포가 비대칭으로 찌그러지며 기포 중심을 관통하는 초속 수백 미터의 뾰족한 고속 바늘 물대포(마이크로 제트)를 발사**합니다. 이 미세 바늘 물대포가 단단한 쇠 날개(임펠러)를 초당 수천 번 이상 때려 갉아먹고 파괴하는 것이 펌프 궤멸의 실체입니다.
            </div>
        </div>
        
        <h3>3. 공동현상 (Cavitation)의 단계별 발생 메커니즘</h3>
        <p>공동현상은 유체동역학적 압력 분포 변화로 인해 액상에서 기상으로 상변화(Phase change)가 일어나는 역학적 순환 단계이다.</p>
        <ol>
            <li><strong>국부적 압력 강하 (Depressurization)</strong><br>원심펌프 임펠러 날개깃의 마찰, 와류, 급격한 유동 수축에 의해 유속이 극대화되는 <strong>임펠러 입구부</strong>에서 유체의 국부 정압이 급격히 저하된다.</li>
            <li><strong>기포 핵 형성 및 비등 (Vaporization)</strong><br>정압이 해당 유체 운전 수온의 **포화수증기압($P_v$) 이하**로 내려가는 순간, 물이 끓는점에 이르러 국부 비등을 개시하며 수많은 마이크로 기포(Vapor bubble)가 형성된다.</li>
            <li><strong>고압부 이동 및 급격한 응축 붕괴 (Imposition & Collapse)</strong><br>생성된 기포들이 흐름을 타고 압력이 높은 임펠러 외곽(토출부 방향)으로 고속 이송된다. 이때 고압 액체에 포위된 기포는 순간적으로 압축을 견디지 못하고 중심으로 수축하며 응축 붕괴(Implosion)를 겪는다.</li>
            <li><strong>마이크로 제트 분사 및 금속 파쇄 (Micro-jet Shock & Erosion)</strong><br>기포가 비대칭 붕괴할 때, 기포의 한쪽 벽이 반대편 벽을 뚫고 지나가는 고속의 **마이크로 제트(Micro-jet, 속도 약 $100\sim 500\,\text{m/s}$)**가 형성되어 임펠러 금속 표면을 집중 타격한다. 타격 시 가해지는 국부 피크 압력이 약 **$10,000\,\text{bar}$** 에 육박하여 금속 표면에 기계적 피로 균열을 내고 갉아먹는 점식(Pitting)을 유도한다.</li>
        </ol>
        
        <h3>4. 공동현상에 의한 펌프의 4대 공학적 장해</h3>
        <ul>
            <li><strong>전양정 및 펌프 효율의 급격한 붕괴 (performance drop-off)</strong>: 날개 깃 내에 가득 찬 기포 체적으로 인해 유체의 원활한 흐름 단면적이 축소되고 가압 효율이 떨어져 성능 곡선 상의 양정과 유량이 절벽식으로 급격히 감쇄한다.</li>
            <li><strong>격렬한 충격음과 기계 진동 유발</strong>: 기포 붕괴 시 분출되는 미시적 폭압파가 누적되어 펌프 본체와 배관에서 웅웅거리거나 돌멩이가 굴러가는 듯한 소음이 발생하며, 기계 베어링과 회전축 정밀도를 훼손한다.</li>
            <li><strong>임펠러 및 펌프 케이싱 내벽의 점식(Pitting) 파손</strong>: 금속 표면이 마이크로 제트에 의해 파내어져 스펀지 같은 다공성 부식 형상을 띠게 되며, 장기 운전 시 임펠러 깃이 부러져 나가 펌프가 궤멸된다.</li>
            <li><strong>물리적 기밀 누설(Mechanical Seal 손상)</strong>: 진동 공진으로 인해 축봉 장치가 변형되어 펌프 외부로 소화수가 대량 누수되는 2차 파괴로 전이된다.</li>
        </ul>
        
        <h3>5. 공동현상 차단을 위한 엔지니어링 방지 대책</h3>
        
        <h4>1) 시스템적 가용 흡입양정(NPSH_av) 향상 대책</h4>
        <ul>
            <li><strong>수위 가압식 (Positive Suction) 설계</strong>: 소방수조 수위를 펌프보다 높게 설정하여 흡입 실양정($H_s$)을 양(+)의 값으로 확보한다. (가장 확실한 공동현상 차단법)</li>
            <li><strong>흡입관 마찰손실($H_f$) 저감</strong>: 흡입 배관 굵기를 증경하여 유속을 저감($1.5\,\text{m/s}$ 이하)하고, 배관 내 스트레이너의 여과 유효면적을 넓게 설계하여 마찰손실 압력 강하를 막는다.</li>
            <li><strong>편심 레듀샤 상부 수평 시공</strong>: 흡입관 변경 부위에 편심 레듀샤를 사용하고 평평한 부분이 위로 가게 시공하여 배관 내부의 공기 체적 포켓을 방지한다.</li>
        </ul>
        
        <h4>2) 펌프 고유 필요흡입양정(NPSH_re)의 하향 대책</h4>
        <ul>
            <li><strong>펌프 회전 속도(\(N\))의 저감</strong>: 펌프 고유 필요흡입수두는 회전수의 대략 2~3승에 비례하여 늘어나므로 저속 극수 모터를 채용한다.</li>
            <li><strong>양흡입 (Double Suction) 임펠러 채택</strong>: 유량을 양쪽 방향으로 분할 인입하여 흡입 속도를 1/2로 낮추어 필요 정압을 크게 절감한다.</li>
        </ul>
        
        <div class="insight-box" style="border-left: 4px solid #f43f5e;">
            <strong>실전 답안 작성 전략: 꼬리에 꼬리를 무는 연상 마인드맵</strong>
            <ul>
                <li><strong>중심 이미지</strong>: 저압부로 들어간 <strong>물방울 이탈 전하</strong>가 기포로 비등했다가, 고압부에서 찌그러지며 금속 표면으로 <strong>황색 마이크로 제트 바늘 화살</strong>을 뿜어 단단한 <strong>회색 임펠러 날개에 곰보 점식(Pitting)</strong>을 내고 펌프 전양정을 수직 낙하시킬 때, <strong>가압 흡입의 양(+)의 실양정 방패</strong>로 기포 발생을 억제하는 계통</li>
                <li><strong>흐름 설계</strong>: 
                    ① 공동현상 정의 및 물리 메커니즘 4단계(압력강하-기화-응축붕괴-마이크로제트 타격) 설명 ➡️ 
                    ② 캐비테이션 4대 공학적 한계 장해 양상 정립 ➡️ 
                    ③ NPSH_av 향상 방안(가압수조, 흡입관 증경, 편심레듀샤 상부편평) ➡️ 
                    ④ NPSH_re 저감 방안(저회전 펌프, 양흡입 펌프) 연계 결론
                </li>
            </ul>
        </div>
        
        <h3>관련 기출문제</h3>
        <p class="exam-mapping">
            [제133회 2교시] 펌프의 캐비테이션 발생에 따른 영향 및 방지대책을 유효흡입수두(NPSHav)와 필요흡입수두(NPSHre)를 사용하여 설명하시오.<br>
            [제127회 1교시] 소방펌프 흡입측에 버터플라이 밸브를 설치하지 못하는 이유와 설치 시 발생할 수 있는 현상에 대하여 쓰시오.
        </p>
    </article>
    """
    
    # 5. Replace articles content in BeautifulSoup
    q49_art.replace_with(BeautifulSoup(new_q49_html, "html.parser").article)
    print("Successfully replaced Q49 content inside soup.")
    
    q50_art.replace_with(BeautifulSoup(new_q50_html, "html.parser").article)
    print("Successfully replaced Q50 content inside soup.")
    
    # 6. Restructure headers of these 2 new articles (since they were just injected)
    # We will do header splitting for q49 and q50 to fit standard headers
    for q_id in ["q49", "q50"]:
        art = soup.find("article", id=q_id)
        if art:
            header = art.find(class_="sheet-header")
            if header:
                category_container = header.find(class_="category-path-container")
                question_meta = header.find(class_="question-meta")
                question_title = header.find(class_="question-title")
                if not question_title:
                    question_title = header.find("h2")
                score_badge = header.find(class_="score-badge")
                
                header_left = soup.new_tag("div", attrs={"class": "header-left"})
                header_right = soup.new_tag("div", attrs={"class": "header-right"})
                
                if category_container:
                    header_left.append(category_container.extract())
                if question_meta:
                    header_left.append(question_meta.extract())
                if question_title:
                    header_left.append(question_title.extract())
                if score_badge:
                    header_right.append(score_badge.extract())
                    
                header.clear()
                header.append(header_left)
                header.append(header_right)
                print(f"Restructured header for {q_id} to standard header-left/right.")
                
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Successfully saved updated HTML to: {file_path}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = update_q49_q50(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied updated HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
