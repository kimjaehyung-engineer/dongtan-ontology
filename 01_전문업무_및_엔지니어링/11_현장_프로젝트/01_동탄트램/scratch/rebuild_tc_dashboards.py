import os, re

base_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표'
dist_dir = os.path.join(base_dir, 'time-chainage-mvp', 'dist')
assets_dir = os.path.join(dist_dir, 'assets')

css_path = os.path.join(assets_dir, 'index-BV-kqEkz.css')
js_path = os.path.join(assets_dir, 'index-no5s-_SR.js')
target_standalone_html = os.path.join(base_dir, '동탄트램_Time_Chainage_공정표_대시보드.html')
dist_index_html = os.path.join(dist_dir, 'index.html')

# Read original files
with open(css_path, 'r', encoding='utf-8', errors='ignore') as f:
    css_content = f.read()

with open(js_path, 'r', encoding='utf-8', errors='ignore') as f:
    js_content = f.read()

# Stripping default export to avoid SyntaxError in non-module or inline settings
js_content_clean = re.sub(r'export\s*\{[^}]*\}\s*;?\s*$', '/* export stripped */', js_content.strip())

# === 1. BUILD STANDALONE HTML (Using safe replace to prevent F-string brace breakage) ===
html_template = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>동탄트램 Time-Chainage & 예정공정표 대시보드</title>
  <style>
__CSS_CONTENT__
  </style>
  <style>
    * { box-sizing: border-box; }
    html, body {
      width: 100vw;
      height: 100vh;
      margin: 0;
      padding: 0;
      overflow: hidden;
      background-color: #0f172a;
      color: #f8fafc;
      font-family: Inter, -apple-system, sans-serif;
    }
    #root {
      width: 100vw;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }
    #root > div {
      width: 100%;
      height: 100%;
      flex: 1;
    }
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="module">
__JS_CONTENT__
  </script>
</body>
</html>
"""

standalone_html = html_template.replace('__CSS_CONTENT__', css_content).replace('__JS_CONTENT__', js_content_clean)

with open(target_standalone_html, 'w', encoding='utf-8') as f:
    f.write(standalone_html)
print(f"Created clean standalone HTML at: {target_standalone_html}")

# === 2. BUILD STANDARD REFERENCE HTML FOR DIST ===
reference_html = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>동탄트램 Time-Chainage & 예정공정표 대시보드</title>
  <link rel="stylesheet" href="./assets/index-BV-kqEkz.css">
  <style>
    * { box-sizing: border-box; }
    html, body {
      width: 100vw;
      height: 100vh;
      margin: 0;
      padding: 0;
      overflow: hidden;
      background-color: #0f172a;
      color: #f8fafc;
      font-family: Inter, -apple-system, sans-serif;
    }
    #root {
      width: 100vw;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }
    #root > div {
      width: 100%;
      height: 100%;
      flex: 1;
    }
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="./assets/index-no5s-_SR.js"></script>
</body>
</html>
"""

with open(dist_index_html, 'w', encoding='utf-8') as f:
    f.write(reference_html)
print(f"Created standard reference HTML at: {dist_index_html}")
