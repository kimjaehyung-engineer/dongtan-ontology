import os

js_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\assets\index-no5s-_SR.js'

with open(js_path, 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# Check for Leaflet / Mapbox / React Flow / ECharts / Recharts / ChartJS
libraries = ['leaflet', 'mapbox', 'react-flow', 'echarts', 'recharts', 'chart.js', 'canvas', 'svg', 'D3']
print("=== Libraries detected in JS bundle ===")
for lib in libraries:
    count = code.lower().count(lib)
    print(f"  {lib}: {count} occurrences")

# Check for CSS links in JS or unhandled exceptions
pos = code.find('throw')
print("\nFirst throw statement in JS:", code[pos:pos+100] if pos != -1 else "None")
