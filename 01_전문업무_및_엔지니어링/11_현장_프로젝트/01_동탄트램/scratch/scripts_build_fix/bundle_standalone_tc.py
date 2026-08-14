import os

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표'
tc_dir = os.path.join(base_dir, 'time-chainage-mvp', 'dist')
assets_dir = os.path.join(tc_dir, 'assets')

css_file = os.path.join(assets_dir, 'index-BV-kqEkz.css')
js_file = os.path.join(assets_dir, 'index-no5s-_SR.js')

target_html = os.path.join(base_dir, '동탄트램_Time_Chainage_공정표_대시보드.html')
dist_index_html = os.path.join(tc_dir, 'index.html')

with open(css_file, 'r', encoding='utf-8', errors='ignore') as f:
    css_text = f.read()

with open(js_file, 'r', encoding='utf-8', errors='ignore') as f:
    js_text = f.read()

# Build standalone HTML that embeds CSS and JS inline so it works anywhere without CORS/server issues!
standalone_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>동탄트램 Time-Chainage & 예정공정표 대시보드</title>
  <style>
{css_text}
  </style>
  <style>
    * {{ box-sizing: border-box; }}
    html, body {{
      width: 100vw;
      height: 100vh;
      margin: 0;
      padding: 0;
      overflow: hidden;
      background-color: #0f172a;
      color: #f8fafc;
      font-family: 'Noto Sans KR', sans-serif;
    }}
    #root {{
      width: 100vw;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }}
  </style>
</head>
<body>
  <div id="root"></div>
  <script>
{js_text}
  </script>
</body>
</html>
"""

# Write to both target standalone HTML and dist/index.html
with open(target_html, 'w', encoding='utf-8') as f:
    f.write(standalone_html)

with open(dist_index_html, 'w', encoding='utf-8') as f:
    f.write(standalone_html)

print(f"Created standalone HTML: {target_html} (size: {os.path.getsize(target_html)} bytes)")
print(f"Updated dist/index.html: {dist_index_html}")
