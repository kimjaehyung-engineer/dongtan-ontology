import os
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상"

for act_dir in os.listdir(base_dir):
    chk_dir = os.path.join(base_dir, act_dir, "체크리스트")
    if os.path.exists(chk_dir):
        files = [f for f in os.listdir(chk_dir) if f.endswith('.html')]
        if files:
            html_path = os.path.join(chk_dir, files[0])
            with open(html_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            print(f"=== Activity: {act_dir} ===")
            lis = soup.find_all('li')
            for li in lis[:4]:
                print("  -", li.get_text().strip())
