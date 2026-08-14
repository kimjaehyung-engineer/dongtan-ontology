import os, re

app_jsx_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src\App.jsx'
index_css_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src\index.css'

output_html_path1 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'
output_html_path2 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\index.html'

with open(app_jsx_path, 'r', encoding='utf-8') as f:
    app_jsx = f.read()

with open(index_css_path, 'r', encoding='utf-8') as f:
    index_css = f.read()

# Strip import / export statements
app_jsx_clean = re.sub(r'import\s+.*?;?\n', '', app_jsx)
app_jsx_clean = re.sub(r'export\s+default\s+\w+;?', '', app_jsx_clean)

recharts_helpers = """
const { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, ReferenceArea, Dot } = window.Recharts || {};
const { useState, useEffect, useRef, useMemo, useCallback } = React;
"""

template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>동탄트램 Time-Chainage & 예정공정표 대시보드</title>
  
  <!-- React 18 & ReactDOM CDN -->
  <script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
  
  <!-- Recharts CDN -->
  <script src="https://unpkg.com/recharts@2.12.7/umd/Recharts.js" crossorigin></script>
  
  <!-- Babel Standalone for JSX Parsing -->
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

  <style>
{index_css}
  </style>
  <style>
    * {{ box-sizing: border-box; }}
    html, body {{
      width: 100vw;
      height: 100vh;
      margin: 0;
      padding: 0;
      overflow: hidden;
      background-color: #f8fafc;
      color: #1e293b;
      font-family: 'Noto Sans KR', -apple-system, sans-serif;
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

  <script type="text/babel">
{recharts_helpers}

{app_jsx_clean}

const rootElement = document.getElementById("root");
if (rootElement) {{
  const root = ReactDOM.createRoot(rootElement);
  root.render(<App />);
}}
  </script>
</body>
</html>
"""

with open(output_html_path1, 'w', encoding='utf-8') as f:
    f.write(template)

with open(output_html_path2, 'w', encoding='utf-8') as f:
    f.write(template)

print(f"Created working HTML in both locations ({os.path.getsize(output_html_path1)} bytes)")
