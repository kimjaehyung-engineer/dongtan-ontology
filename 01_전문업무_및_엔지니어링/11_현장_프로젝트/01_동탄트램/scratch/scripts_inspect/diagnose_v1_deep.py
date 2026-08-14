import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Check light-theme CSS override block
light_idx = text.find('.light-theme')
if light_idx != -1:
    print("=== .light-theme CSS block ===")
    print(text[light_idx:light_idx+500])
else:
    print("!! .light-theme CSS block NOT FOUND !!")

# 2. Check toggle layer event listeners
toggle_listener_idx = text.find('toggle-bg')
if toggle_listener_idx != -1:
    # find the second occurrence (JS event listener, not HTML checkbox)
    second_idx = text.find('toggle-bg', toggle_listener_idx + 10)
    if second_idx != -1:
        print("\n=== Toggle-bg JS listener snippet ===")
        print(text[second_idx-200:second_idx+600])

# 3. Check for broken CSS from my insertion - look for unclosed CSS blocks
style_start = text.find('<style>')
style_end = text.find('</style>')
css_block = text[style_start:style_end]
print(f"\n=== CSS block size: {len(css_block)} chars ===")

# Count open vs close braces
open_braces = css_block.count('{')
close_braces = css_block.count('}')
print(f"  Open braces {{: {open_braces}")
print(f"  Close braces }}: {close_braces}")
if open_braces != close_braces:
    print(f"  !! MISMATCH: {open_braces - close_braces} unclosed braces !!")

# 4. Check for initScheduleIntegration call in DOMContentLoaded
dom_idx = text.find('DOMContentLoaded')
if dom_idx != -1:
    dom_block = text[dom_idx:dom_idx+500]
    print(f"\n  initScheduleIntegration in DOMContentLoaded: {'initScheduleIntegration' in dom_block}")

# 5. Check for second DOMContentLoaded (might cause issues)
second_dom = text.find('DOMContentLoaded', dom_idx + 10)
if second_dom != -1:
    print(f"\n=== SECOND DOMContentLoaded found at position {second_dom} ===")
    print(text[second_dom-50:second_dom+300])
