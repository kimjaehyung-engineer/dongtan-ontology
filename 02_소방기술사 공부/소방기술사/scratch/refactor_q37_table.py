import os
import shutil
from bs4 import BeautifulSoup

def refactor_q37_table(file_path):
    print(f"Refactoring Q37 table in: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_q37_table"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. Find article with id="q37"
    q37_art = soup.find("article", id="q37")
    if not q37_art:
        print("Error: Could not find article with id='q37'")
        return False
        
    # 2. Find table within q37
    target_table = q37_art.find("table")
    if not target_table:
        print("Error: Could not find table inside Q37")
        return False
        
    # 3. Premium Table HTML to replace
    premium_table_html = r"""
    <table class="premium-data-table" style="width: 100%; border-collapse: collapse; margin: 24px 0; border: 1px solid var(--border); border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.02);">
        <thead>
            <tr style="background-color: var(--bg-secondary); border-bottom: 2px solid var(--border);">
                <th style="padding: 14px; text-align: center; font-weight: 800; color: var(--text-primary); border-right: 1px solid var(--border); width: 18%; font-size: 0.9rem;">구분</th>
                <th style="padding: 14px; text-align: center; font-weight: 800; color: var(--text-primary); border-right: 1px solid var(--border); width: 27%; font-size: 0.9rem;">배관용 탄소강관<br><span style="font-size: 0.78rem; font-weight: 500; color: var(--text-muted);">(KS D 3507, SPP)</span></th>
                <th style="padding: 14px; text-align: center; font-weight: 800; color: var(--text-primary); border-right: 1px solid var(--border); width: 28%; font-size: 0.9rem;">압력 배관용 탄소강관<br><span style="font-size: 0.78rem; font-weight: 500; color: var(--text-muted);">(KS D 3562, SPPS)</span></th>
                <th style="padding: 14px; text-align: center; font-weight: 800; color: var(--text-primary); width: 27%; font-size: 0.9rem;">이음매 없는 강관<br><span style="font-size: 0.78rem; font-weight: 500; color: var(--text-muted);">(KS D 3563 등 Seamless)</span></th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom: 1px solid var(--border);">
                <td style="padding: 14px; text-align: center; font-weight: 800; color: var(--text-primary); background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.88rem;">적용 압력</td>
                <td style="padding: 14px; border-right: 1px solid var(--border);">
                    <span style="display: inline-block; padding: 5px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; background-color: rgba(59, 130, 246, 0.08); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.2);">
                        사용최고압력 1.2 MPa 이하
                    </span>
                </td>
                <td style="padding: 14px; border-right: 1px solid var(--border);">
                    <span style="display: inline-block; padding: 5px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; background-color: rgba(239, 68, 68, 0.08); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2);">
                        사용최고압력 1.2 MPa 초과
                    </span>
                </td>
                <td style="padding: 14px;">
                    <span style="display: inline-block; padding: 5px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; background-color: rgba(139, 92, 246, 0.08); color: #8b5cf6; border: 1px solid rgba(139, 92, 246, 0.2); margin-bottom: 6px;">
                        가스계 소화설비 등 고압
                    </span>
                    <div style="font-size: 0.8rem; color: var(--text-secondary); margin-left: 4px;">- 고압식 19 MPa, 이산화탄소 계통 등</div>
                </td>
            </tr>
            <tr style="border-bottom: 1px solid var(--border); background-color: rgba(var(--accent-rgb), 0.005);">
                <td style="padding: 14px; text-align: center; font-weight: 800; color: var(--text-primary); background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.88rem;">제조 방법</td>
                <td style="padding: 14px; border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-secondary);">전기저항 용접(ERW), 단접</td>
                <td style="padding: 14px; border-right: 1px solid var(--border); font-size: 0.85rem; color: var(--text-secondary);">전기저항 용접(ERW), 이음매 없는 압연</td>
                <td style="padding: 14px; font-size: 0.85rem; color: var(--text-secondary);">단조, 인발, 압연 (이음매 용접부 없음)</td>
            </tr>
            <tr style="border-bottom: 1px solid var(--border);">
                <td style="padding: 14px; text-align: center; font-weight: 800; color: var(--text-primary); background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.88rem;">주요 적용 설비</td>
                <td style="padding: 14px; border-right: 1px solid var(--border); font-size: 0.82rem; line-height: 1.75; color: var(--text-secondary);">
                    <div style="padding-left: 12px; text-indent: -12px;">• 옥내·외소화전, 스프링클러</div>
                    <div style="padding-left: 12px; text-indent: -12px; margin-top: 4px;">• 연결송수관 (저층부 저압관로)</div>
                    <div style="padding-left: 12px; text-indent: -12px; margin-top: 4px;">• 물분무, 포소화설비 일반 수계배관</div>
                </td>
                <td style="padding: 14px; border-right: 1px solid var(--border); font-size: 0.82rem; line-height: 1.75; color: var(--text-secondary);">
                    <div style="padding-left: 12px; text-indent: -12px;">• 고층 건축물의 수계 고압 배관</div>
                    <div style="padding-left: 12px; text-indent: -12px; margin-top: 4px;">• 가압송수장치 토출측 주배관 (&gt; 1.2 MPa)</div>
                    <div style="padding-left: 12px; text-indent: -12px; margin-top: 4px;">• 할로겐화합물 및 불활성기체 소화설비</div>
                </td>
                <td style="padding: 14px; font-size: 0.82rem; line-height: 1.75; color: var(--text-secondary);">
                    <div style="padding-left: 12px; text-indent: -12px;">• 이산화탄소 소화설비 (저장용기 ~ 선택밸브 후단)</div>
                    <div style="padding-left: 12px; text-indent: -12px; margin-top: 4px;">• 불활성기체 고압 저장용기 집합관</div>
                    <div style="padding-left: 12px; text-indent: -12px; margin-top: 4px;">• 초고압 미분무 고압배관</div>
                </td>
            </tr>
            <tr style="background-color: rgba(var(--accent-rgb), 0.005);">
                <td style="padding: 14px; text-align: center; font-weight: 800; color: var(--text-primary); background-color: var(--bg-secondary); border-right: 1px solid var(--border); font-size: 0.88rem;">인장 강도</td>
                <td style="padding: 14px; border-right: 1px solid var(--border); font-size: 0.85rem; font-weight: 700; color: var(--text-primary); font-family: 'Fira Code', monospace;">290 MPa (30 kgf/mm²) 이상</td>
                <td style="padding: 14px; border-right: 1px solid var(--border); font-size: 0.85rem; font-weight: 700; color: var(--text-primary); font-family: 'Fira Code', monospace;">380 MPa (39 kgf/mm²) 이상</td>
                <td style="padding: 14px; font-size: 0.85rem; font-weight: 700; color: var(--text-primary); font-family: 'Fira Code', monospace;">380 ~ 510 MPa 이상 (강종별 구분)</td>
            </tr>
        </tbody>
    </table>
    """
    
    # 4. Replace original table with new structured table
    target_table.replace_with(BeautifulSoup(premium_table_html, "html.parser").table)
    print("Table successfully refactored inside BeautifulSoup DOM.")
    
    # 5. Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Successfully saved updated HTML to: {file_path}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = refactor_q37_table(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied updated HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
