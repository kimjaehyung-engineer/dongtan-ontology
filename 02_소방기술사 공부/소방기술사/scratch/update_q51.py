import os
import shutil
from bs4 import BeautifulSoup

def update_q51_article(file_path):
    print(f"Updating Question 51 inside: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_q51"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. Target article with id="q51"
    q51_art = soup.find("article", id="q51")
    if not q51_art:
        print("Error: Could not find article with id='q51' in HTML.")
        return False
        
    # 2. Comprehensive Premium Answer HTML
    new_q51_html = r"""
    <article class="answer-sheet" id="q51">
        <div class="category-path-container">
            <span class="category-path">소방펌프 &gt; 수리학적 특성</span>
            <span class="category-badge">소방펌프</span>
        </div>
        <h2>[소방펌프] Question 51. 소방펌프의 유효흡입수두(\(\text{NPSH}_{av}\))와 필요흡입수두(\(\text{NPSH}_{re}\))의 상호 상관관계 및 운전 마진</h2>
        
        <h3>1. 개요 및 출제 의도</h3>
        <p>소방용 가압송수장치의 중심인 원심펌프에서 흡입성능을 규명하는 순흡입수두(NPSH, Net Positive Suction Head)는 공동현상(Cavitation) 발생 예방과 소방시설의 기동 신뢰성을 좌우하는 유체역학적 핵심 인자이다. 설비 계통의 조건에 따라 결정되는 공급 수두인 유효흡입수두(\(\text{NPSH}_{av}\))와 펌프 자체 임펠러 입구 마찰 강하분을 극복하기 위해 요구되는 필요흡입수두(\(\text{NPSH}_{re}\))의 정량적 메커니즘을 밝히고, 안전 운전 마진 및 배관 설계 개선책을 고찰한다.</p>
        
        <h3>2. 종합 모식도: NPSH 배관 계통도 및 임펠러 입구 압력 강하/기포 소멸 메커니즘</h3>
        <div class="zoomable-media" data-title="NPSH 계통 및 압력 강하 분포도">
            <svg viewBox="0 0 700 350" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background: var(--bg-secondary); border-radius: 10px; padding: 10px;">
                <!-- Outer Border -->
                <rect width="680" height="330" x="10" y="10" rx="8" fill="none" stroke="var(--border)" stroke-width="1.5"/>
                
                <!-- Left: Pump Suction System Geometry (흡입 계통 기하학) -->
                <g transform="translate(30, 20)">
                    <rect width="280" height="290" rx="8" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1"/>
                    <text x="140" y="25" text-anchor="middle" fill="#2563eb" font-weight="bold" font-size="12">흡입 배관 수리학적 에너지 구배</text>
                    
                    <!-- Water Tank -->
                    <rect width="80" height="100" x="30" y="120" fill="none" stroke="var(--border)" stroke-width="2"/>
                    <line x1="30" y1="140" x2="110" y2="140" stroke="#3b82f6" stroke-width="2"/>
                    <text x="70" y="160" text-anchor="middle" fill="#3b82f6" font-size="9">수위면 (Pa)</text>
                    
                    <!-- Pump Centerline -->
                    <circle cx="210" cy="180" r="20" fill="#94a3b8" stroke="var(--border)" stroke-width="1.5"/>
                    <text x="210" y="183" text-anchor="middle" fill="#1e293b" font-weight="bold" font-size="8">펌프</text>
                    
                    <!-- Suction Pipe -->
                    <path d="M 90 200 L 190 200 L 190 180" stroke="#3b82f6" stroke-width="3" fill="none"/>
                    
                    <!-- Heights and Loss -->
                    <line x1="110" y1="140" x2="210" y2="140" stroke="var(--text-secondary)" stroke-dasharray="2,2"/>
                    <line x1="210" y1="140" x2="210" y2="180" stroke="#ef4444" stroke-width="1.5"/>
                    <text x="220" y="165" fill="#ef4444" font-weight="bold" font-size="8">Hs (흡입 실양정)</text>
                    <text x="140" y="225" text-anchor="middle" fill="var(--text-secondary)" font-size="8">흡입배관 손실 Hf</text>
                </g>
                
                <!-- Right: Impeller Inlet Pressure drop profile (압력 강하 프로파일) -->
                <g transform="translate(340, 20)">
                    <rect width="310" height="290" rx="8" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1"/>
                    <text x="155" y="25" text-anchor="middle" fill="#dc2626" font-weight="bold" font-size="12">임펠러 입구 압력 변화 및 캐비테이션</text>
                    
                    <!-- Coordinates -->
                    <line x1="40" y1="240" x2="280" y2="240" stroke="var(--text-primary)" stroke-width="1.5"/>
                    <line x1="40" y1="50" x2="40" y2="240" stroke="var(--text-primary)" stroke-width="1.5"/>
                    <text x="35" y="45" text-anchor="end" fill="var(--text-primary)" font-size="8">압력 (P)</text>
                    <text x="270" y="255" fill="var(--text-primary)" font-size="8">유동경로</text>
                    
                    <!-- Vapor Pressure line (포화수증기압 Pv) -->
                    <line x1="40" y1="160" x2="280" y2="160" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="3,3"/>
                    <text x="240" y="152" fill="#ef4444" font-weight="bold" font-size="8">포화수증기압 (Pv)</text>
                    
                    <!-- Pressure drop curve -->
                    <path d="M 40 80 Q 100 80 140 180 T 220 100 L 270 100" fill="none" stroke="#2563eb" stroke-width="2"/>
                    <text x="65" y="95" fill="#2563eb" font-size="8">흡입구 압력</text>
                    <text x="140" y="200" fill="#ea580c" font-weight="bold" font-size="8">임펠러 날깃 초입 압력 강화</text>
                    
                    <!-- Cavitation zone (기포 발생 구역) -->
                    <ellipse cx="140" cy="180" rx="15" ry="8" fill="#fbbf24" opacity="0.3"/>
                    <circle cx="135" cy="178" r="2" fill="#ea580c"/>
                    <circle cx="145" cy="182" r="3" fill="#ea580c"/>
                    <text x="140" y="168" text-anchor="middle" fill="#ea580c" font-size="7">기포 발생(Pv 돌파)</text>
                    
                    <!-- NPSH_re interval -->
                    <line x1="200" y1="160" x2="200" y2="100" stroke="#8b5cf6" stroke-width="1" marker-end="url(#arrow)" marker-start="url(#arrow)"/>
                    <text x="205" y="130" fill="#8b5cf6" font-weight="bold" font-size="8">NPSH_re 마진 필요</text>
                </g>
            </svg>
            <div class="diagram-explanation">
                <strong>모식도 설명:</strong> 좌측은 소방 펌프 가동 시 대기압 수두에서 흡입 실양정($H_s$)과 흡입 배관 마찰손실($H_f$)이 에너지선을 깎아 먹는 물리 계통입니다. 우측은 액체가 임펠러 날개 깃(Blade) 입구로 흐를 때 국부 수축으로 인해 압력이 급격히 저하되는 선로를 나타냅니다. 이 하강 압력이 포화수증기압($P_v$) 선 밑으로 내려가면 물이 기화하며 기포가 솟구치다 고압부에서 깨져 날개에 구멍을 냅니다(침식).
            </div>
            <div class="key-takeaway">
                <strong>초간단 직관적 이해 (비유법):</strong> 펌프가 빨아 올리는 물이 가진 에너지 여유분인 **유효흡입수두($NPSH_{av}$)**는 내 지갑 안의 돈(가용 수두)이며, 펌프가 안 망가지고 물을 품기 위해 임펠러 입구에서 뜯어가는 통행세인 **필요흡입수두($NPSH_{re}$)**는 필수 세금(요구 수두)입니다. **지갑에 든 돈이 세금보다 30% 이상(안전 마진) 넉넉히 들어 있어야 가난(공동현상)으로 인한 부도(펌프 파손)를 막을 수 있습니다**.
            </div>
        </div>
        
        <h3>3. 유효흡입수두(\(\text{NPSH}_{av}\))의 정의 및 유도공식</h3>
        <p>유효흡입수두(Net Positive Suction Head Available)는 펌프 흡입구 플랜지 중심에서 계통의 위치, 대기압, 마찰손실, 수증기압 조건에 따라 공급되는 <strong>실제 유효 수리학적 정압 여유분</strong>이다.</p>
        
        <h4>1) 기본 계산 공식</h4>
        <div class="formula-box" style="margin: 10px 0; font-family: monospace; font-size: 1.1rem; text-align: center; font-weight: bold;">
            \text{NPSH}_{av} = H_a \pm H_s - H_f - H_v \quad [m]
        </div>
        
        <h4>2) 개별 수두 인자의 상세 물리 정의</h4>
        <ul>
            <li><strong>대기압 수두 (\(H_a\))</strong>: 대기가 수조 수면을 누르는 대기압을 수두로 나타낸 것. 해수면 표준대기압 조건($1.0332\,\text{kg/cm}^2$)에서 <strong>약 $10.33\,\text{m}$</strong> 이다. (\(H_a = P_a / \rho g\))</li>
            <li><strong>흡입 실양정 (\(H_s\))</strong>: 수면에서 펌프 흡입구 중심까지의 수직 거리.
                - <strong>가압 흡입 (수면이 펌프보다 높은 경우)</strong>: $+H_s$ 적용 (유효 수두 증가하여 유리).
                - <strong>부압 흡입 (수면이 펌프보다 낮은 경우)</strong>: $-H_s$ 적용 (유효 수두 감소하여 불리).
            </li>
            <li><strong>흡입 배관 마찰손실 (\(H_f\))</strong>: 흡입 여과망(풋밸브, 스트레이너), 흡입 배관 및 이음류 등에서 발생하는 총 압력손실 수두.</li>
            <li><strong>포화수증기압 수두 (\(H_v\))</strong>: 운전 수온에서의 포화수증기압. 상온($20^\circ\text{C}$) 물 기준 약 $0.24\,\text{m}$ 수준이나, 수온이 상승할수록 급격히 증가하여 유효흡입수두를 저하시킨다. (\(H_v = P_v / \rho g\))</li>
        </ul>
        
        <h3>4. 필요흡입수두(\(\text{NPSH}_{re}\))의 물리적 성상 및 결정 변수</h3>
        <p>필요흡입수두(Net Positive Suction Head Required)는 펌프 입구 깃에서 기류 수축과 마찰로 인해 발생하는 압력 강하분을 극복하고, 액체의 기화를 막기 위해 <strong>펌프 자체에 요구되는 흡입 플랜지 단면의 최소 절대 정압 수두</strong>이다.</p>
        <ul>
            <li><strong>결정 주체</strong>: 펌프 흡입구 및 회전차(임펠러) 형상 설계(날개 깃 두께, 각도, 입구 단면적 등)와 펌프 회전 속도에 의해 결정되는 <strong>펌프 제조사 고유의 성능 고정 지표</strong>이다. (계통 배관과는 무관)</li>
            <li><strong>유량 증가와의 상관성</strong>: 필요흡입수두는 펌프 송출 유량의 대략 1.5~2승에 비례하여 증가한다. ($\text{NPSH}_{re} \propto Q^2$) 이에 따라 소방펌프 과부하 운전 시 캐비테이션 유발 확률이 커진다.</li>
            <li><strong>제조사 시험법 (3% Head Drop Test)</strong>: 펌프 흡입압력을 서서히 내릴 때, 펌프의 전양정(Head)이 정상치 대비 3% 저하하는 시점의 흡입 수두를 측정하여 $\text{NPSH}_{re}$로 규정한다.</li>
        </ul>
        
        <h3>5. \(\text{NPSH}_{av}\)와 \(\text{NPSH}_{re}\)의 상호 관계 및 공동현상 판정</h3>
        <p>펌프 운전의 안전 성능과 캐비테이션 발생 여부는 두 수두의 대소 관계에 의해 지배된다.</p>
        <ol>
            <li><strong>\(\text{NPSH}_{av} &gt; \text{NPSH}_{re}\) (안전 운전 상태)</strong><br>공급되는 유효 에너지가 펌프 입구의 압력 강하 요구분보다 크므로, 임펠러 내부 임의 지점에서도 액체의 압력이 포화수증기압($P_v$) 이하로 떨어지지 않아 공동현상이 전혀 발생하지 않는다.</li>
            <li><strong>\(\text{NPSH}_{av} \le \text{NPSH}_{re}\) (공동현상 발현 상태, Cavitation)</strong><br>요구되는 최저 압력을 만족하지 못하므로, 날개 깃 입구의 최저 압력 지점에서 물이 순간적으로 부글부글 끓어오르며 포화증기 기포(Vapor bubble)가 형성된다. 이 기포가 임펠러 고압부로 넘어가며 순간 압착 파쇄(약 $10,000\,\text{bar}$ 의 충격 압력)를 일으켜 심각한 소음, 진압 진동, 그리고 양정 저하 및 임펠러 익편 침식 파손(Erosion)을 초래한다.</li>
        </ol>
        
        <h3>6. 안전 운전 마진(Safety Margin) 및 소방 배관 대책</h3>
        
        <h4>1) 공학적 안전 운전 마진 수치</h4>
        <p>이론적으로는 두 수두가 같을 때 임계가 발생하나, 유량 변동 및 수압 서지에 대비하기 위해 설계 안전율(Margin)을 둔다.</p>
        <ul>
            <li><strong>유량 연동 마진</strong>: <strong>$\text{NPSH}_{av} \ge \text{NPSH}_{re} \times 1.3$</strong> (30% 여유 확보) 또는 최소 <strong>$\text{NPSH}_{av} \ge \text{NPSH}_{re} + 0.5\,\text{m} \sim 1.0\,\text{m}$</strong> 을 유지하도록 설계한다.</li>
            <li><strong>소방펌프의 가혹성</strong>: 소방펌프는 평상시 대기 상태에서 급격히 최대 운전점(정격 유량의 150%)으로 기동한다. 유량 급증 시 배관 마찰손실($H_f$)과 펌프의 필요흡입수두($\text{NPSH}_{re}$)가 동시 폭증하므로, 반드시 최대 유량점을 기준으로 안전 마진이 만족되도록 설계해야 신뢰성을 보장할 수 있다.</li>
        </ul>
        
        <h4>2) 소방 흡입 배관 설계 개선책</h4>
        <ul>
            <li><strong>가압 흡입식(Foot-Valve 배제) 배치</strong>: 소방 수조의 수위를 펌프 흡입구보다 항상 높게 위치시킨다($+H_s$). 수압이 항상 양(+)의 값을 가져 공동현상 리스크가 원천 차단된다.</li>
            <li><strong>흡입관 구경의 증경</strong>: 흡입측 관로 유속을 $1.5\,\text{m/s}$ 이하(토출 배관 $3.0\,\text{m/s}$ 이하 대비 절반)로 넓혀 유량 변동 시의 배관 마찰손실 수두($H_f$)를 대폭 저감한다.</li>
            <li><strong>편심 레듀샤(Eccentric Reducer) 편평부 상부 설치</strong>: 수평관의 리듀싱 피팅 시 상부를 편평(Flat top)하게 시공하여 관 상부에 공기 고임(Air pocket) 현상을 막고 기류 막힘에 의한 유속 상승 및 수두 손실을 방지한다.</li>
        </ul>
        
        <div class="insight-box" style="border-left: 4px solid #f43f5e;">
            <strong>실전 답안 작성 전략: 꼬리에 꼬리를 무는 연상 마인드맵</strong>
            <ul>
                <li><strong>중심 이미지</strong>: 수조의 <strong>파란 소화수(Ha+Hs)</strong>가 구불구불한 <strong>흡입 배관 저항(Hf)</strong> 언덕을 지나며 기력이 쇠한 상태로 펌프 입구에 들어설 때, <strong>임펠러 날개 깃(Blade) 입구의 저압 함정(NPSH_re)</strong>을 만나 <strong>기포 폭탄(Cavitation)</strong>을 일으키려 하지만, <strong>30%의 지갑 돈 여유(안전마진)</strong>와 <strong>가압 흡입 수위(+Hs)</strong> 방패로 극복하는 수력도</li>
                <li><strong>흐름 설계</strong>: 
                    ① NPSH와 Cavitation 발생 원인 정의 ➡️ 
                    ② NPSH_av 인자별 공식($H_a \pm H_s - H_f - H_v$) 정밀 분해 기술 ➡️ 
                    ③ NPSH_re 펌프 고유의 3% 양정감쇄 시험값 기술 ➡️ 
                    ④ 안전 마진 관계식($\times 1.3$ 또는 $+0.5\text{m}$) 수치 명시 ➡️ 
                    ⑤ 소방설비 3대 흡입 개선 대책(가압수조, 증경, 편심레듀샤 상부편평 시공) 제시
                </li>
            </ul>
        </div>
        
        <h3>관련 기출문제</h3>
        <p class="exam-mapping">
            [제138회 1교시] 소방용 펌프의 필요유효흡입수두(NPSHre)를 산출하는 방법에 대하여 설명하시오.<br>
            [제133회 2교시] 펌프의 캐비테이션 발생에 따른 영향 및 방지대책을 유효흡입수두(NPSHav)와 필요흡입수두(NPSHre)를 사용하여 설명하시오.
        </p>
    </article>
    """
    
    # 3. Replace article content
    q51_art.replace_with(BeautifulSoup(new_q51_html, "html.parser").article)
    print("Successfully replaced Q51 content inside soup.")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Successfully saved updated HTML to: {file_path}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = update_q51_article(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied updated HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
