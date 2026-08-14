import os
from bs4 import BeautifulSoup

def fix_headings():
    files = [
        "08.메뉴얼 및 평면도/동탄트램_업무_매뉴얼.html",
        "03_보고서_및_출력/지장물_이설_업무_매뉴얼.html"
    ]
    
    mapping = {
        "sec-railway-plan": "1. 철도계획",
        "sec-intro": "2. 노반 및 지장물 이설",
        "sec-architecture": "3. 건축",
        "sec-depot": "4. 차량기지",
        "sec-arch-plan": "5. 건축계획",
        "sec-geotechnical": "6. 토질 및 기초",
        "sec-structure": "7. 구조",
        "sec-systems": "8. 시스템 (전기·통신·신호)",
        "sec-track": "9. 궤도",
        "sec-inspection": "10. 검수",
        "sec-construction-mgt": "11. 공사관리"
    }
    
    for filepath in files:
        if not os.path.exists(filepath):
            print(f"File {filepath} not found. Skipping.")
            continue
            
        print(f"Fixing H1 headers in {filepath}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse using BeautifulSoup with HTML parser
        soup = BeautifulSoup(content, 'html.parser')
        
        for sec_id, correct_title in mapping.items():
            section = soup.find('section', id=sec_id)
            if not section:
                print(f"  Warning: Section with id={sec_id} not found.")
                continue
                
            h1 = section.find('h1')
            if h1:
                # Replace content inside h1 with correct title
                h1.string = correct_title
                print(f"  Updated existing H1 inside #{sec_id} to '{correct_title}'")
            else:
                # Special case: sec-intro in 지장물_이설_업무_매뉴얼.html might not have H1
                if sec_id == "sec-intro":
                    print(f"  H1 missing in #sec-intro. Inserting fully styled header block...")
                    header_html = f"""
            <div style="border-bottom: 2px solid var(--border-color); padding-bottom: 1.25rem; margin-bottom: 2.5rem; margin-top: 1rem;">
                <span class="category-tag" style="margin-bottom: 0.5rem; display: inline-block;">노반 공종 가이드라인</span>
                <h1 style="font-size: 2.5rem; font-weight: 800; color: var(--text-primary); margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.6rem; letter-spacing: -0.02em;">
                    {correct_title}
                </h1>
                <p style="color: var(--text-muted); font-size: 1rem; font-weight: 500; margin: 0; line-height: 1.6;">
                    노반 건설 구간 내 지상 및 지하지장물의 조사 절차, 관계기관 인허가 협의, 시공 단계 안전 대책과 정산 업무 지침을 다룹니다.
                </p>
            </div>
                    """
                    # Parse header_html and insert as first child of section
                    header_soup = BeautifulSoup(header_html, 'html.parser')
                    section.insert(0, header_soup)
                    print(f"  Successfully inserted missing Section 2 H1 header!")
                else:
                    print(f"  Warning: H1 missing in #{sec_id}")
                    
        # Write clean html back to file (keep encoding utf-8)
        # Use formatter="html" to avoid altering spacing too much
        html_str = str(soup)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_str)
        print(f"  Saved {filepath} successfully!")

if __name__ == '__main__':
    fix_headings()
