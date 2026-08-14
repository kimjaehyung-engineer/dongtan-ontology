import re

app_jsx_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src\App.jsx'

with open(app_jsx_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Find lucide imports
matches = re.findall(r'import\s+\{([^}]+)\}\s+from\s+[\'"]lucide-react[\'"]', text)
icons = []
for m in matches:
    icons.extend([icon.strip() for icon in m.split(',') if icon.strip()])

print("Lucide icons used in App.jsx:", set(icons))
