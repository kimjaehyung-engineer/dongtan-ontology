import os, sys

sys.stdout.reconfigure(encoding='utf-8')

app_jsx_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src\App.jsx'

with open(app_jsx_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

pos = text.find('function mkInitialActivities')
if pos != -1:
    snippet = text[pos:pos+2000]
    safe_text = ''.join(c for c in snippet if ord(c) < 0xFFFF)
    print(safe_text)
