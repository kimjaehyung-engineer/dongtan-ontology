import os, re

app_jsx_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src\App.jsx'

with open(app_jsx_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Search for INITIAL_ACTIVITIES definition in App.jsx
matches = re.findall(r'const\s+INITIAL[A-Z_]*\s*=\s*\[[\s\S]*?\];', text)
print(f"Found INITIAL arrays: {len(matches)}")
for idx, m in enumerate(matches):
    print(f"\n--- Array {idx+1} (length: {len(m)}) ---")
    print(m[:600])
