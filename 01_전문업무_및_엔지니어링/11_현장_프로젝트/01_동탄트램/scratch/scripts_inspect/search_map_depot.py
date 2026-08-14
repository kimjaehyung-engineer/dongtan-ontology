import os
import re

map_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\동탄트램_노선평면도.html"

with open(map_path, 'r', encoding='utf-8') as f:
    content = f.read()

terms = ["depot", "차량기지", "검수고", "시뮬레이터"]
for term in terms:
    count = content.count(term)
    print(f"Term '{term}': {count} occurrences")
