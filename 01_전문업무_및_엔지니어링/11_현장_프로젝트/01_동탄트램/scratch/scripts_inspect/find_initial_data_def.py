import os

app_jsx_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src\App.jsx'

with open(app_jsx_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

pos = text.find('const INITIAL_DATA')
if pos != -1:
    print(text[pos:pos+2500].encode('utf-8', errors='ignore').decode('utf-8', errors='ignore'))
