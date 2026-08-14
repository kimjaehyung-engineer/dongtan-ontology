import os

js_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\assets\index-no5s-_SR.js'

with open(js_path, 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

pos = code.find('index-BXynDoHT')
print(f"Occurrence of 'index-BXynDoHT': {pos}")
if pos != -1:
    print(code[max(0, pos-100):pos+200])
