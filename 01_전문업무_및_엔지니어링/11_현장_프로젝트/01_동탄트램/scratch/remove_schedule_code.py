import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print(f"BEFORE cleanup: {len(text)} bytes")

# ========== STEP 1: Remove Schedule CSS ==========
# Find and remove all schedule-related CSS blocks
css_patterns_to_remove = [
    # .schedule-panel-container block
    r'\.schedule-panel-container\s*\{[^}]*\}',
    r'\.schedule-panel-header\s*\{[^}]*\}',
    r'\.schedule-panel-body\s*\{[^}]*\}',
    r'\.sch-tree-item\s*\{[^}]*\}',
    r'\.sch-tree-item\.active\s*\{[^}]*\}',
    r'\.sch-tree-item:hover\s*\{[^}]*\}',
    r'\.sch-badge\s*\{[^}]*\}',
    r'\.sch-act-row\s*\{[^}]*\}',
    r'\.sch-act-row:hover\s*\{[^}]*\}',
    r'\.sch-act-code\s*\{[^}]*\}',
    r'\.sch-act-name\s*\{[^}]*\}',
    r'\.sch-act-dur\s*\{[^}]*\}',
    r'\.btn-open-schedule-panel\s*\{[^}]*\}',
    r'\.act-focus-pulse\s*\{[^}]*\}',
    r'@keyframes\s+act-pulse\s*\{[^}]*\{[^}]*\}[^}]*\{[^}]*\}[^}]*\}',
    r'\.floating-trigger-group\s*\{[^}]*\}',
]
for pat in css_patterns_to_remove:
    text = re.sub(pat, '', text)
    
print("✓ Removed schedule CSS blocks")

# ========== STEP 2: Remove Schedule Panel HTML ==========
# Remove the entire schedule panel HTML block
schedule_panel_start = text.find('<!-- 공정표 연동 사이드 패널 -->')
if schedule_panel_start == -1:
    schedule_panel_start = text.find('<div id="schedule-panel"')
if schedule_panel_start == -1:
    schedule_panel_start = text.find('id="schedule-panel"')
    
if schedule_panel_start != -1:
    # Find the closing div - need to count nesting
    # Look for the schedule panel container div end
    search_start = schedule_panel_start
    panel_end = text.find('</div><!-- /schedule-panel -->', search_start)
    if panel_end == -1:
        # Try to find the end by looking for the panel's closing structure
        # Find 'schedule-panel' id and remove from there until the next sibling
        panel_div_start = text.rfind('<div', max(0, search_start - 200), search_start + 50)
        if panel_div_start == -1:
            panel_div_start = search_start
        # Count nested divs to find matching close
        depth = 0
        i = panel_div_start
        while i < len(text):
            if text[i:i+4] == '<div':
                depth += 1
            elif text[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    panel_end = i + 6
                    break
            i += 1
        if panel_end != -1:
            removed = text[panel_div_start:panel_end]
            text = text[:panel_div_start] + text[panel_end:]
            print(f"✓ Removed schedule panel HTML ({len(removed)} chars)")
    else:
        panel_end += len('</div><!-- /schedule-panel -->')
        comment_start = text.rfind('<!--', max(0, schedule_panel_start - 100), schedule_panel_start)
        if comment_start == -1:
            comment_start = schedule_panel_start
        removed = text[comment_start:panel_end]
        text = text[:comment_start] + text[panel_end:]
        print(f"✓ Removed schedule panel HTML ({len(removed)} chars)")
else:
    print("  Schedule panel HTML not found")

# ========== STEP 3: Replace floating-trigger-group with original single button ==========
ftg_start = text.find('<div class="floating-trigger-group">')
if ftg_start != -1:
    ftg_end = text.find('</div>', ftg_start)
    if ftg_end != -1:
        ftg_end += 6
        # Also check if there's a second closing div
        next_chars = text[ftg_end:ftg_end+20].strip()
        if next_chars.startswith('</div>'):
            ftg_end += text[ftg_end:ftg_end+20].find('</div>') + 6
        
        old_ftg = text[ftg_start:ftg_end]
        # Replace with original single floating button
        new_btn = '<button id="btn-reset-view" class="btn-floating" title="전체 보기">🗺️</button>'
        text = text[:ftg_start] + new_btn + text[ftg_end:]
        print(f"✓ Replaced floating-trigger-group with original button")
else:
    print("  floating-trigger-group not found")

# ========== STEP 4: Remove schedule JS functions ==========
# Remove initScheduleIntegration function
init_idx = text.find('function initScheduleIntegration()')
if init_idx != -1:
    # Find the end of this function by brace counting
    brace_start = text.find('{', init_idx)
    depth = 0
    i = brace_start
    func_end = -1
    while i < len(text):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                func_end = i + 1
                break
        i += 1
    if func_end != -1:
        text = text[:init_idx] + text[func_end:]
        print(f"✓ Removed initScheduleIntegration function")

# Remove renderActivityTree function
rat_idx = text.find('function renderActivityTree(')
if rat_idx != -1:
    brace_start = text.find('{', rat_idx)
    depth = 0
    i = brace_start
    func_end = -1
    while i < len(text):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                func_end = i + 1
                break
        i += 1
    if func_end != -1:
        text = text[:rat_idx] + text[func_end:]
        print(f"✓ Removed renderActivityTree function")

# Remove focusActivityOnMap function
fam_idx = text.find('function focusActivityOnMap(')
if fam_idx != -1:
    brace_start = text.find('{', fam_idx)
    depth = 0
    i = brace_start
    func_end = -1
    while i < len(text):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                func_end = i + 1
                break
        i += 1
    if func_end != -1:
        text = text[:fam_idx] + text[func_end:]
        print(f"✓ Removed focusActivityOnMap function")

# Remove pRW_Stations, pRE_Stations, pRW2 data if present
for varname in ['const pRW_Stations', 'const pRE_Stations', 'const pRW2_Stations']:
    var_idx = text.find(varname)
    if var_idx != -1:
        # Find end of array
        bracket_start = text.find('[', var_idx)
        depth = 0
        i = bracket_start
        while i < len(text):
            if text[i] == '[':
                depth += 1
            elif text[i] == ']':
                depth -= 1
                if depth == 0:
                    arr_end = i + 1
                    # Skip semicolon
                    if arr_end < len(text) and text[arr_end] == ';':
                        arr_end += 1
                    break
            i += 1
        text = text[:var_idx] + text[arr_end:]
        print(f"✓ Removed {varname}")

# Remove initScheduleIntegration() call if in DOMContentLoaded
text = text.replace('  initScheduleIntegration();\n', '')
text = text.replace('initScheduleIntegration();\n', '')

print(f"\nAFTER schedule removal: {len(text)} bytes")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("✅ Schedule code removed!")
