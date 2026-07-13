import os
import shutil
from bs4 import BeautifulSoup

def refactor_pipe_diagram(file_path):
    print(f"Refactoring pipe diagram in: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_pipe_diag_refactor"
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
        
    # 2. Find svg inside card
    svg = card.find("svg")
    if not svg:
        print("Error: Could not find svg inside common_pipe_classification")
        return False
        
    # 3. New Premium SVG with Vertical Branching Layout (No overlapping, perfectly aligned)
    new_svg_html = r"""
    <svg viewBox="0 0 740 440" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background: var(--bg-secondary); border-radius: 12px; padding: 15px;">
        <!-- Definitions for markers and filters -->
        <defs>
            <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
                <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.05"/>
            </filter>
        </defs>

        <!-- Outer Border -->
        <rect width="720" height="420" x="10" y="10" rx="8" fill="none" stroke="var(--border)" stroke-width="1.5"/>
        
        <!-- ================= ROOT NODE ================= -->
        <rect width="160" height="38" x="290" y="20" rx="6" fill="var(--accent)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
        <text x="370" y="44" text-anchor="middle" fill="#ffffff" font-family="'Noto Sans KR', sans-serif" font-weight="800" font-size="11.5">소방 배관 파이프</text>
        
        <!-- Root to Level 1 Bridge -->
        <line x1="370" y1="58" x2="370" y2="72" stroke="var(--text-muted)" stroke-width="1.5"/>
        <line x1="72" y1="72" x2="672" y2="72" stroke="var(--text-muted)" stroke-width="1.5"/>
        
        <!-- ================= LEVEL 1 NODES (6 대분류) ================= -->
        <!-- 1. 강관 -->
        <line x1="72" y1="72" x2="72" y2="85" stroke="var(--text-muted)" stroke-width="1.5"/>
        <rect width="95" height="30" x="25" y="85" rx="5" fill="#ef4444" stroke="#dc2626" stroke-width="1" filter="url(#shadow)"/>
        <text x="72.5" y="104" text-anchor="middle" fill="#ffffff" font-family="'Noto Sans KR', sans-serif" font-weight="800" font-size="9.5">강관 (Steel)</text>
        
        <!-- 2. 동관 -->
        <line x1="192.5" y1="72" x2="192.5" y2="85" stroke="var(--text-muted)" stroke-width="1.5"/>
        <rect width="95" height="30" x="145" y="85" rx="5" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
        <text x="192.5" y="104" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="9.5">동관 (Copper)</text>
        
        <!-- 3. 주철관 -->
        <line x1="312.5" y1="72" x2="312.5" y2="85" stroke="var(--text-muted)" stroke-width="1.5"/>
        <rect width="95" height="30" x="265" y="85" rx="5" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
        <text x="312.5" y="104" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="9.5">주철관 (Cast Iron)</text>
        
        <!-- 4. 스테인리스관 -->
        <line x1="432.5" y1="72" x2="432.5" y2="85" stroke="var(--text-muted)" stroke-width="1.5"/>
        <rect width="95" height="30" x="385" y="85" rx="5" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
        <text x="432.5" y="104" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="9.5">스텐관 (STS)</text>
        
        <!-- 5. 합성수지관 -->
        <line x1="552.5" y1="72" x2="552.5" y2="85" stroke="var(--text-muted)" stroke-width="1.5"/>
        <rect width="95" height="30" x="505" y="85" rx="5" fill="#3b82f6" stroke="#2563eb" stroke-width="1" filter="url(#shadow)"/>
        <text x="552.5" y="104" text-anchor="middle" fill="#ffffff" font-family="'Noto Sans KR', sans-serif" font-weight="800" font-size="9.5">합성수지관</text>
        
        <!-- 6. 시멘트관 -->
        <line x1="672.5" y1="72" x2="672.5" y2="85" stroke="var(--text-muted)" stroke-width="1.5"/>
        <rect width="95" height="30" x="625" y="85" rx="5" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
        <text x="672.5" y="104" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="9.5">시멘트관 (흄관)</text>

        <!-- ================= LEFT: 강관 하부 분기 (수직 전개형 트리) ================= -->
        <!-- 강관(72.5) 하단에서 2단계 분기선 -->
        <line x1="72.5" y1="115" x2="72.5" y2="132" stroke="var(--text-muted)" stroke-width="1.2"/>
        <line x1="45" y1="132" x2="205" y2="132" stroke="var(--text-muted)" stroke-width="1.2"/>
        
        <!-- 2단계 노드 1: 배관용 강관 -->
        <line x1="45" y1="132" x2="45" y2="145" stroke="var(--text-muted)" stroke-width="1.2"/>
        <rect width="65" height="24" x="12.5" y="145" rx="3" fill="#fee2e2" stroke="#ef4444" stroke-width="1" filter="url(#shadow)"/>
        <text x="45" y="160" text-anchor="middle" fill="#991b1b" font-family="'Noto Sans KR', sans-serif" font-weight="800" font-size="8.5">배관용강관</text>
        
        <!-- 2단계 노드 2: 라이닝 강관 -->
        <line x1="125" y1="132" x2="125" y2="145" stroke="var(--text-muted)" stroke-width="1.2"/>
        <rect width="65" height="24" x="92.5" y="145" rx="3" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
        <text x="125" y="160" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="8.5">라이닝강관</text>
        
        <!-- 2단계 노드 3: 기타 강관 -->
        <line x1="205" y1="132" x2="205" y2="145" stroke="var(--text-muted)" stroke-width="1.2"/>
        <rect width="65" height="24" x="172.5" y="145" rx="3" fill="var(--bg-primary)" stroke="var(--border)" stroke-width="1" filter="url(#shadow)"/>
        <text x="205" y="160" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-weight="700" font-size="8.5">기타강관</text>

        <!-- 3단계 (배관용강관 아래 수직 리스트) -->
        <line x1="45" y1="169" x2="45" y2="330" stroke="var(--text-muted)" stroke-width="1"/>
        
        <!-- 3.1 탄소강관 (SPP) -->
        <line x1="45" y1="195" x2="60" y2="195" stroke="var(--text-muted)" stroke-width="1"/>
        <rect width="90" height="22" x="60" y="184" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="1"/>
        <text x="105" y="198" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="8">탄소강관 (SPP)</text>
        
        <!-- 3.2 압력탄소 (SPPS) -->
        <line x1="45" y1="225" x2="60" y2="225" stroke="var(--text-muted)" stroke-width="1"/>
        <rect width="90" height="22" x="60" y="214" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="1"/>
        <text x="105" y="228" text-anchor="middle" fill="#dc2626" font-family="'Inter', sans-serif" font-weight="800" font-size="8">압력탄소 (SPPS)</text>
        
        <!-- 3.3 고압탄소 (SPPH) -->
        <line x1="45" y1="255" x2="60" y2="255" stroke="var(--text-muted)" stroke-width="1"/>
        <rect width="90" height="22" x="60" y="244" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="1"/>
        <text x="105" y="258" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="8">고압탄소 (SPPH)</text>
        
        <!-- 3.4 고온탄소 (SPHT) -->
        <line x1="45" y1="285" x2="60" y2="285" stroke="var(--text-muted)" stroke-width="1"/>
        <rect width="90" height="22" x="60" y="274" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="1"/>
        <text x="105" y="288" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="8">고온탄소 (SPHT)</text>

        <!-- 3.5 스텐강관 (STS) -->
        <line x1="45" y1="315" x2="60" y2="315" stroke="var(--text-muted)" stroke-width="1"/>
        <rect width="90" height="22" x="60" y="304" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="1"/>
        <text x="105" y="318" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="8">스텐강관 (STS)</text>

        <!-- 3단계 (라이닝강관 아래 수직 리스트) -->
        <line x1="125" y1="169" x2="125" y2="240" stroke="var(--text-muted)" stroke-width="1"/>
        
        <!-- 3.2.1 모르타르 라이닝 -->
        <line x1="125" y1="195" x2="140" y2="195" stroke="var(--text-muted)" stroke-width="1"/>
        <rect width="90" height="22" x="140" y="184" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="1"/>
        <text x="185" y="198" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-size="7.5">모르타르 라이닝</text>
        
        <!-- 3.2.2 합성수지 라이닝 -->
        <line x1="125" y1="225" x2="140" y2="225" stroke="var(--text-muted)" stroke-width="1"/>
        <rect width="90" height="22" x="140" y="214" rx="2" fill="#ffffff" stroke="var(--border)" stroke-width="1"/>
        <text x="185" y="228" text-anchor="middle" fill="var(--text-primary)" font-family="'Noto Sans KR', sans-serif" font-size="7.5">합성수지 라이닝</text>

        <!-- ================= RIGHT: 합성수지관 하부 분기 (수직 전개형 트리) ================= -->
        <line x1="552.5" y1="115" x2="552.5" y2="260" stroke="var(--text-muted)" stroke-width="1.2"/>
        
        <!-- 5.1 CPVC (소방용) -->
        <line x1="552.5" y1="145" x2="570" y2="145" stroke="var(--text-muted)" stroke-width="1.2"/>
        <rect width="95" height="22" x="570" y="134" rx="3" fill="#dbeafe" stroke="#3b82f6" stroke-width="1"/>
        <text x="617.5" y="148" text-anchor="middle" fill="#1e40af" font-family="'Inter', sans-serif" font-weight="800" font-size="8">소방용 CPVC</text>
        
        <!-- 5.2 PVC (일반/배수) -->
        <line x1="552.5" y1="175" x2="570" y2="175" stroke="var(--text-muted)" stroke-width="1.2"/>
        <rect width="95" height="22" x="570" y="164" rx="3" fill="#ffffff" stroke="var(--border)" stroke-width="1"/>
        <text x="617.5" y="178" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="8">일반용 PVC</text>
        
        <!-- 5.3 PE (지중매설) -->
        <line x1="552.5" y1="205" x2="570" y2="205" stroke="var(--text-muted)" stroke-width="1.2"/>
        <rect width="95" height="22" x="570" y="194" rx="3" fill="#ffffff" stroke="var(--border)" stroke-width="1"/>
        <text x="617.5" y="208" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="8">지중매설 PE</text>
        
        <!-- 5.4 GRE (해수/고압) -->
        <line x1="552.5" y1="235" x2="570" y2="235" stroke="var(--text-muted)" stroke-width="1.2"/>
        <rect width="95" height="22" x="570" y="224" rx="3" fill="#ffffff" stroke="var(--border)" stroke-width="1"/>
        <text x="617.5" y="238" text-anchor="middle" fill="var(--text-primary)" font-family="'Inter', sans-serif" font-weight="700" font-size="8">해수/고압 GRE</text>
    </svg>
    """
    
    # 4. Replace original svg with new structured svg
    svg.replace_with(BeautifulSoup(new_svg_html, "html.parser").svg)
    print("SVG successfully replaced inside BeautifulSoup DOM.")
    
    # 5. Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Successfully saved updated HTML to: {file_path}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = refactor_pipe_diagram(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied updated HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
