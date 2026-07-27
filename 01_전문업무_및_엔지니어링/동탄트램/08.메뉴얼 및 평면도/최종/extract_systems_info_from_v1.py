from bs4 import BeautifulSoup
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

v1_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\동탄트램_업무_매뉴얼v1.html"

with open(v1_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print(f"Loaded {v1_path}")

# Search for headers or text blocks containing 신호, 전기, 통신, SIL, LTE-R, DC 750V, SCADA, 변전소, 전차선, 교차로, 전자연동장치
keywords = ['신호', '전기', '통신', 'CBI', 'SIL', 'LTE-R', '변전소', '전차선', '급전', 'SCADA', 'PSD', 'CCTV', '축차계수기', '선로전환기', '무전차선', '오버헤드']

sections = []

for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'div', 'section']):
    txt = h.get_text().strip()
    for kw in keywords:
        if kw in txt and len(txt) < 300:
            sections.append((kw, txt))
            break

print(f"Found {len(sections)} relevant sections/headings:")
for kw, txt in sections[:30]:
    print(f"[{kw}] {txt[:100]}...")
