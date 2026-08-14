import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Get the CSS block
style_start = text.find('<style>') + 7
style_end = text.find('</style>')
css = text[style_start:style_end]

# Remove all schedule-related CSS blocks using a more aggressive approach
# Find blocks that contain schedule-related class names
lines = css.split('\n')
new_lines = []
skip_block = False
brace_depth = 0
removed_count = 0

schedule_markers = [
    'btn-open-schedule-panel', 'schedule-panel', 'schedule-title',
    'schedule-badge', 'schedule-tree', 'act-focus-pulse', 'act-pulse',
    'sch-tree', 'sch-badge', 'sch-act', 'floating-trigger-group'
]

i = 0
while i < len(lines):
    line = lines[i]
    
    # Check if this line starts a schedule-related CSS block
    is_schedule_line = any(marker in line for marker in schedule_markers)
    
    if is_schedule_line and not skip_block:
        skip_block = True
        brace_depth = 0
        removed_count += 1
    
    if skip_block:
        brace_depth += line.count('{') - line.count('}')
        if brace_depth <= 0 and '{' in ''.join(lines[max(0,i-5):i+1]):
            skip_block = False
            brace_depth = 0
            i += 1
            continue
    else:
        new_lines.append(line)
    
    i += 1

new_css = '\n'.join(new_lines)

# Also handle @keyframes act-pulse
new_css = re.sub(r'@keyframes\s+act-pulse\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}', '', new_css)

# Clean up excessive blank lines
new_css = re.sub(r'\n{4,}', '\n\n\n', new_css)

text = text[:style_start] + new_css + text[style_end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"✓ Removed {removed_count} schedule CSS blocks")
print(f"✅ File size: {len(text)} bytes")

# Verify
remaining = sum(1 for m in schedule_markers if m in text)
print(f"  Schedule markers still in file: {remaining}")
