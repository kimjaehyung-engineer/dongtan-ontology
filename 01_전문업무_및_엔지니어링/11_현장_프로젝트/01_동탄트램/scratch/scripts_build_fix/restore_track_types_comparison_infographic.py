import os
from bs4 import BeautifulSoup

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램"
manual_file = os.path.join(base_dir, "08.메뉴얼 및 평면도", "동탄트램_업무_매뉴얼.html")

with open(manual_file, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Check if track_types_comparison_detail.png exists in the manual
has_info = soup.find('img', src=lambda s: s and 'track_types_comparison_detail.png' in s)

if not has_info:
    print("Restoring track_types_comparison_detail.png right below item 2 in section 4.1...")
    # Find item 2 "궤도구조 및 하부 단면 상세 설계치"
    target_item = None
    for h in soup.find_all(['h4', 'div', 'p', 'strong']):
        if '궤도구조 및 하부 단면 상세 설계치' in h.text or '2. 궤도구조' in h.text:
            target_item = h
            if h.parent and h.parent.name in ['div', 'li']:
                target_item = h.parent
            break
            
    if target_item:
        img_div = soup.new_tag('div', style='text-align: center; margin: 2rem 0;')
        img_tag = soup.new_tag('img', src='./track_types_comparison_detail.png', alt='동탄트램 궤도 반-PC 슬래브 및 수지고정 상세', style='width: 100%; max-width: 950px; height: auto; border-radius: 8px; border: 1px solid var(--border-color); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);')
        img_div.append(img_tag)
        target_item.insert_after(img_div)
        print("Successfully restored infographic right below item 2!")

# Double check that NO tram_track_cross_section.png remains anywhere
for img in soup.find_all('img', src=lambda s: s and 'tram_track_cross_section.png' in s):
    img.decompose()

with open(manual_file, 'w', encoding='utf-8') as f:
    f.write(str(soup))
