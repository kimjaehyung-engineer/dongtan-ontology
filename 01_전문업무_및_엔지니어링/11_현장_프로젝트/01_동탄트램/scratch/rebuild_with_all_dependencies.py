import os, re

app_jsx_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src\App.jsx'
index_css_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src\index.css'

output_html_path1 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'
output_html_path2 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\index.html'

with open(app_jsx_path, 'r', encoding='utf-8') as f:
    app_jsx = f.read()

with open(index_css_path, 'r', encoding='utf-8') as f:
    index_css = f.read()

# Strip import / export statements safely
app_jsx_clean = re.sub(r'import\s+.*?;?\n', '', app_jsx)
app_jsx_clean = re.sub(r'export\s+default\s+\w+;?', '', app_jsx_clean)

# Recharts destructured variables
recharts_helpers = """
const { ResponsiveContainer, ScatterChart, Scatter, LineChart, Line, XAxis, YAxis, ZAxis, CartesianGrid, Tooltip, Legend, ReferenceLine, ReferenceArea, Dot, LabelList } = window.Recharts || {};
const { useState, useEffect, useRef, useMemo, useCallback } = React;

// Inline date-fns helpers
const parseISO = (str) => {
  if (!str) return new Date();
  if (str instanceof Date) return str;
  return new Date(str);
};

const getTime = (date) => {
  const d = parseISO(date);
  return d.getTime();
};

const format = (date, fmtStr) => {
  if (!date) return '';
  const d = parseISO(date);
  if (isNaN(d.getTime())) return '';
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  const hh = String(d.getHours()).padStart(2, '0');
  const min = String(d.getMinutes()).padStart(2, '0');
  
  if (fmtStr === 'yyyy-MM-dd') return `${yyyy}-${mm}-${dd}`;
  if (fmtStr === 'MM/dd') return `${mm}/${dd}`;
  if (fmtStr === 'yyyy.MM.dd') return `${yyyy}.${mm}.${dd}`;
  if (fmtStr === 'yyyy-MM') return `${yyyy}-${mm}`;
  return `${yyyy}-${mm}-${dd}`;
};

// html2canvas & jsPDF fallbacks if needed
const html2canvas = window.html2canvas || (async (el) => ({ toDataURL: () => '' }));
const jsPDF = window.jspdf?.jsPDF || class { save() {} addImage() {} };
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
  
  <!-- XLSX Library -->
  <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>

  <!-- HTML2Canvas & jsPDF -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>

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

print(f"Successfully built complete HTML with date-fns & Recharts helpers ({os.path.getsize(output_html_path1)} bytes)!")
