import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# FIX 1: Set :root default to LIGHT theme colors instead of dark
old_root = """:root {
  --bg-color: #0f172a;
  --panel-bg: #1e293b;
  --card-bg: #1e293b;
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
  --border-color: #334155;
  --blue-glow: 0 0 15px rgba(29, 111, 232, 0.6);
  --red-glow: 0 0 15px rgba(224, 49, 49, 0.6);
  --blue: #1d6fe8;
  --red: #e03131;
  --glass-bg: rgba(30, 41, 59, 0.85);
  --header-bg: linear-gradient(135deg, #1e293b, #0f172a);"""

new_root = """:root {
  --bg-color: #f8fafc;
  --panel-bg: #ffffff;
  --card-bg: #ffffff;
  --text-primary: #0f172a;
  --text-secondary: #334155;
  --text-muted: #64748b;
  --border-color: #cbd5e1;
  --blue-glow: 0 0 15px rgba(29, 111, 232, 0.6);
  --red-glow: 0 0 15px rgba(224, 49, 49, 0.6);
  --blue: #1d6fe8;
  --red: #e03131;
  --glass-bg: rgba(255, 255, 255, 0.85);
  --header-bg: linear-gradient(135deg, #ffffff, #f1f5f9);"""

if old_root in text:
    text = text.replace(old_root, new_root, 1)
    print("✓ Fixed :root to light theme defaults")

# FIX 2: Replace .light-theme with .dark-theme override
old_light = """.light-theme {
  --bg-color: #f8fafc;
  --panel-bg: #ffffff;
  --card-bg: #ffffff;
  --text-primary: #0f172a;
  --text-secondary: #334155;
  --text-muted: #64748b;
  --border-color: #cbd5e1;
  --glass-bg: rgba(255, 255, 255, 0.85);
  --header-bg: linear-gradient(135deg, #ffffff, #f1f5f9);
}"""

new_dark = """.dark-theme {
  --bg-color: #0f172a;
  --panel-bg: #1e293b;
  --card-bg: #1e293b;
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
  --border-color: #334155;
  --glass-bg: rgba(30, 41, 59, 0.85);
  --header-bg: linear-gradient(135deg, #1e293b, #0f172a);
}"""

if old_light in text:
    text = text.replace(old_light, new_dark, 1)
    print("✓ Replaced .light-theme with .dark-theme CSS override")

# FIX 3: Update theme toggle JS - swap light-theme to dark-theme
text = text.replace(
    'document.body.classList.toggle("light-theme");',
    'document.body.classList.toggle("dark-theme");'
)
text = text.replace(
    'document.body.classList.contains("light-theme") ? "☀️" : "🌙"',
    'document.body.classList.contains("dark-theme") ? "🌙" : "☀️"'
)
text = text.replace(
    'localStorage.setItem("v1-theme", document.body.classList.contains("light-theme") ? "light" : "dark");',
    'localStorage.setItem("v1-theme", document.body.classList.contains("dark-theme") ? "dark" : "light");'
)
print("✓ Updated theme toggle JS to dark-theme class")

# FIX 4: Update DOMContentLoaded theme load
text = text.replace(
    'if (localStorage.getItem("v1-theme") === "light") {\n    document.body.classList.add("light-theme");\n    btnTheme.textContent = "☀️";\n  }',
    'if (localStorage.getItem("v1-theme") === "dark") {\n    document.body.classList.add("dark-theme");\n    btnTheme.textContent = "🌙";\n  }'
)
print("✓ Updated DOMContentLoaded theme initialization")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"\n✅ Fixed light theme as default! File size: {len(text)} bytes")
