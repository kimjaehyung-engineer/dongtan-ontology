import os

dist_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist'
html_path = os.path.join(dist_dir, 'index.html')

html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <base href="./">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>동탄트램 Time-Chainage & 예정공정표 대시보드</title>
  <link rel="stylesheet" crossorigin href="./assets/index-BV-kqEkz.css">
  <style>
    * { box-sizing: border-box; }
    html, body {
      width: 100%;
      height: 100%;
      margin: 0;
      padding: 0;
      background-color: #f8fafc;
    }
    #root {
      width: 100%;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
  </style>
</head>

<body>
  <div id="root"></div>
  <script type="module" crossorigin src="./assets/index-no5s-_SR.js"></script>
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Updated index.html at {html_path}")
