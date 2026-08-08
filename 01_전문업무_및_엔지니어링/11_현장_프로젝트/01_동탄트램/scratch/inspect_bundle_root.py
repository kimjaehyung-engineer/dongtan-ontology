import os

js_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\assets\index-no5s-_SR.js'

with open(js_path, 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

print(f"JS Total length: {len(code)} chars")

print("\n=== Search for root element ===")
pos = code.find('document.getElementById')
while pos != -1:
    print(f"Found getElementById at {pos}: {code[pos:pos+100]}")
    pos = code.find('document.getElementById', pos + 1)
