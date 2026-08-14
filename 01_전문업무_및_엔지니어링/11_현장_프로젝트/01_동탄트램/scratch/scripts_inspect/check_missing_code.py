import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print(f"Current file size: {len(text)} bytes")

# Check what's present and what's missing
checks = {
    'drawPaths': 'function drawPaths' in text,
    'drawDistances': 'function drawDistances' in text,
    'renderIntersections': 'function renderIntersections' in text,
    'renderConstructionSections': 'function renderConstructionSections' in text,
    'renderInteractiveElements': 'function renderInteractiveElements' in text,
    'selectConstructionSection': 'function selectConstructionSection' in text,
    'selectIntersection': 'function selectIntersection' in text,
    'focusCoordinates': 'function focusCoordinates' in text,
    'openIntersectionDrawer': 'function openIntersectionDrawer' in text,
    'openIntersectionModal': 'function openIntersectionModal' in text,
    'DOMContentLoaded': 'DOMContentLoaded' in text,
    'toggle-bg listener': 'getElementById("toggle-bg")' in text,
    'btnTheme': 'btnTheme' in text,
    'applyFontSize': 'applyFontSize' in text,
    'activitiesDatabase': 'activitiesDatabase' in text,
    'initScheduleIntegration': 'initScheduleIntegration' in text,
    'schedule-panel HTML': 'id="schedule-panel"' in text,
    'schedule CSS': '.schedule-panel-container' in text,
    'floating-trigger-group': 'floating-trigger-group' in text,
    'btn-open-schedule-panel': 'btn-open-schedule-panel' in text,
    'constructionSections data': 'const constructionSections' in text,
    'intersectionData': 'const intersectionData' in text,
    'stationData': 'const stationData' in text,
    'nodes data': 'const nodes' in text,
}

print("\n=== CODE PRESENCE CHECK ===")
for name, present in checks.items():
    status = "✓ PRESENT" if present else "✗ MISSING"
    print(f"  {status}: {name}")

# Count DOMContentLoaded
dom_count = text.count('DOMContentLoaded')
print(f"\n  DOMContentLoaded count: {dom_count}")
