import re

app_jsx_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src\App.jsx'

with open(app_jsx_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Find all component usage like <IconName .../> or lucide references
component_matches = re.findall(r'<([A-Z][a-zA-Z0-9]*)\s*', text)
unique_components = sorted(list(set(component_matches)))
print("=== All Capitalized Components used in App.jsx ===")
print(unique_components)

# Find any undefined variables or icons
imports = re.findall(r'import\s+.*', text)
print("\n=== Original Import Statements in App.jsx ===")
for imp in imports:
    print("  -", imp)
