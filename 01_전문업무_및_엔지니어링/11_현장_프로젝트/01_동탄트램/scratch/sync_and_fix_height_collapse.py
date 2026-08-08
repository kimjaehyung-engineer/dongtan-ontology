import os, sys, shutil, json, re

sys.stdout.reconfigure(encoding='utf-8')

target_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'
dist_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\index.html'

with open(target_html, 'r', encoding='utf-8') as f:
    html = f.read()

# Fix layout collapse CSS: add explicit px heights to wrapper and chart-box
fixed_html = html.replace(
    '.chart-box {\n      flex: 1; background: var(--bg-panel); border: 1px solid var(--border);',
    '.chart-box {\n      flex: 1; background: var(--bg-panel); border: 1px solid var(--border); min-height: 540px; height: 100%;'
).replace(
    '.svg-wrapper {\n      flex: 1; width: 100%; height: 100%; position: relative; min-height: 400px; background: #ffffff;',
    '.svg-wrapper {\n      flex: 1; width: 100%; height: 100%; position: relative; min-height: 480px; height: 480px; background: #ffffff;'
)

with open(target_html, 'w', encoding='utf-8') as f:
    f.write(fixed_html)

# Synchronize 100% to dist/index.html
with open(dist_html, 'w', encoding='utf-8') as f:
    f.write(fixed_html)

print("✓ Successfully injected explicit 540px/480px CSS height guards & synchronized both HTML files 100%!")
