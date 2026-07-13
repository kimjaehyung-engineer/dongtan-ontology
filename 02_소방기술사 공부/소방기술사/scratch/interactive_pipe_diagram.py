import os
import shutil
from bs4 import BeautifulSoup

def inject_interactive_diagram(file_path):
    print(f"Making pipe diagram interactive inside: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_interactive_diagram"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. Target card element
    card = soup.find(id="common_pipe_classification")
    if not card:
        print("Error: Could not find element with id='common_pipe_classification'")
        return False
        
    # 2. Re-compile the SVG with interactive class tags (<g class="pipe-node">)
    interactive_svg_html = r"""
    <svg id="pipeTreeSvg" viewBox="0 0 740 270" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background: var(--bg-secondary); border-radius: 12px; padding: 10px;">
        <defs>
            <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
                <feDropShadow dx="0" dy="1" stdDeviation="2" flood-opacity="0.04"/>
            </filter>
        </defs>

        <!-- Outer Border -->
        <rect width="720" height="250" x="10" y="10" rx="8" fill="none" stroke="var(--border)" stroke-width="1.5"/>
        
        <!-- ================= ROOT NODE ================= -->
        <g class="pipe-node" data-pipe="root" style="cursor: pointer;">
            <rect width="140" height="30" x="300" y="15" rx="5" fill="var(--accent)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
            <text x="370" y="34" text-anchor="middle" fill="#ffffff" font-family="'Noto Sans KR', sans-serif" font-weight="800" font-size="10.5">소방 배관 파이프</text>
        </g>
        
        <!-- Root to Level 1 Bridge -->
        <line x1="370" y1="45" x2="370" y2="52" stroke="var(--text-muted)" stroke-width="1.5"/>
        <line x1="72.5" y1="52" x2="672.5" y2="52" stroke="var(--text-muted)" stroke-width="1.5"/>
        
        <!-- ================= LEVEL 1 NODES (6 대분류) ================= -->
        <!-- 1. 강관 -->
        <line x1="72.5" y1="52" x2="72.5" y2="60" stroke="var(--text-muted)" stroke-width="1.5"/>
        <g class="pipe-node" data-pipe="steel" style="cursor: pointer;">
            <rect width="90" height="24" x="27.5" y="60" rx="4" fill="#ef4444" stroke="#dc2626" stroke-width="1" filter="url(#shadow)"/>
            <text x="72.5" y="75" text-anchor="middle" fill="#ffffff" font-family="'Noto Sans KR', sans-serif" font-weight="800" font-size="9">강관 (Steel)</text>
        </g>
        
        <!-- 2. 동관 -->
        <line x1="192.5" y1="52" x2="192.5" y2="60" stroke="var(--text-muted)" stroke-width="1.5"/>
        <g class="pipe-node" data-pipe="copper" style="cursor: pointer;">
            <rect width="90" height="24" x="147.5" y="60" rx="4" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
            <text x="192.5" y="75" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="9">동관 (Copper)</text>
        </g>
        
        <!-- 3. 주철관 -->
        <line x1="312.5" y1="52" x2="312.5" y2="60" stroke="var(--text-muted)" stroke-width="1.5"/>
        <g class="pipe-node" data-pipe="cast_iron" style="cursor: pointer;">
            <rect width="90" height="24" x="267.5" y="60" rx="4" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
            <text x="312.5" y="75" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="9">주철관 (Cast Iron)</text>
        </g>
        
        <!-- 4. 스테인리스관 -->
        <line x1="432.5" y1="52" x2="432.5" y2="60" stroke="var(--text-muted)" stroke-width="1.5"/>
        <g class="pipe-node" data-pipe="sts" style="cursor: pointer;">
            <rect width="90" height="24" x="387.5" y="60" rx="4" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
            <text x="432.5" y="75" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="9">스텐관 (STS)</text>
        </g>
        
        <!-- 5. 합성수지관 -->
        <line x1="552.5" y1="52" x2="552.5" y2="60" stroke="var(--text-muted)" stroke-width="1.5"/>
        <g class="pipe-node" data-pipe="plastic" style="cursor: pointer;">
            <rect width="90" height="24" x="507.5" y="60" rx="4" fill="#3b82f6" stroke="#2563eb" stroke-width="1" filter="url(#shadow)"/>
            <text x="552.5" y="75" text-anchor="middle" fill="#ffffff" font-family="'Noto Sans KR', sans-serif" font-weight="800" font-size="9">합성수지관</text>
        </g>
        
        <!-- 6. 시멘트관 -->
        <line x1="672.5" y1="52" x2="672.5" y2="60" stroke="var(--text-muted)" stroke-width="1.5"/>
        <g class="pipe-node" data-pipe="cement" style="cursor: pointer;">
            <rect width="90" height="24" x="627.5" y="60" rx="4" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
            <text x="672.5" y="75" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="9">시멘트관 (흄관)</text>
        </g>

        <!-- ================= LEFT: 강관 하부 분기 ================= -->
        <line x1="72.5" y1="84" x2="72.5" y2="96" stroke="var(--text-muted)" stroke-width="1.2"/>
        <line x1="45" y1="96" x2="205" y2="96" stroke="var(--text-muted)" stroke-width="1.2"/>
        
        <!-- 2단계 노드 1: 배관용 강관 -->
        <line x1="45" y1="96" x2="45" y2="105" stroke="var(--text-muted)" stroke-width="1.2"/>
        <g class="pipe-node" data-pipe="pipe_steel" style="cursor: pointer;">
            <rect width="60" height="20" x="15" y="105" rx="3" fill="#fee2e2" stroke="#ef4444" stroke-width="1" filter="url(#shadow)"/>
            <text x="45" y="118" text-anchor="middle" fill="#991b1b" font-family="'Noto Sans KR', sans-serif" font-weight="800" font-size="8">배관용강관</text>
        </g>
        
        <!-- 2단계 노드 2: 라이닝 강관 -->
        <line x1="125" y1="96" x2="125" y2="105" stroke="var(--text-muted)" stroke-width="1.2"/>
        <g class="pipe-node" data-pipe="lining" style="cursor: pointer;">
            <rect width="60" height="20" x="95" y="105" rx="3" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
            <text x="125" y="118" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="8">라이닝강관</text>
        </g>
        
        <!-- 2단계 노드 3: 기타 강관 -->
        <line x1="205" y1="96" x2="205" y2="105" stroke="var(--text-muted)" stroke-width="1.2"/>
        <g class="pipe-node" data-pipe="etc_steel" style="cursor: pointer;">
            <rect width="60" height="20" x="175" y="105" rx="3" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
            <text x="205" y="118" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="8">기타강관</text>
        </g>

        <!-- 3단계 (배관용강관 아래 수직 리스트) -->
        <line x1="45" y1="125" x2="45" y2="243" stroke="var(--text-muted)" stroke-width="1"/>
        
        <!-- 3.1 탄소강관 (SPP) -->
        <line x1="45" y1="147" x2="60" y2="147" stroke="var(--text-muted)" stroke-width="1"/>
        <g class="pipe-node" data-pipe="spp" style="cursor: pointer;">
            <rect width="85" height="18" x="60" y="138" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
            <text x="102.5" y="150" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="7.5">탄소강관 (SPP)</text>
        </g>
        
        <!-- 3.2 압력탄소 (SPPS) -->
        <line x1="45" y1="170" x2="60" y2="170" stroke="var(--text-muted)" stroke-width="1"/>
        <g class="pipe-node" data-pipe="spps" style="cursor: pointer;">
            <rect width="85" height="18" x="60" y="161" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
            <text x="102.5" y="173" text-anchor="middle" fill="#dc2626" font-family="'Inter', sans-serif" font-weight="800" font-size="7.5">압력탄소 (SPPS)</text>
        </g>
        
        <!-- 3.3 고압탄소 (SPPH) -->
        <line x1="45" y1="193" x2="60" y2="193" stroke="var(--text-muted)" stroke-width="1"/>
        <g class="pipe-node" data-pipe="spph" style="cursor: pointer;">
            <rect width="85" height="18" x="60" y="184" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
            <text x="102.5" y="196" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="7.5">고압탄소 (SPPH)</text>
        </g>
        
        <!-- 3.4 고온탄소 (SPHT) -->
        <line x1="45" y1="216" x2="60" y2="216" stroke="var(--text-muted)" stroke-width="1"/>
        <g class="pipe-node" data-pipe="spht" style="cursor: pointer;">
            <rect width="85" height="18" x="60" y="207" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
            <text x="102.5" y="219" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="7.5">고온탄소 (SPHT)</text>
        </g>

        <!-- 3.5 스텐강관 (STS) -->
        <line x1="45" y1="239" x2="60" y2="239" stroke="var(--text-muted)" stroke-width="1"/>
        <g class="pipe-node" data-pipe="ssc" style="cursor: pointer;">
            <rect width="85" height="18" x="60" y="230" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
            <text x="102.5" y="242" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="7.5">스텐강관 (STS)</text>
        </g>

        <!-- 3단계 (라이닝강관 아래 수직 리스트) -->
        <line x1="125" y1="125" x2="125" y2="170" stroke="var(--text-muted)" stroke-width="1"/>
        
        <!-- 3.2.1 모르타르 라이닝 -->
        <line x1="125" y1="147" x2="140" y2="147" stroke="var(--text-muted)" stroke-width="1"/>
        <g class="pipe-node" data-pipe="mortar" style="cursor: pointer;">
            <rect width="85" height="18" x="140" y="138" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
            <text x="182.5" y="150" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-size="7.2">모르타르 라이닝</text>
        </g>
        
        <!-- 3.2.2 합성수지 라이닝 -->
        <line x1="125" y1="170" x2="140" y2="170" stroke="var(--text-muted)" stroke-width="1"/>
        <g class="pipe-node" data-pipe="resin_lining" style="cursor: pointer;">
            <rect width="85" height="18" x="140" y="161" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
            <text x="182.5" y="173" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-size="7.2">합성수지 라이닝</text>
        </g>

        <!-- ================= RIGHT: 합성수지관 하부 분기 ================= -->
        <line x1="552.5" y1="84" x2="552.5" y2="200" stroke="var(--text-muted)" stroke-width="1.2"/>
        
        <!-- 5.1 CPVC (소방용) -->
        <line x1="552.5" y1="107" x2="570" y2="107" stroke="var(--text-muted)" stroke-width="1.2"/>
        <g class="pipe-node" data-pipe="cpvc" style="cursor: pointer;">
            <rect width="90" height="18" x="570" y="98" rx="2.5" fill="#dbeafe" stroke="#3b82f6" stroke-width="0.8"/>
            <text x="615" y="110" text-anchor="middle" fill="#1e40af" font-family="'Inter', sans-serif" font-weight="800" font-size="7.5">소방용 CPVC</text>
        </g>
        
        <!-- 5.2 PVC (일반/배수) -->
        <line x1="552.5" y1="130" x2="570" y2="130" stroke="var(--text-muted)" stroke-width="1.2"/>
        <g class="pipe-node" data-pipe="pvc" style="cursor: pointer;">
            <rect width="90" height="18" x="570" y="121" rx="2.5" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
            <text x="615" y="133" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="7.5">일반용 PVC</text>
        </g>
        
        <!-- 5.3 PE (지중매설) -->
        <line x1="552.5" y1="153" x2="570" y2="153" stroke="var(--text-muted)" stroke-width="1.2"/>
        <g class="pipe-node" data-pipe="pe" style="cursor: pointer;">
            <rect width="90" height="18" x="570" y="144" rx="2.5" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
            <text x="615" y="156" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="7.5">지중매설 PE</text>
        </g>
        
        <!-- 5.4 GRE (해수/고압) -->
        <line x1="552.5" y1="176" x2="570" y2="176" stroke="var(--text-muted)" stroke-width="1.2"/>
        <g class="pipe-node" data-pipe="gre" style="cursor: pointer;">
            <rect width="90" height="18" x="570" y="167" rx="2.5" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
            <text x="615" y="179" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="7.5">해수/고압 GRE</text>
        </g>
    </svg>
    """
    
    # Replace the old SVG with the new interactive SVG
    svgs = card.find_all("svg")
    if svgs:
        svgs[0].replace_with(BeautifulSoup(interactive_svg_html, "html.parser").svg)
        print("Replaced static SVG with interactive skeleton.")
        
    # 3. HTML for Detailed Info Panel and Event handling Javascript (Strictly no '**' symbols)
    info_panel_html = r"""
    <!-- 동적 상세 설명 패널 (인터랙티브 연동) -->
    <div id="pipe_detail_panel" style="background-color: var(--bg-secondary); border: 2px solid var(--accent); border-radius: 12px; padding: 22px; margin-top: 15px; margin-bottom: 25px; min-height: 120px; transition: all 0.25s ease; box-shadow: inset 0 2px 10px rgba(0,0,0,0.02);">
        <h5 id="pipe_detail_title" style="margin: 0 0 10px 0; font-size: 1.05rem; font-weight: 800; color: var(--accent); display: flex; align-items: center; gap: 8px;">
            🔍 선택 배관 상세 설계 스펙
        </h5>
        <div id="pipe_detail_desc" style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.75;">
            위 계통도 다이어그램에서 알고 싶은 배관 박스를 클릭해 보세요. 마스터 소방 기술 정보에 입각한 상세 규격, 한계 성능 및 설계 가이드가 이곳에 실시간 요약 표출됩니다.
        </div>
    </div>

    <!-- 인터랙티브 클릭 이벤트 가동 스크립트 -->
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        const pipeData = {
            "root": {
                "title": "소방 배관 파이프 (Root)",
                "desc": "소화약제를 가압송수장치(펌프) 또는 용기로부터 방수구까지 공급하는 핵심 이송 통로입니다. 설치 환경에 맞게 압력, 온도, 수격작용, 부식 한계 등의 엔지니어링 팩터를 검토하여 적합한 재질의 관을 설계 매핑해야 합니다."
            },
            "steel": {
                "title": "강관 (Steel Pipe)",
                "desc": "기계적 강도와 내압성, 내충격성이 매우 탁월하여 소방 압력 배관 계통에 널리 쓰이는 탄소강 재질의 배관입니다. 단, 산소와 물이 접촉하면 관 내벽에 녹(부식)이 발생하므로 방식 설계가 중요합니다."
            },
            "copper": {
                "title": "동관 (Copper Pipe • KS D 5301)",
                "desc": "연질 비철금속으로서 가공성 및 내식성이 대단히 우수하고 마찰 손실이 적습니다. 주로 스프링클러 헤드 하강용 신축 배관에 사용됩니다. 특유의 유연성 덕분에 좁고 복잡한 천장 내부 공간에서 곡관 가공이 자유롭습니다.<br><span style='color: var(--accent);'>※ 한계:</span> 탄산가스와 암모니아 환경에 취약하여 이산화탄소 소화설비 방출 배관으로는 사용할 수 없습니다."
            },
            "cast_iron": {
                "title": "주철관 (Cast Iron Pipe)",
                "desc": "두께가 매우 두껍고 외부 흙(토양) 및 부식성 인자에 잘 견디는 강력한 관재로, 옥외 지중 매립용 소화용수 주배관에 주로 쓰입니다.<br><span style='color: var(--accent);'>※ 한계:</span> 압축 강도는 크지만 때리는 기계적 충격에 잘 깨지는 성질(취성)이 있어 지상 노출부나 수격작용이 가해지는 가압 계통에는 사용하지 않습니다."
            },
            "sts": {
                "title": "배관용 스테인리스강관 (STS • KS D 3576 / 3595)",
                "desc": "크롬과 니켈 합금에 의해 부동태 피막을 반영구적으로 유지하므로 내식성이 일반 탄소강관 대비 1,600배 이상 뛰어납니다. 오랜 기간 물을 채워 대기해도 녹 찌꺼기(스케일)가 전혀 슬지 않아 스프링클러 노즐 막힘 사고를 완벽 차단합니다. 또한 인장강도가 철관의 2배에 달해 박막 규격(Sch 10) 시공으로 배관 계통 하중을 획기적으로 경량화합니다.<br><span style='color: var(--accent);'>※ 주의:</span> 타 금속 배관(동, 탄소강)과 직접 물리적 연결 시 전지식 전식(갈바닉) 부식이 일어나므로 반드시 절연 플랜지나 부속으로 절연 격리하여야 합니다."
            },
            "plastic": {
                "title": "합성수지관 (Plastic Pipe)",
                "desc": "부식 및 내부 스케일이 100% 발생하지 않고, 관 내벽 평활도가 매우 뛰어나 마찰손실계수가 C=150으로 극히 낮아 유속 흐름 성능이 우수합니다. 단, 열에 매우 약해 지상 노출 시공이 철저히 제한되며 지하 매설이나 불연 천장 내부 습식 한정 조건에서만 씁니다."
            },
            "cement": {
                "title": "시멘트관 (Cement Pipe / 흄관)",
                "desc": "콘크리트를 원심력으로 성형한 대형 관으로, 소방 배수용으로 씁니다. 내부 소화 펌프의 가압 고압은 버티지 못해 소화수 수송에는 쓰지 못하지만 지상의 도로 하중(차량 통행 등)을 찌그러짐 없이 견디는 압축 강도가 탁월하여 대용량의 소화 배수를 방출·유도하는 하수관거용으로 최적입니다."
            },
            "pipe_steel": {
                "title": "배관용 탄소강관 (Steel Pipe for Piping)",
                "desc": "유체를 직접 이송하는 목적으로 제작된 정밀 관재로 소방의 중추를 이룹니다. 사용 최고 압력 1.2 MPa 경계를 기준으로 적정 규격을 분기 설계합니다."
            },
            "lining": {
                "title": "라이닝 강관 (Lined Steel Pipe)",
                "desc": "금속 강관 내벽에 시멘트 모르타르나 에폭시, 폴리에틸렌 등 합성수지를 두껍게 코팅하여 강재의 기계적 튼튼함과 수지부의 방청성·저마찰 성능을 융합한 관재입니다. 주로 매설 용수로 쓰입니다.<br><span style='color: var(--accent);'>※ 주의:</span> 나사 가공이나 절단 부위 등 라이닝 피막이 손상된 틈새로 부식이 집중 침투하는 틈새 부식을 예방하기 위한 전용 접합 부속 시공이 요구됩니다."
            },
            "etc_steel": {
                "title": "기타 강관 (Structural/Special Steel Pipe)",
                "desc": "소화수 이송 목적 외에 비계 조립 및 배관 지지 등 외부 구조 부재용으로 가공된 구조용 강관 및 열교환용 튜브 계통 강관입니다."
            },
            "spp": {
                "title": "배관용 탄소강관 (SPP • KS D 3507)",
                "desc": "사용최고압력 1.2 MPa 미만의 가장 범용적인 일반 소화수 계통용 배관입니다. 아연 도금을 한 백관과 도금 없는 흑관으로 나뉘며, 사용 온도 한계는 350도 이하로 안전이 보장됩니다. (400도 장시간 초과 시 내강의 고용 탄소가 결정립계로 석출 및 분리되어 관이 깨집니다.) 조도계수는 습식 C=120, 준비작동식/건식은 C=100을 준용합니다."
            },
            "spps": {
                "title": "압력배관용 탄소강관 (SPPS • KS D 3562)",
                "desc": "사용최고압력 1.2 MPa 이상의 고압 구간(펌프 토출측 주배관, 고층부 입상 주배관)에 필수 설계되는 강관입니다. 무계목(Seamless) 또는 고성능 용접관 형태로 생산되며, 설계 압력에 맞추어 스케줄 번호(Sch 40, Sch 80 등)를 증가시켜 안전 성능을 만족시킵니다."
            },
            "spph": {
                "title": "고압배관용 탄소강관 (SPPH • KS D 3564)",
                "desc": "방출 압력이 10 MPa를 돌파하는 가스계 소화설비 용기 2차측 집합관(매니폴드) 등 극고압 가혹 조건에 설치되는 고인장 특화 강관입니다."
            },
            "spht": {
                "title": "고온배관용 탄소강관 (SPHT • KS D 3570)",
                "desc": "사용 온도가 350도를 초과하는 혹독한 열매체 이송 조건에서도 연성을 잃지 않도록 조성된 특수 고온 배관입니다."
            },
            "ssc": {
                "title": "배관용 스테인리스강관 (SSC / STS3576)",
                "desc": "크롬과 니켈 고합금 강재로 표면 부동태 피막을 형성하여 반영구적 무부식성이 검증된 수계 고강도 관재입니다. C=150의 최상의 조도를 보유합니다."
            },
            "mortar": {
                "title": "모르타르 라이닝 강관 (Mortar Lined Pipe)",
                "desc": "강관 내벽에 시멘트 모르타르 및 석탄산 타르를 도포하고 외벽에는 아스팔트 피막을 입힌 관으로, 옥외 지하 매설 용수관에 한하여 제한 시공합니다."
            },
            "resin_lining": {
                "title": "합성수지 라이닝 강관 (Resin Lined Pipe)",
                "desc": "강관 내/외벽 전체에 폴리에틸렌(PE) 또는 에폭시 분체를 코팅하여 강도와 완벽한 내부식성을 융합한 프리미엄 코팅 배관입니다."
            },
            "cpvc": {
                "title": "소방용 CPVC 배관 (KS M 3414)",
                "desc": "염소화 PVC 소재로 일반 플라스틱 대비 내열/내압성을 획기적으로 보강한 소방 전용 배관입니다. 한계산소지수 60% 이상으로 자기소화성을 가져 화재 시 쉽게 연소되지 않으며 조도가 C=150으로 아주 매끄러워 양정 손실이 극소입니다. 습식 소화 배관에 한정하며 불연 천장 안쪽에 은폐 매립하거나 직접 지하 매설 시에만 쓸 수 있습니다."
            },
            "pvc": {
                "title": "일반용 PVC 배관 (Polyvinyl Chloride)",
                "desc": "기계적 연성과 화열 안정 한계가 매우 취약하여 화재에 직접 닿으면 즉시 파열되므로, 소화배관으로는 절대 사용할 수 없으며 오직 펌프실 배수 드레인 관로용으로만 씁니다."
            },
            "pe": {
                "title": "지중매설 PE 배관 (Polyethylene Pipe • KS D 3607)",
                "desc": "유연성과 내충격성이 극대화되어 지반 변동 및 지진의 전단력을 흡수하며 영하 80도에서도 얼어 깨지지 않는 우수한 연질 수지배관입니다. 120~140도 사이에서 즉시 용융되므로 지상 노출부는 절대로 설치할 수 없고, 오직 옥외 지하 매설 소방 용수배관으로만 공인 설계됩니다."
            },
            "gre": {
                "title": "해수/고압 GRE 배관 (Glass-fiber Reinforced Epoxy)",
                "desc": "에폭시 수지 내부에 유리섬유 필라멘트를 와인딩 보강하여 금속 파이프 수준의 높은 한계 압력을 버티는 초경량 고강도 특수 합성수지관입니다. 바닷물에 전혀 부식되지 않아 화학 플랜트, 발전소의 해수 소방 배관 계통에 필수적으로 적용됩니다."
            }
        };

        const svg = document.getElementById("pipeTreeSvg");
        if (!svg) return;

        const nodes = svg.querySelectorAll(".pipe-node");
        const panel = document.getElementById("pipe_detail_panel");
        const titleEl = document.getElementById("pipe_detail_title");
        const descEl = document.getElementById("pipe_detail_desc");

        nodes.forEach(node => {
            node.addEventListener("click", function() {
                const pipeKey = this.getAttribute("data-pipe");
                const data = pipeData[pipeKey];

                if (!data) return;

                // 1. Reset all node strokes
                nodes.forEach(n => {
                    const rect = n.querySelector("rect");
                    if (rect) {
                        // Restore default color based on class/fill
                        rect.style.stroke = "var(--border)";
                        rect.style.strokeWidth = "1px";
                    }
                });

                // 2. Highlight clicked node
                const clickedRect = this.querySelector("rect");
                if (clickedRect) {
                    clickedRect.style.stroke = "var(--accent)";
                    clickedRect.style.strokeWidth = "2.5px";
                }

                // 3. Update Detail Panel with Fade effect
                panel.style.opacity = 0;
                panel.style.transform = "translateY(3px)";
                
                setTimeout(() => {
                    titleEl.innerHTML = "🔍 " + data.title;
                    descEl.innerHTML = data.desc;
                    panel.style.opacity = 1;
                    panel.style.transform = "translateY(0)";
                }, 120);
            });
        });
    });
    </script>
    """
    
    # 4. Insert detailed info panel and script right after the SVG
    svg_container = card.find("svg")
    if svg_container:
        svg_container.insert_after(BeautifulSoup(info_panel_html, "html.parser"))
        print("Successfully injected interactive panel and JavaScript after SVG.")
    else:
        print("Error: SVG container not found to append panel after")
        return False
        
    # 5. Save back
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Successfully saved updated HTML to: {file_path}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = inject_interactive_diagram(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied updated HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
