import re

app_jsx_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src\App.jsx'

with open(app_jsx_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Search for JSX Tags like <Something ...
tags = set(re.findall(r'<([A-Z][a-zA-Z0-9]*)\b', text))
print("=== All JSX Tags used in App.jsx ===")
print(sorted(list(tags)))

# 2. Check for Lucide icons or other components used inside JSX or JS
# Find component definitions: const Something = ... or function Something
defined_components = set(re.findall(r'(?:const|function|class)\s+([A-Z][a-zA-Z0-9]*)', text))
print("\n=== Defined Components/Classes in App.jsx ===")
print(sorted(list(defined_components)))

undefined_tags = tags - defined_components
print("\n=== Tags NOT defined in App.jsx itself (must come from imports/globals) ===")
print(sorted(list(undefined_tags)))
