import os

js_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\assets\index-no5s-_SR.js'

with open(js_path, 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# Search for any dynamic fetch or path resolution in JS bundle
print("=== Search for fetch, absolute paths, assets or endpoints in JS ===")
keywords = ['fetch(', 'axios.', '/api/', 'url(', 'window.location']
for kw in keywords:
    pos = code.find(kw)
    if pos != -1:
        print(f"  Found '{kw}' at {pos}: {code[pos:pos+150]}")
