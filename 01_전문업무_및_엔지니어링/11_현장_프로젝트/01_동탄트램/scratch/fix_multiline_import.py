import os, re

app_jsx_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src\App.jsx'
index_css_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src\index.css'

output_html_path1 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'
output_html_path2 = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\index.html'

with open(app_jsx_path, 'r', encoding='utf-8') as f:
    app_jsx = f.read()

with open(index_css_path, 'r', encoding='utf-8') as f:
    index_css = f.read()

# Multiline aware import / export cleaning
app_jsx_clean = re.sub(r'import\s+[\s\S]*?from\s+[\'"].*?[\'"];?', '', app_jsx)
app_jsx_clean = re.sub(r'import\s+[\'"].*?[\'"];?', '', app_jsx_clean)
app_jsx_clean = re.sub(r'export\s+default\s+\w+;?', '', app_jsx_clean)

# Safe Recharts & React helper bindings
recharts_helpers = """
window.addEventListener('error', function(e) {
  console.error("Runtime Error:", e);
  const errDiv = document.getElementById('debug-error-log');
  if (errDiv) {
    errDiv.style.display = 'block';
    errDiv.innerHTML += '<div><b>[Error]</b> ' + (e.message || e) + ' (line ' + (e.lineno || 0) + ')</div>';
  }
});

const R = window.Recharts || window.recharts || {};

const ResponsiveContainer = R.ResponsiveContainer || (({children}) => React.createElement('div', {style:{width:'100%',height:'100%'}}, children));
const ScatterChart = R.ScatterChart || (({children}) => React.createElement('div', null, children));
const Scatter = R.Scatter || (() => null);
const LineChart = R.LineChart || (({children}) => React.createElement('div', null, children));
const Line = R.Line || (() => null);
const XAxis = R.XAxis || (() => null);
const YAxis = R.YAxis || (() => null);
const ZAxis = R.ZAxis || (() => null);
const CartesianGrid = R.CartesianGrid || (() => null);
const Tooltip = R.Tooltip || (() => null);
const Legend = R.Legend || (() => null);
const ReferenceLine = R.ReferenceLine || (() => null);
const ReferenceArea = R.ReferenceArea || (() => null);
const Dot = R.Dot || (() => null);
const LabelList = R.LabelList || (() => null);

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
  <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js" crossorigin></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js" crossorigin></script>
  
  <!-- Recharts 2.10.3 UMD CDN -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/recharts/2.10.3/Recharts.min.js" crossorigin></script>
  
  <!-- XLSX Library -->
  <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>

  <!-- Babel Standalone -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.6/babel.min.js"></script>

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
    #debug-error-log {{
      display: none;
      position: fixed;
      bottom: 10px;
      right: 10px;
      background: #fef2f2;
      border: 1px solid #fca5a5;
      color: #991b1b;
      padding: 10px;
      border-radius: 6px;
      font-size: 12px;
      max-width: 400px;
      max-height: 200px;
      overflow-y: auto;
      z-index: 99999;
    }}
  </style>
</head>
<body>
  <div id="root"></div>
  <div id="debug-error-log"></div>

  <script type="text/babel">
{recharts_helpers}

{app_jsx_clean}

window.addEventListener('load', () => {{
  const rootElement = document.getElementById("root");
  if (rootElement && typeof ReactDOM !== 'undefined') {{
    const root = ReactDOM.createRoot(rootElement);
    root.render(<App />);
  }}
}});
  </script>
</body>
</html>
"""

with open(output_html_path1, 'w', encoding='utf-8') as f:
    f.write(template)

with open(output_html_path2, 'w', encoding='utf-8') as f:
    f.write(template)

print("Successfully fixed multiline import regex and rebuilt HTML!")
