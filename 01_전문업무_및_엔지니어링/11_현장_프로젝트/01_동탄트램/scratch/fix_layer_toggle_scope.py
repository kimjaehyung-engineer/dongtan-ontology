import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Strategy: Move the entire layer toggle + theme toggle block INSIDE the first DOMContentLoaded handler.
# The old code is at top-level. We'll:
# 1. Remove the old top-level block  
# 2. Insert it inside the first DOMContentLoaded right after renderInteractiveElements()

# Find the old block: starts at "// Layers toggling" and ends before next function def or DOMContentLoaded
old_block_start = text.find('// Layers toggling\n')
if old_block_start == -1:
    print("!! Could not find '// Layers toggling' block")
    sys.exit(1)

# Find end of old block - it goes through theme toggle and font size code, ending at the first DOMContentLoaded
first_dom = text.find('document.addEventListener("DOMContentLoaded"', old_block_start)
old_block = text[old_block_start:first_dom]
print(f"Found old toggle block: {len(old_block)} chars")
print(f"Last 200 chars of old block: {old_block[-200:]}")

# Remove old block from its current location
text = text[:old_block_start] + text[first_dom:]
print("✓ Removed old toggle block from top-level scope")

# Now insert it INSIDE the first DOMContentLoaded, right after renderInteractiveElements();
insert_anchor = 'renderInteractiveElements();\n'
insert_idx = text.find(insert_anchor)
if insert_idx != -1:
    insert_pos = insert_idx + len(insert_anchor)
    # Wrap the old block content
    wrapped_block = '\n  // === Layer & Theme Toggle Listeners (inside DOMContentLoaded) ===\n' + old_block
    text = text[:insert_pos] + wrapped_block + text[insert_pos:]
    print("✓ Inserted toggle block inside first DOMContentLoaded")
else:
    print("!! Could not find renderInteractiveElements() anchor")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"\n✅ Layer toggle fix applied! File size: {len(text)} bytes")
