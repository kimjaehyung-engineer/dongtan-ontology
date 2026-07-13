import os
import shutil
from bs4 import BeautifulSoup

def compact_pipe_diagram(file_path):
    print(f"Compacting pipe classification diagram inside: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_compact_diagram"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. Find the target card
    card = soup.find(id="common_pipe_classification")
    if not card:
        print("Error: Could not find card element")
        return False
        
    # 2. Find the first svg (which is the tree diagram)
    svgs = card.find_all("svg")
    if not svgs:
        print("Error: No SVG found inside card")
        return False
        
    tree_svg = svgs[0]
    
    # 3. New Compact SVG HTML (viewBox="0 0 740 270" - extremely tight & clean, no '**' symbols)
    compact_svg_html = r"""
    <svg viewBox="0 0 740 270" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background: var(--bg-secondary); border-radius: 12px; padding: 10px;">
        <defs>
            <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
                <feDropShadow dx="0" dy="1" stdDeviation="2" flood-opacity="0.04"/>
            </filter>
        </defs>

        <!-- Outer Border -->
        <rect width="720" height="250" x="10" y="10" rx="8" fill="none" stroke="var(--border)" stroke-width="1.5"/>
        
        <!-- ================= ROOT NODE ================= -->
        <rect width="140" height="30" x="300" y="15" rx="5" fill="var(--accent)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
        <text x="370" y="34" text-anchor="middle" fill="#ffffff" font-family="'Noto Sans KR', sans-serif" font-weight="800" font-size="10.5">소방 배관 파이프</text>
        
        <!-- Root to Level 1 Bridge -->
        <line x1="370" y1="45" x2="370" y2="52" stroke="var(--text-muted)" stroke-width="1.5"/>
        <line x1="72.5" y1="52" x2="672.5" y2="52" stroke="var(--text-muted)" stroke-width="1.5"/>
        
        <!-- ================= LEVEL 1 NODES (6 대분류) ================= -->
        <!-- 1. 강관 -->
        <line x1="72.5" y1="52" x2="72.5" y2="60" stroke="var(--text-muted)" stroke-width="1.5"/>
        <rect width="90" height="24" x="27.5" y="60" rx="4" fill="#ef4444" stroke="#dc2626" stroke-width="1" filter="url(#shadow)"/>
        <text x="72.5" y="75" text-anchor="middle" fill="#ffffff" font-family="'Noto Sans KR', sans-serif" font-weight="800" font-size="9">강관 (Steel)</text>
        
        <!-- 2. 동관 -->
        <line x1="192.5" y1="52" x2="192.5" y2="60" stroke="var(--text-muted)" stroke-width="1.5"/>
        <rect width="90" height="24" x="147.5" y="60" rx="4" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
        <text x="192.5" y="75" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="9">동관 (Copper)</text>
        
        <!-- 3. 주철관 -->
        <line x1="312.5" y1="52" x2="312.5" y2="60" stroke="var(--text-muted)" stroke-width="1.5"/>
        <rect width="90" height="24" x="267.5" y="60" rx="4" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
        <text x="312.5" y="75" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="9">주철관 (Cast Iron)</text>
        
        <!-- 4. 스테인리스관 -->
        <line x1="432.5" y1="52" x2="432.5" y2="60" stroke="var(--text-muted)" stroke-width="1.5"/>
        <rect width="90" height="24" x="387.5" y="60" rx="4" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
        <text x="432.5" y="75" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="9">스텐관 (STS)</text>
        
        <!-- 5. 합성수지관 -->
        <line x1="552.5" y1="52" x2="552.5" y2="60" stroke="var(--text-muted)" stroke-width="1.5"/>
        <rect width="90" height="24" x="507.5" y="60" rx="4" fill="#3b82f6" stroke="#2563eb" stroke-width="1" filter="url(#shadow)"/>
        <text x="552.5" y="75" text-anchor="middle" fill="#ffffff" font-family="'Noto Sans KR', sans-serif" font-weight="800" font-size="9">합성수지관</text>
        
        <!-- 6. 시멘트관 -->
        <line x1="672.5" y1="52" x2="672.5" y2="60" stroke="var(--text-muted)" stroke-width="1.5"/>
        <rect width="90" height="24" x="627.5" y="60" rx="4" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
        <text x="672.5" y="75" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="9">시멘트관 (흄관)</text>

        <!-- ================= LEFT: 강관 하부 분기 (초타이트 수직 트리) ================= -->
        <!-- 강관(72.5) 하단에서 2단계 분기선 -->
        <line x1="72.5" y1="84" x2="72.5" y2="96" stroke="var(--text-muted)" stroke-width="1.2"/>
        <line x1="45" y1="96" x2="205" y2="96" stroke="var(--text-muted)" stroke-width="1.2"/>
        
        <!-- 2단계 노드 1: 배관용 강관 -->
        <line x1="45" y1="96" x2="45" y2="105" stroke="var(--text-muted)" stroke-width="1.2"/>
        <rect width="60" height="20" x="15" y="105" rx="3" fill="#fee2e2" stroke="#ef4444" stroke-width="1" filter="url(#shadow)"/>
        <text x="45" y="118" text-anchor="middle" fill="#991b1b" font-family="'Noto Sans KR', sans-serif" font-weight="800" font-size="8">배관용강관</text>
        
        <!-- 2단계 노드 2: 라이닝 강관 -->
        <line x1="125" y1="96" x2="125" y2="105" stroke="var(--text-muted)" stroke-width="1.2"/>
        <rect width="60" height="20" x="95" y="105" rx="3" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
        <text x="125" y="118" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="8">라이닝강관</text>
        
        <!-- 2단계 노드 3: 기타 강관 -->
        <line x1="205" y1="96" x2="205" y2="105" stroke="var(--text-muted)" stroke-width="1.2"/>
        <rect width="60" height="20" x="175" y="105" rx="3" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
        <text x="205" y="118" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="8">기타강관</text>

        <!-- 3단계 (배관용강관 아래 수직 리스트 - y축 갭 23px로 타이트화) -->
        <line x1="45" y1="125" x2="45" y2="243" stroke="var(--text-muted)" stroke-width="1"/>
        
        <!-- 3.1 탄소강관 (SPP) -->
        <line x1="45" y1="147" x2="60" y2="147" stroke="var(--text-muted)" stroke-width="1"/>
        <rect width="85" height="18" x="60" y="138" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
        <text x="102.5" y="150" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="7.5">탄소강관 (SPP)</text>
        
        <!-- 3.2 압력탄소 (SPPS) -->
        <line x1="45" y1="170" x2="60" y2="170" stroke="var(--text-muted)" stroke-width="1"/>
        <rect width="85" height="18" x="60" y="161" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
        <text x="102.5" y="173" text-anchor="middle" fill="#dc2626" font-family="'Inter', sans-serif" font-weight="800" font-size="7.5">압력탄소 (SPPS)</text>
        
        <!-- 3.3 고압탄소 (SPPH) -->
        <line x1="45" y1="193" x2="60" y2="193" stroke="var(--text-muted)" stroke-width="1"/>
        <rect width="85" height="18" x="60" y="184" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
        <text x="102.5" y="196" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="7.5">고압탄소 (SPPH)</text>
        
        <!-- 3.4 고온탄소 (SPHT) -->
        <line x1="45" y1="216" x2="60" y2="216" stroke="var(--text-muted)" stroke-width="1"/>
        <rect width="85" height="18" x="60" y="207" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
        <text x="102.5" y="219" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="7.5">고온탄소 (SPHT)</text>

        <!-- 3.5 스텐강관 (STS) -->
        <line x1="45" y1="239" x2="60" y2="239" stroke="var(--text-muted)" stroke-width="1"/>
        <rect width="85" height="18" x="60" y="230" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
        <text x="102.5" y="242" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="7.5">스텐강관 (STS)</text>

        <!-- 3단계 (라이닝강관 아래 수직 리스트 - y축 갭 23px) -->
        <line x1="125" y1="125" x2="125" y2="170" stroke="var(--text-muted)" stroke-width="1"/>
        
        <!-- 3.2.1 모르타르 라이닝 -->
        <line x1="125" y1="147" x2="140" y2="147" stroke="var(--text-muted)" stroke-width="1"/>
        <rect width="85" height="18" x="140" y="138" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
        <text x="182.5" y="150" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-size="7.2">모르타르 라이닝</text>
        
        <!-- 3.2.2 합성수지 라이닝 -->
        <line x1="125" y1="170" x2="140" y2="170" stroke="var(--text-muted)" stroke-width="1"/>
        <rect width="85" height="18" x="140" y="161" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
        <text x="182.5" y="173" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-size="7.2">합성수지 라이닝</text>

        <!-- ================= RIGHT: 합성수지관 하부 분기 (초타이트 수직 리스트) ================= -->
        <line x1="552.5" y1="84" x2="552.5" y2="200" stroke="var(--text-muted)" stroke-width="1.2"/>
        
        <!-- 5.1 CPVC (소방용) -->
        <line x1="552.5" y1="107" x2="570" y2="107" stroke="var(--text-muted)" stroke-width="1.2"/>
        <rect width="90" height="18" x="570" y="98" rx="2.5" fill="#dbeafe" stroke="#3b82f6" stroke-width="0.8"/>
        <text x="615" y="110" text-anchor="middle" fill="#1e40af" font-family="'Inter', sans-serif" font-weight="800" font-size="7.5">소방용 CPVC</text>
        
        <!-- 5.2 PVC (일반/배수) -->
        <line x1="552.5" y1="130" x2="570" y2="130" stroke="var(--text-muted)" stroke-width="1.2"/>
        <rect width="90" height="18" x="570" y="121" rx="2.5" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
        <text x="615" y="133" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="7.5">일반용 PVC</text>
        
        <!-- 5.3 PE (지중매설) -->
        <line x1="552.5" y1="153" x2="570" y2="153" stroke="var(--text-muted)" stroke-width="1.2"/>
        <rect width="90" height="18" x="570" y="144" rx="2.5" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
        <text x="615" y="156" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="7.5">지중매설 PE</text>
        
        <!-- 5.4 GRE (해수/고압) -->
        <line x1="552.5" y1="176" x2="570" y2="176" stroke="var(--text-muted)" stroke-width="1.2"/>
        <rect width="90" height="18" x="570" y="167" rx="2.5" fill="#ffffff" stroke="var(--border)" stroke-width="0.8"/>
        <text x="615" y="179" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="7.5">해수/고압 GRE</text>
    </svg>
    """
    
    # 4. Replace tree_svg
    tree_svg.replace_with(BeautifulSoup(compact_svg_html, "html.parser").svg)
    print("Tree SVG successfully replaced with compact version inside DOM.")
    
    # 5. Save back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Successfully saved updated HTML to: {file_path}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = compact_pipe_diagram(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied updated HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
