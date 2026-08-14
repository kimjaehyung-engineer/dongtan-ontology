import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print(f"HTML total size: {len(text)} bytes")

# 1. Check for CSS issues - dark background
print("\n=== CSS / Background Issues ===")
# Check body or root background color
body_bg_matches = re.findall(r'body\s*\{[^}]*background[^}]*\}', text, re.DOTALL)
for m in body_bg_matches:
    print(f"  body CSS: {m[:200]}")

# Check :root variables
root_match = re.search(r':root\s*\{([^}]*)\}', text, re.DOTALL)
if root_match:
    root_text = root_match.group(1)
    print(f"\n  :root variables (first 600 chars): {root_text[:600]}")

# Check for dark mode CSS
dark_matches = re.findall(r'--bg-primary[^;]*;', text)
for d in dark_matches[:5]:
    print(f"  --bg-primary: {d}")

# 2. Check layer toggle listeners
print("\n=== Layer Toggle Listeners ===")
toggle_ids = ['toggle-bg', 'toggle-routes', 'toggle-nodes', 'toggle-labels', 'toggle-distances', 'toggle-turnouts', 'toggle-intersections-lines', 'toggle-intersections-labels', 'toggle-construction-sections']
for tid in toggle_ids:
    count = text.count(tid)
    print(f"  '{tid}': {count} occurrences")

# 3. Check if DOMContentLoaded has layer toggle setup
dom_loaded_idx = text.find('DOMContentLoaded')
if dom_loaded_idx != -1:
    snippet = text[dom_loaded_idx:dom_loaded_idx+2000]
    print(f"\n=== DOMContentLoaded snippet (first 1500 chars) ===")
    print(snippet[:1500])

# 4. Check for duplicate </style> or broken CSS
style_count = text.count('</style>')
print(f"\n  Number of </style> tags: {style_count}")
script_count = text.count('</script>')
print(f"  Number of </script> tags: {script_count}")
