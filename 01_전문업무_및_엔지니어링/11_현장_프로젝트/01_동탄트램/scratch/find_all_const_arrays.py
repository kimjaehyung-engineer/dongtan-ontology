import os, re

app_jsx_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src\App.jsx'

with open(app_jsx_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Search for const declarations
const_matches = re.findall(r'const\s+([A-Z0-9_]+)\s*=\s*\[', text)
print("=== Array constants defined in App.jsx ===")
print(const_matches)

# Print first 200 chars for each matching constant
for name in const_matches:
    p = text.find(f'const {name}')
    print(f"\n--- {name} ---")
    print(text[p:p+300])
