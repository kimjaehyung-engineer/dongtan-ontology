import os
import shutil
from bs4 import BeautifulSoup

def update_q52_article(file_path):
    print(f"Updating Question 52 inside: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_q52"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. Target article with id="q52"
    q52_art = soup.find("article", id="q52")
    if not q52_art:
        print("Error: Could not find article with id='q52' in HTML.")
        return False
        
    # 2. Comprehensive Premium Answer HTML
    new_q52_html = r"""
    <article class="answer-sheet" id="q52">
        <div class="category-path-container">
            <span class="category-path">소방펌프 &gt; 수리학적 안전</span>
            <span class="category-badge">소방펌프</span>
        </div>
        <h2>[소방펌프] Question 52. 소방배관 계통의 수격작용(Water Hammering) 및 펌프의 맥동현상(Surging) 발생 요인과 방지 대책</h2>
        
        <h3>1. 개요 및 출제 의도</h3>
        <p>수계 소화설비에서 소화수 방출 신뢰성을 지탱하는 배관망 계통은 과도한 과압과 동적 진동 리스크에 상시 노출되어 있다. 급격한 유량 변화에 의해 계통 내 극심한 충격파가 생기는 수격작용(Water Hammering)과, 펌프 성능 특성 및 배관 체적 구성 요건에 의해 유량과 압력이 정기적으로 요동치는 자가 진동 현상인 맥동현상(Surging)은 소방시설의 파손 및 오동작을 초래하는 주요인이다. 두 현상의 발생 요인을 수리학적으로 분석하고 입체적인 방지 대책을 수록하고자 한다.</p>
        
        <h3>2. 종합 모식도: 수격 작용 충격파 전파 및 펌프 산형 곡선 상의 서징(Surging) 메커니즘</h3>
        <div class="zoomable-media" data-title="수격작용 및 맥동현상 발생 계통도">
            <svg viewBox="0 0 700 350" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background: var(--bg-secondary); border-radius: 10px; padding: 10px;">
                <!-- Definitions for gradients -->
                <defs>
                    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--text-primary)"/>
                    </marker>
                </defs>
                <!-- Outer Border -->
                <rect width="680" height="330" x="10" y="10" rx="8" fill="none" stroke="var(--border)" stroke-width="1.5"/>
                
                <!-- Left: Water Hammering (수격작용 배관 전파) -->
                <g transform="translate(30, 20)">
                    <rect width="280" height="290" rx="8" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1"/>
                    <text x="140" y="25" text-anchor="middle" fill="#ef4444" font-weight="bold" font-size="11">수격작용 (Water Hammering) 충격파</text>
                    
                    <!-- Pipe and Valve -->
                    <rect width="180" height="25" x="30" y="120" fill="#94a3b8" stroke="var(--border)"/>
                    <rect width="12" height="40" x="210" y="112" fill="#ef4444" stroke="var(--border)"/>
                    <text x="216" y="100" text-anchor="middle" fill="#ef4444" font-weight="bold" font-size="8">밸브 급폐쇄</text>
                    
                    <!-- Shock wave pattern (충격파 반사) -->
                    <path d="M 205 132 C 180 120 170 144 145 132 C 120 120 110 144 85 132" stroke="#ea580c" stroke-width="2.5" fill="none"/>
                    <path d="M 85 132 C 60 120 50 144 30 132" stroke="#ea580c" stroke-width="2" fill="none" stroke-dasharray="2,2"/>
                    <text x="130" y="160" text-anchor="middle" fill="#ea580c" font-weight="bold" font-size="9">충격압력파 전파 (a ≈ 1000 m/s)</text>
                    
                    <!-- Arrester Solution -->
                    <circle cx="120" cy="80" r="10" fill="#10b981"/>
                    <rect width="8" height="15" x="116" y="90" fill="#10b981"/>
                    <text x="120" y="65" text-anchor="middle" fill="#10b981" font-weight="bold" font-size="8">수격방지기 (Arrester)</text>
                </g>
                
                <!-- Right: Surging (맥동현상 펌프 곡선) -->
                <g transform="translate(340, 20)">
                    <rect width="310" height="290" rx="8" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1"/>
                    <text x="155" y="25" text-anchor="middle" fill="#2563eb" font-weight="bold" font-size="11">맥동현상 (Surging) 펌프 곡선 거동</text>
                    
                    <!-- HQ Graph Coordinates -->
                    <line x1="40" y1="230" x2="270" y2="230" stroke="var(--text-primary)" stroke-width="1.5"/>
                    <line x1="40" y1="50" x2="40" y2="230" stroke="var(--text-primary)" stroke-width="1.5"/>
                    <text x="35" y="45" text-anchor="end" fill="var(--text-primary)" font-size="8">양정 (H)</text>
                    <text x="260" y="245" fill="var(--text-primary)" font-size="8">유량 (Q)</text>
                    
                    <!-- Mountain-shape Pump Curve (산형 곡선) -->
                    <path d="M 40 180 Q 120 80 250 200" fill="none" stroke="#dc2626" stroke-width="2"/>
                    <circle cx="120" cy="110" r="5" fill="#f59e0b"/>
                    <text x="120" y="95" text-anchor="middle" fill="#f59e0b" font-weight="bold" font-size="8">정상부(산)</text>
                    
                    <!-- Surging swing arrows -->
                    <path d="M 70 125 L 170 125" stroke="#8b5cf6" stroke-width="1.5" marker-end="url(#arrow)" marker-start="url(#arrow)"/>
                    <text x="120" y="142" text-anchor="middle" fill="#8b5cf6" font-weight="bold" font-size="8">좌우 압력/유량 진동 (서징 구간)</text>
                    <text x="70" y="200" fill="var(--text-secondary)" font-size="7">※ 정상부 좌측(Q_partial)</text>
                    <text x="70" y="212" fill="var(--text-secondary)" font-size="7">부분유량 불연속 발생</text>
                </g>
            </svg>
            <div class="diagram-explanation">
                <strong>모식도 설명:</strong> 좌측은 배관 내 흐르던 유체 속도가 차단 밸브의 급격한 차단으로 급랭 압력파를 받아 배관을 타고 음속에 준하는 전파 속도($a$)로 반사 운동을 겪는 수격작용입니다. 우측은 펌프의 성능곡선이 우상향(산형)일 때, 정점의 왼쪽 불안정 영역에서 기류가 압력 용기(Air Pocket)의 신축 작용에 힘입어 양정과 유량이 주기적으로 요동치는 맥동(Surging) 운동 곡선입니다.
            </div>
            <div class="key-takeaway">
                <strong>초간단 직관적 이해 (비유법):</strong> **수격작용**은 빠르게 달리던 소방수 열차가 갑자기 나타난 바위벽(갑자기 닫힌 밸브)에 쾅 부딪혀 **열차 칸들이 찌그러지며 강한 쇠망치 충격음(쾅쾅)을 뿜어 배관을 부수는 충격**이고, **맥동현상**은 펌프가 뿜어내는 기운(압력)과 배관 풍선(공기 주머니)의 팽창력이 타이밍이 엇박자로 꼬여 **펌프가 컥컥거리며 불규칙한 맥박(유량 요동)을 짚으며 미친 듯이 떠는 진동 현상**입니다.
            </div>
        </div>
        
        <h3>3. 수격작용(Water Hammering)의 발생 요인 및 수식</h3>
        <p>수격작용은 관로를 흐르던 물의 운동 에너지(Velocity)가 급격한 밸브 폐쇄 등으로 인해 압력 에너지(Pressure)로 일순간에 에너지 치환되며 강렬한 소음과 물리적 파괴력을 내뿜는 급격한 압력 파동 현상이다.</p>
        
        <h4>1) 주요 발생 요인</h4>
        <ul>
            <li><strong>밸브의 급격한 조작</strong>: 가지배관 말단 스프링클러 헤드 개방 후 릴리프 장치 조작이나 토출 주밸브의 급작스러운 수동 폐쇄.</li>
            <li><strong>펌프의 급격한 기동 및 정지 (Blackout)</strong>: 화재 신호 감지로 펌프가 급가속 회전 시 순간 수동 급압이 발생하거나, 동력 전원 정전으로 펌프가 팽하고 멈출 때 관성 흐름이 갈라지며 압력 하강 후 배압 충격 발생.</li>
        </ul>
        
        <h4>2) Joukowsky 압력 상승 공식</h4>
        <p>밸브 폐쇄 시간이 관로 압력파 왕복 시간($T_c = 2L/a$)보다 짧을 때 발생하는 급격한 압력 상승량($\Delta P$)은 다음과 같다.</p>
        <div class="formula-box" style="margin: 10px 0; font-family: monospace; font-size: 1.1rem; text-align: center; font-weight: bold;">
            \Delta P = \rho \cdot a \cdot \Delta v \quad [Pa] \quad \left( \text{수두 환산 시 } \Delta H = \frac{a \cdot \Delta v}{g} \right)
        </div>
        <ul>
            <li>$\rho$: 유체의 밀도 ($kg/m^3$)</li>
            <li>$a$: 압력파 전파 속도. 배관 재질의 탄성과 유체 압축성을 결합한 음속 수치 (철제 배관 내 약 $1,000 \sim 1,200\,\text{m/s}$)</li>
            <li>$\Delta v$: 유체 유속의 변화량 ($m/s$)</li>
        </ul>
        
        <h3>4. 펌프 맥동현상(Surging)의 4대 발생 요인 (조건)</h3>
        <p>맥동현상(서징)은 펌프의 토출 유량과 압력이 일정한 주기를 갖고 주기적으로 증가와 감소를 반복하며 배관 전체가 규칙적으로 공진 요동하는 자가 흥분 진동 상태이다. 아래 **4대 물리적 조건**이 동시 충족될 때 트리거된다.</p>
        <ol>
            <li><strong>펌프 성능 H-Q 곡선이 우상향(산형, Mountain-shape) 특성을 가질 것</strong><br>체절 운전점에서 일정 유량까지 양정이 상승하다가 다시 하강하는 우상향 곡선 구간이 존재해야 한다.</li>
            <li><strong>펌프 토출 배관망 내부에 '공기 주머니(Air chamber/Air pocket)'가 존재할 것</strong><br>기상의 탄성 체적(공기실, 압력챔버 상부 공기층)이 에너지를 상시 축적·방출하는 완충 스프링 역할을 수행한다.</li>
            <li><strong>유량 제어 밸브(조절판)가 공기실 하류 측(배관 말단부)에 설치되어 있을 것</strong><br>체적 부하 뒤에서 가압 흐름 통제가 가해지는 유압 구조 요건을 뜻한다.</li>
            <li><strong>펌프의 운전점이 성능 곡선 정상부(산)의 좌측 영역(불안정 영역)에 있을 것</strong><br>이 부분유량 운전 구간에서는 압력이 올라가면 유량이 오히려 감소하고, 압력이 낮아지면 유량이 늘어나는 불안정한 엇박자 사이클이 발달한다.</li>
        </ol>
        
        <h3>5. 두 현상의 소방 공학적 방지 대책</h3>
        
        <h4>1) 수격작용 (Water Hammering) 방지 대책</h4>
        <ul>
            <li><strong>수격방지기(Water Hammer Arrester) 설치</strong>: 배관의 구부러지는 굴곡부 및 밸브 직전 상류 측에 벨로즈/질소 충전식 방지기를 가설하여 순간 과압 압격파를 내부 질소 쿠션으로 상쇄 흡수한다.</li>
            <li><strong>완폐식 (Slow-closing) 밸브 및 릴리프 장치 도입</strong>: 밸브 폐쇄 시 모터 제어로 수 초에 걸쳐 천천히 닫히도록 조절하여 유속 변화율($\Delta v / dt$)을 제어한다.</li>
            <li><strong>서지 탱크(Surge Tank) 시공</strong>: 압력 급강하 시 즉시 물을 채워 배관 내부 압력을 보존하고 수격파를 완화한다.</li>
        </ul>
        
        <h4>2) 맥동현상 (Surging) 방지 대책</h4>
        <ul>
            <li><strong>우하향(단조 감소형) 특성의 펌프 채택</strong>: 소방펌프 화재안전기준 상 체절 양정의 140% 한계 규격 요건과 맞추어, 체절 압력에서 최대 운전점까지 양정이 끊임없이 단조 감소하는 우하향(Flat-Drooping) 곡선 특성 펌프를 선정하여 우상향 불안정 구역을 원천 배제한다.</li>
            <li><strong>토출 바이패스(Bypass) 릴리프 운전</strong>: 부분 부하 유량 발생 시 바이패스 배관을 통해 유량을 펌프 성능곡선의 정상부 우측 안전 영역($Q_{safe}$) 이상으로 상시 방출 순환시켜 부분 부하 불안정 구간 진입을 예방한다.</li>
            <li><strong>배관 공기 포켓 배출</strong>: 배관 계통 내 축적된 공기를 완전 배출하고, 정기적으로 에어 벤트 밸브를 관리하여 탄성 기상 체적 생성을 억제한다.</li>
            <li><strong>밸브 위치의 펌프 토출구 직후 이설</strong>: 배관 체적(공기 고임부)보다 밸브를 상류(펌프 토출 팁 부근)에 밀착 배치하여, 펌프와 밸브 사이에 축적되는 완충 체적을 최소화한다.</li>
        </ul>
        
        <div class="insight-box" style="border-left: 4px solid #f43f5e;">
            <strong>실전 답안 작성 전략: 꼬리에 꼬리를 무는 연상 마인드맵</strong>
            <ul>
                <li><strong>중심 이미지</strong>: 밸브가 갑자기 탁 닫힐 때 <strong>음속의 충격파(a=1,000m/s)</strong>가 반사되어 <strong>압격 폭탄(Water Hammer)</strong>을 만들려 할 때 <strong>수격방지기 질소 주머니</strong>가 충격을 흡수하고, 옆 펌프에서는 <strong>우상향 산형 곡선</strong>의 미로에 갇혀 <strong>압력실 공기 스프링</strong> 때문에 컥컥거리며 <strong>맥동(Surging)</strong>할 때 <strong>릴리프 밸브 바이패스</strong>로 물을 토출시켜 탈출하는 입체 공학 밸런스</li>
                <li><strong>흐름 설계</strong>: 
                    ① 수격작용 발생 원인 및 Joukowsky 공식 유도 기술 ➡️ 
                    ② 수격 대책(수격방지기, Slow-closing 밸브) ➡️ 
                    ③ 맥동현상(서징) 4대 구성 조건 상세 정의 ➡️ 
                    ④ 맥동 대책(우하향 펌프 곡선 선정, 릴리프 바이패스, 밸브 이설) 논리적 매핑
                </li>
            </ul>
        </div>
        
        <h3>관련 기출문제</h3>
        <p class="exam-mapping">
            [제122회 4교시] 소방배관 계통의 수격작용(Water Hammering) 및 펌프의 맥동현상(Surging) 발생 요인과 방지 대책에 대하여 설명하시오.<br>
            [제122회 3교시] 배관 내 수격현상(Water Hammer) 발생 시 충격파 전파 메커니즘을 설명하시오.
        </p>
    </article>
    """
    
    # 3. Replace article content
    q52_art.replace_with(BeautifulSoup(new_q52_html, "html.parser").article)
    print("Successfully replaced Q52 content inside soup.")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Successfully saved updated HTML to: {file_path}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = update_q52_article(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied updated HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
