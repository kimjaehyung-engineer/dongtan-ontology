import os
from bs4 import BeautifulSoup

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램"
manual_file = os.path.join(base_dir, "08.메뉴얼 및 평면도", "동탄트램_업무_매뉴얼.html")

with open(manual_file, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

style_tag = soup.find('style')
if style_tag:
    remove_all_lines_css = """
    /* ==========================================================================
       REMOVE ALL VERTICAL ACCENT LINES ON MAIN HEADINGS (대제목 수직 파란선 완전 제거)
       ========================================================================== */
    
    .section-header, .section-header__title, .section-header div, .section-header h2, section h2, section h1 {
      border-left: none !important;
      padding-left: 0 !important;
      margin-left: 0 !important;
      font-size: 1.85rem !important;
      font-weight: 800 !important;
      color: #0f172a !important;
      line-height: 1.3 !important;
    }

    .section-header::before, .section-header__title::before, .section-header div::before, .section-header h2::before, section h2::before, section h1::before {
      content: none !important;
      display: none !important;
      border: none !important;
    }
    """
    style_tag.string += "\n" + remove_all_lines_css

with open(manual_file, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("Successfully removed all vertical accent lines on main headings.")
