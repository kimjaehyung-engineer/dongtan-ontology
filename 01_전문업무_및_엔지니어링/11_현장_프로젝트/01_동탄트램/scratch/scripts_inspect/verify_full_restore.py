import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print(f"File size: {len(text)} bytes")

# Full verification
checks = {
    'drawPaths function': 'function drawPaths' in text,
    'drawDistances function': 'function drawDistances' in text,
    'drawTurnouts function': 'function drawTurnouts' in text,
    'renderIntersections function': 'function renderIntersections' in text,
    'renderConstructionSections function': 'function renderConstructionSections' in text,
    'renderInteractiveElements function': 'function renderInteractiveElements' in text,
    'selectConstructionSection function': 'function selectConstructionSection' in text,
    'selectIntersection function': 'function selectIntersection' in text,
    'focusCoordinates function': 'function focusCoordinates' in text,
    'openIntersectionDrawer function': 'function openIntersectionDrawer' in text,
    'openIntersectionModal function': 'function openIntersectionModal' in text,
    'closeIntersectionModal function': 'function closeIntersectionModal' in text,
    'applyFontSize function': 'function applyFontSize' in text,
    'bindRoutePathEvents function': 'function bindRoutePathEvents' in text,
    'toggle-bg listener': 'getElementById("toggle-bg")' in text,
    'toggle-routes listener': 'getElementById("toggle-routes")' in text,
    'toggle-labels listener': 'getElementById("toggle-labels")' in text,
    'toggle-construction-sections listener': 'getElementById("toggle-construction-sections")' in text,
    'btnTheme variable': 'const btnTheme' in text,
    ':root dark bg': '#0f172a' in text.split('.light-theme')[0][:2000],
    '.light-theme CSS': '.light-theme {' in text,
    'DOMContentLoaded with drawPaths': 'drawPaths()' in text,
    'constructionSections data': 'const constructionSections' in text,
    'intersectionData': 'const intersectionData' in text,
    'nodes data': 'const nodes' in text,
}

print("\n=== FULL VERIFICATION ===")
all_ok = True
for name, present in checks.items():
    status = "✓" if present else "✗"
    if not present:
        all_ok = False
    print(f"  {status} {name}")

# Check NO schedule code
schedule_checks = {
    'activitiesDatabase (should be ABSENT)': 'activitiesDatabase' not in text,
    'initScheduleIntegration (should be ABSENT)': 'initScheduleIntegration' not in text,
    'schedule-panel HTML (should be ABSENT)': 'id="schedule-panel"' not in text,
    'schedule CSS (should be ABSENT)': '.schedule-panel-container' not in text,
    'floating-trigger-group (should be ABSENT)': 'floating-trigger-group' not in text,
    'btn-open-schedule-panel (should be ABSENT)': 'btn-open-schedule-panel' not in text,
}

print("\n=== SCHEDULE CODE REMOVAL CHECK ===")
for name, absent in schedule_checks.items():
    status = "✓" if absent else "✗"
    if not absent:
        all_ok = False
    print(f"  {status} {name}")

# Check JS brace balance
script_start = text.find('<script>')
script_end = text.find('</script>')
js_block = text[script_start+8:script_end]
open_b = js_block.count('{')
close_b = js_block.count('}')
print(f"\n=== JS BRACE BALANCE ===")
print(f"  Open: {open_b}, Close: {close_b}, Match: {open_b == close_b}")
if open_b != close_b:
    all_ok = False

dom_count = text.count('DOMContentLoaded')
print(f"\n  DOMContentLoaded count: {dom_count}")

print(f"\n{'✅ ALL CHECKS PASSED!' if all_ok else '❌ SOME CHECKS FAILED!'}")
