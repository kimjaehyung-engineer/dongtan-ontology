import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print("=== :root verification ===")
root_match = re.search(r':root\s*\{([^}]*)\}', text, re.DOTALL)
if root_match:
    root_text = root_match.group(1)
    has_light_bg = '#f8fafc' in root_text
    has_light_text = '#0f172a' in root_text
    print(f"  --bg-color #f8fafc (light): {has_light_bg}")
    print(f"  --text-primary #0f172a (dark text): {has_light_text}")

print("\n=== Theme class verification ===")
has_dark_theme_class = '.dark-theme' in text
has_light_theme_class = '.light-theme' in text
print(f"  .dark-theme CSS exists: {has_dark_theme_class}")
print(f"  .light-theme CSS exists: {has_light_theme_class}")

has_toggle_dark = 'toggle("dark-theme")' in text
print(f"  JS toggle dark-theme: {has_toggle_dark}")

print("\n=== Layer toggle listener verification ===")
toggle_checks = [
    'toggle-bg', 'toggle-routes', 'toggle-nodes', 'toggle-labels',
    'toggle-distances', 'toggle-turnouts', 'toggle-intersections-lines',
    'toggle-intersections-labels', 'toggle-construction-sections'
]
for tid in toggle_checks:
    has_listener = f'getElementById("{tid}")' in text
    print(f"  {tid}: listener present = {has_listener}")
