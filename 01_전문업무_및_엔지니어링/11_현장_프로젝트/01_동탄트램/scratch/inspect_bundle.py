import os

js_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\assets\index-no5s-_SR.js'

with open(js_path, 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

print(f"JS Total length: {len(code)} chars")
print("\n=== First 500 chars ===")
print(code[:500])

print("\n=== Last 500 chars ===")
print(code[-500:])

# Check if document.getElementById("root") or ReactDOM.createRoot is used
print("\n=== Search for root / createRoot / render ===")
for m in ['createRoot', 'getElementById("root")', 'getElementById(\'root\')', 'render(']:
    pos = code.find(m)
    print(f"  '{m}': found at {pos}")
