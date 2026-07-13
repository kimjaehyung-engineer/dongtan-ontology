import os
import shutil
from bs4 import BeautifulSoup

def inject_pipe_classification(file_path):
    print(f"Injecting Common Pipe Classification Card into: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_pipe_class"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. CSS helper styles for common card
    style_tag = soup.find("style")
    if style_tag:
        common_card_css = """
        /* Common Learning Info Card Style */
        .common-info-card {
            background-color: var(--bg-primary);
            border: 2px solid var(--accent);
            border-radius: 16px;
            padding: 30px;
            margin-top: 40px;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(var(--accent-rgb), 0.05);
            position: relative;
        }
        .common-info-card::before {
            content: "💡 공통 필수 학습 지식";
            position: absolute;
            top: -15px;
            left: 30px;
            background-color: var(--accent);
            color: white;
            font-size: 0.85rem;
            font-weight: 800;
            padding: 4px 16px;
            border-radius: 30px;
            box-shadow: 0 4px 10px rgba(var(--accent-rgb), 0.2);
        }
        """
        style_tag.append(common_card_css)
        print("CSS styles for common info card injected.")

    # 2. Structure the HTML of the Pipe Classification
    pipe_html = r"""
    <div class="common-info-card" id="common_pipe_classification">
        <div class="category-path-container" style="margin-top: 10px;">
            <span class="category-path">배관재료 &gt; 공통 필수 기초</span>
            <span class="category-badge" style="background-color: var(--accent); color: white;">배관 공통</span>
        </div>
        <h2 style="font-size: 1.6rem; font-weight: 800; color: var(--text-primary); margin-top: 15px; margin-bottom: 25px; border-bottom: 2px dashed var(--border); padding-bottom: 12px;">
            [공통학습] 소방 배관(파이프)의 재질별·용도별 전방위 종합 분류 체계
        </h2>
        
        <p class="desc" style="font-size: 0.95rem; line-height: 1.7; color: var(--text-secondary); margin-bottom: 25px;">
            수계 및 가스계 소화설비에 사용되는 소화 배관(파이프)은 사용 압력, 온도, 부식성 환경, 기하학적 시공 조건에 따라 다양한 재질로 분기된다. 배관재료 본문 학습에 앞서, 소방 배관의 대분류(6대 재질), 강관의 중분류(3대 분류), 배관용 강관의 소분류 및 합성수지관의 4대 분류 체계를 유기적 계통도로 정립한다.
        </p>

        <!-- SVG Tree Diagram (파이프 분류 체계 계통도) -->
        <div class="zoomable-media" data-title="소방 파이프 종합 분류 계통도">
            <svg viewBox="0 0 740 420" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background: var(--bg-secondary); border-radius: 12px; padding: 15px;">
                <!-- Outer Border -->
                <rect width="720" height="400" x="10" y="10" rx="8" fill="none" stroke="var(--border)" stroke-width="1.5"/>
                
                <!-- Root: 소방 파이프 (Root Node) -->
                <rect width="140" height="35" x="290" y="25" rx="5" fill="var(--accent)" stroke="var(--border)"/>
                <text x="360" y="47" text-anchor="middle" fill="#ffffff" font-weight="bold" font-size="11">소방 배관 파이프</text>
                
                <!-- Level 1 Connections -->
                <path d="M 360 60 L 360 90" stroke="var(--text-secondary)" stroke-width="1.5" fill="none"/>
                <path d="M 80 90 L 640 90" stroke="var(--text-secondary)" stroke-width="1.5" fill="none"/>
                
                <!-- Connectors to L1 Nodes -->
                <line x1="80" y1="90" x2="80" y2="110" stroke="var(--text-secondary)" stroke-width="1.5"/>
                <line x1="190" y1="90" x2="190" y2="110" stroke="var(--text-secondary)" stroke-width="1.5"/>
                <line x1="300" y1="90" x2="300" y2="110" stroke="var(--text-secondary)" stroke-width="1.5"/>
                <line x1="410" y1="90" x2="410" y2="110" stroke="var(--text-secondary)" stroke-width="1.5"/>
                <line x1="530" y1="90" x2="530" y2="110" stroke="var(--text-secondary)" stroke-width="1.5"/>
                <line x1="640" y1="90" x2="640" y2="110" stroke="var(--text-secondary)" stroke-width="1.5"/>
                
                <!-- Level 1 Nodes (6대 대분류) -->
                <!-- 1. 강관 -->
                <rect width="90" height="28" x="35" y="110" rx="4" fill="#ef4444" stroke="var(--border)"/>
                <text x="80" y="127" text-anchor="middle" fill="#ffffff" font-weight="bold" font-size="9">강관 (Steel)</text>
                
                <!-- 2. 동관 -->
                <rect width="90" height="28" x="145" y="110" rx="4" fill="var(--bg-primary)" stroke="var(--border)"/>
                <text x="190" y="127" text-anchor="middle" fill="var(--text-primary)" font-size="9">동관 (Copper)</text>
                
                <!-- 3. 주철관 -->
                <rect width="90" height="28" x="255" y="110" rx="4" fill="var(--bg-primary)" stroke="var(--border)"/>
                <text x="300" y="127" text-anchor="middle" fill="var(--text-primary)" font-size="9">주철관 (Cast Iron)</text>
                
                <!-- 4. 스테인리스관 -->
                <rect width="90" height="28" x="365" y="110" rx="4" fill="var(--bg-primary)" stroke="var(--border)"/>
                <text x="410" y="127" text-anchor="middle" fill="var(--text-primary)" font-size="9">스텐관 (STS)</text>
                
                <!-- 5. 합성수지관 -->
                <rect width="90" height="28" x="485" y="110" rx="4" fill="#3b82f6" stroke="var(--border)"/>
                <text x="530" y="127" text-anchor="middle" fill="#ffffff" font-weight="bold" font-size="9">합성수지관</text>
                
                <!-- 6. 시멘트관 -->
                <rect width="90" height="28" x="595" y="110" rx="4" fill="var(--bg-primary)" stroke="var(--border)"/>
                <text x="640" y="127" text-anchor="middle" fill="var(--text-primary)" font-size="9">시멘트관 (흄관)</text>
                
                <!-- Level 2: 강관 분기 (3대 분류) -->
                <path d="M 80 138 L 80 165" stroke="var(--text-secondary)" stroke-width="1.2" fill="none"/>
                <path d="M 30 165 L 140 165" stroke="var(--text-secondary)" stroke-width="1.2" fill="none"/>
                <line x1="30" y1="165" x2="30" y2="185" stroke="var(--text-secondary)" stroke-width="1.2"/>
                <line x1="85" y1="165" x2="85" y2="185" stroke="var(--text-secondary)" stroke-width="1.2"/>
                <line x1="140" y1="165" x2="140" y2="185" stroke="var(--text-secondary)" stroke-width="1.2"/>
                
                <!-- L2 Nodes under 강관 -->
                <rect width="50" height="22" x="5" y="185" rx="3" fill="#fee2e2" stroke="#ef4444"/>
                <text x="30" y="199" text-anchor="middle" fill="#991b1b" font-weight="bold" font-size="7.5">배관용강관</text>
                
                <rect width="50" height="22" x="60" y="185" rx="3" fill="#f1f5f9" stroke="var(--border)"/>
                <text x="85" y="199" text-anchor="middle" fill="var(--text-primary)" font-size="7.5">라이닝강관</text>
                
                <rect width="50" height="22" x="115" y="185" rx="3" fill="#f1f5f9" stroke="var(--border)"/>
                <text x="140" y="199" text-anchor="middle" fill="var(--text-primary)" font-size="7.5">기타강관</text>
                
                <!-- Level 3: 배관용강관 분기 (소분류) -->
                <path d="M 30 207 L 30 230" stroke="var(--text-secondary)" stroke-width="1" fill="none"/>
                <path d="M 30 230 L 150 230" stroke="var(--text-secondary)" stroke-width="1" fill="none"/>
                <line x1="30" y1="230" x2="30" y2="245" stroke="var(--text-secondary)" stroke-width="1"/>
                <line x1="70" y1="230" x2="70" y2="245" stroke="var(--text-secondary)" stroke-width="1"/>
                <line x1="110" y1="230" x2="110" y2="245" stroke="var(--text-secondary)" stroke-width="1"/>
                <line x1="150" y1="230" x2="150" y2="245" stroke="var(--text-secondary)" stroke-width="1"/>
                
                <rect width="36" height="40" x="12" y="245" rx="2" fill="#fff" stroke="var(--border)"/>
                <text x="30" y="258" text-anchor="middle" fill="var(--text-primary)" font-size="6.5">탄소</text>
                <text x="30" y="270" text-anchor="middle" fill="var(--text-primary)" font-size="6.5">강관</text>
                <text x="30" y="281" text-anchor="middle" fill="#ef4444" font-weight="bold" font-size="6.5">(SPP)</text>
                
                <rect width="36" height="40" x="52" y="245" rx="2" fill="#fff" stroke="var(--border)"/>
                <text x="70" y="258" text-anchor="middle" fill="var(--text-primary)" font-size="6.5">압력</text>
                <text x="70" y="270" text-anchor="middle" fill="var(--text-primary)" font-size="6.5">탄소</text>
                <text x="70" y="281" text-anchor="middle" fill="#ef4444" font-weight="bold" font-size="6.5">(SPPS)</text>
                
                <rect width="36" height="40" x="92" y="245" rx="2" fill="#fff" stroke="var(--border)"/>
                <text x="110" y="258" text-anchor="middle" fill="var(--text-primary)" font-size="6.5">고압</text>
                <text x="110" y="270" text-anchor="middle" fill="var(--text-primary)" font-size="6.5">탄소</text>
                <text x="110" y="281" text-anchor="middle" fill="#ef4444" font-weight="bold" font-size="6.5">(SPPH)</text>
                
                <rect width="36" height="40" x="132" y="245" rx="2" fill="#fff" stroke="var(--border)"/>
                <text x="150" y="258" text-anchor="middle" fill="var(--text-primary)" font-size="6.5">고온</text>
                <text x="150" y="270" text-anchor="middle" fill="var(--text-primary)" font-size="6.5">탄소</text>
                <text x="150" y="281" text-anchor="middle" fill="#ef4444" font-weight="bold" font-size="6.5">(SPHT)</text>
                
                <!-- L2: 라이닝강관 분기 -->
                <path d="M 85 207 L 85 220" stroke="var(--text-secondary)" stroke-width="1" fill="none"/>
                <path d="M 85 220 L 115 220" stroke="var(--text-secondary)" stroke-width="1" fill="none"/>
                <line x1="85" y1="220" x2="85" y2="295" stroke="var(--text-secondary)" stroke-width="1"/>
                <line x1="115" y1="220" x2="115" y2="295" stroke="var(--text-secondary)" stroke-width="1"/>
                
                <text x="85" y="315" text-anchor="middle" fill="var(--text-secondary)" font-size="6" font-weight="bold">모르타르</text>
                <text x="115" y="315" text-anchor="middle" fill="var(--text-secondary)" font-size="6" font-weight="bold">수지코팅</text>
                
                <!-- Level 2: 합성수지관 분기 (4대 분류) -->
                <path d="M 530 138 L 530 185" stroke="var(--text-secondary)" stroke-width="1.2" fill="none"/>
                <path d="M 470 185 L 590 185" stroke="var(--text-secondary)" stroke-width="1.2" fill="none"/>
                <line x1="470" y1="185" x2="470" y2="210" stroke="var(--text-secondary)" stroke-width="1.2"/>
                <line x1="510" y1="185" x2="510" y2="210" stroke="var(--text-secondary)" stroke-width="1.2"/>
                <line x1="550" y1="185" x2="550" y2="210" stroke="var(--text-secondary)" stroke-width="1.2"/>
                <line x1="590" y1="185" x2="590" y2="210" stroke="var(--text-secondary)" stroke-width="1.2"/>
                
                <!-- L2 Nodes under 합성수지관 -->
                <rect width="36" height="24" x="452" y="210" rx="3" fill="#dbeafe" stroke="#3b82f6"/>
                <text x="470" y="225" text-anchor="middle" fill="#1e40af" font-weight="bold" font-size="8">CPVC</text>
                
                <rect width="36" height="24" x="492" y="210" rx="3" fill="#f1f5f9" stroke="var(--border)"/>
                <text x="510" y="225" text-anchor="middle" fill="var(--text-primary)" font-size="8">PVC</text>
                
                <rect width="36" height="24" x="532" y="210" rx="3" fill="#f1f5f9" stroke="var(--border)"/>
                <text x="550" y="225" text-anchor="middle" fill="var(--text-primary)" font-size="8">PE</text>
                
                <rect width="36" height="24" x="572" y="210" rx="3" fill="#f1f5f9" stroke="var(--border)"/>
                <text x="590" y="225" text-anchor="middle" fill="var(--text-primary)" font-size="8">GRE</text>
            </svg>
            <div class="diagram-explanation">
                <strong>모식도 설명:</strong> 소방 파이프의 대분류(6대 재질), 강관의 3대 구분 및 배관용 탄소강관 4종 시리즈(SPP, SPPS, SPPH, SPHT), 그리고 합성수지관의 4대 핵심 재질(CPVC, PVC, PE, GRE)을 유기적으로 연계한 전방위 분류 계통도입니다.
            </div>
        </div>

        <h3>1. 소방 배관 파이프의 재질별 대분류 (6대 분류)</h3>
        <table class="comparison-table">
            <thead>
                <tr>
                    <th>분류</th>
                    <th>주요 특성 및 물리적 강도</th>
                    <th>소방 공학적 실무 적용처</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>강관<br>(Steel)</strong></td>
                    <td>높은 인장 강도와 내압성, 내충격성을 지녀 수압 및 기계적 외력이 가해지는 배관에 최적. 단, 습식 상태에서 부식 발생 가능.</td>
                    <td>수계소화설비(스프링클러, 소화전) 지상부 배관, 가스계 고압 배관, 감압 배관 등 소방의 **메인 중추 배관**.</td>
                </tr>
                <tr>
                    <td><strong>동관<br>(Copper)</strong></td>
                    <td>내식성과 열전도율이 우수하며 마찰 손실이 적음. 가공성이 좋으나 강관 대비 기계적 충격에 약함.</td>
                    <td>스프링클러설비 신축배관, 냉난방 겸용 배관, 소형 가압 급수용 관로.</td>
                </tr>
                <tr>
                    <td><strong>주철관<br>(Cast Iron)</strong></td>
                    <td>내식성과 내구성이 뛰어나 부식성 환경에 강하나, 취성(약한 충격에 깨짐)이 있음.</td>
                    <td>**옥외 지중 매립용 소화용수 주배관**, 배수관.</td>
                </tr>
                <tr>
                    <td><strong>스테인리스관<br>(STS)</strong></td>
                    <td>크롬(Cr) 피막 형성으로 내부식성이 반영구적이며, 배관 두께를 얇게(박막화) 설계할 수 있어 경량화 가능.</td>
                    <td>수계소화설비 입상배관 및 수조 흡입측 배관, **배관용 스테인리스강관(SSC/SPSU)**.</td>
                </tr>
                <tr>
                    <td><strong>합성수지관<br>(Plastic)</strong></td>
                    <td>부식이 전혀 없고 마찰손실계수(C=150)가 극히 낮아 에너지 효율이 좋으나, 고열에 취약함.</td>
                    <td>**소방용 CPVC 배관** (지하 매설 및 노출 시 천장 은폐부 시공), 지중 소수관.</td>
                </tr>
                <tr>
                    <td><strong>시멘트관<br>(Cement)</strong></td>
                    <td>콘크리트를 원심력으로 성형한 흄관 등. 내압력은 약함.</td>
                    <td>소화 배수용 대형 하수관거 및 대형 유수 유입부.</td>
                </tr>
            </tbody>
        </table>

        <h3>2. 강관의 용도별 중분류 (3대 분류)</h3>
        <ul>
            <li><strong>배관용 강관</strong>: 유체를 직접 이송하는 목적으로 제조된 정밀 강관.
                - **배관용 탄소강관 (SPP)**: 사용압력 $1.2\,\text{MPa}$ 이하의 일반 소화수 이송용.
                - **압력배관용 탄소강관 (SPPS)**: 사용압력 $1.2\,\text{MPa}$ 초과의 가압송수 토출측 및 고압 수계 배관.
                - **고압배관용 탄소강관 (SPPH)**: 압력 $10\,\text{MPa}$ 이상 급의 극고압 이송 (가스계 소화설비 저장용기 직후 집합관 등).
                - **고온배관용 탄소강관 (SPHT)**: $350^\circ\text{C}$ 이상의 고온 열매체 수송용.
                - **배관용 스테인리스강관 (SSC / SPSU)**: 내부식성이 우수한 프리미엄 수계 배관.
            </li>
            <li><strong>라이닝 강관</strong>: 금속 강관 내벽에 보호 피막을 코팅하여 부식을 원천 차단하고 수리 흐름을 개선한 하이브리드 배관.
                - **모르타르 라이닝 강관**: 내벽에 시멘트 모르타르를 원심 도포하여 지하 매설 용수로 사용.
                - **합성수지 라이닝 강관 (PE/에폭시 코팅)**: 소방배관 내벽 부식(스케일) 방지 및 마찰 손실 저감을 위한 코팅 강관.
            </li>
            <li><strong>기타 강관</strong>: 구조용 탄소강관(SCT, 비계 및 기둥 지지용), 보일러 및 열교환기용 강관 등 소화수 이송 외의 특수 목적용 강관.</li>
        </ul>

        <h3>3. 합성수지관의 분류 및 소방 특징 (4대 분류)</h3>
        <ul>
            <li><strong>CPVC (Chlorinated Polyvinyl Chloride, 소방용 합성수지관)</strong>:
                - 염소화 PVC 수지로서 일반 PVC 대비 내열성, 내압 성능을 비약적으로 보강한 소방 전용 배관.
                - 소방청 화재안전성능기준에서 정한 **은폐 설치 장소** 및 스프링클러 설비 배관용으로 사용 승인.
            </li>
            <li><strong>PVC (Polyvinyl Chloride, 일반 염화비닐관)</strong>:
                - 기계적 강도와 내열성이 약하여 소화 배관으로는 사용 불가하며, 소방 펌프실 배수 드레인이나 환기 계통 배수관에 국한.
            </li>
            <li><strong>PE (Polyethylene, 폴리에틸렌관)</strong>:
                - 신축성과 내충격성, 동파 복원력이 우수하여 **옥외 지중 매립용 소방용수 주배관**으로 널리 시공.
            </li>
            <li><strong>GRE (Glass-fiber Reinforced Epoxy, 유리섬유 강화 에폭시관)</strong>:
                - 유리섬유로 보강하여 초고압 성능과 반영구적 내식성을 지닌 특수 관재.
                - 부식성이 극심한 **해수 소화 배관망**이나 화학 플랜트, 발전소 소방 배관에 제한적 채택.
            </li>
        </ul>
    </div>
    """
    
    # 3. Insert before q37
    q37_art = soup.find("article", id="q37")
    if q37_art:
        soup_pipe = BeautifulSoup(pipe_html, "html.parser").div
        q37_art.insert_before(soup_pipe)
        print("Successfully injected common pipe classification card before Q37.")
    else:
        print("Error: Could not find article with id='q37' to insert before.")
        return False
        
    # 4. Insert link in sidebar under Ch 6 (id="ch-content-6")
    ch6_ul = soup.find("ul", id="ch-content-6")
    if ch6_ul:
        li_common = soup.new_tag("li", attrs={"class": "nav-item"})
        a_common = soup.new_tag("a", href="#common_pipe_classification", attrs={"class": "nav-link"})
        s_num = soup.new_tag("span", attrs={"class": "nav-num"}, style="background-color: var(--accent); color: white; border-radius: 4px; padding: 2px 6px;")
        s_num.string = "공통지식"
        s_title = soup.new_tag("span")
        s_title.string = "소방 배관 파이프의 재질·용도별 종합 분류 체계"
        
        a_common.append(s_num)
        a_common.append(s_title)
        li_common.append(a_common)
        
        # Insert as first child of the sidebar ul to put it at the beginning of Ch 6
        ch6_ul.insert(0, li_common)
        print("Successfully inserted common linker into Ch 6 sidebar accordion.")
    else:
        print("Error: Could not find ul with id='ch-content-6' in sidebar.")
        return False
        
    # 5. Save back
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Successfully saved injected HTML to: {file_path}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = inject_pipe_classification(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied updated HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
