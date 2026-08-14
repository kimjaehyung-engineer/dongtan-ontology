import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Find the script block
script_start = text.find('<script>')
script_end = text.find('</script>')
js_block = text[script_start+8:script_end]
print(f"JS block size: {len(js_block)} chars")

# 2. Check for activitiesDatabase and look for JSON parsing issues
act_db_idx = js_block.find('const activitiesDatabase')
if act_db_idx != -1:
    # Find end of JSON array
    bracket_start = js_block.find('[', act_db_idx)
    depth = 0
    end_pos = bracket_start
    for i in range(bracket_start, min(bracket_start + 200000, len(js_block))):
        if js_block[i] == '[':
            depth += 1
        elif js_block[i] == ']':
            depth -= 1
            if depth == 0:
                end_pos = i
                break
    
    json_str = js_block[bracket_start:end_pos+1]
    print(f"activitiesDatabase JSON size: {len(json_str)} chars")
    
    # Check what comes after the JSON
    after_json = js_block[end_pos+1:end_pos+100]
    print(f"After JSON: '{after_json[:80]}'")
    
    # Check if there's a semicolon
    if ';' in after_json[:5]:
        print("  ✓ Semicolon found after JSON array")
    else:
        print("  !! No semicolon after JSON array !!")
else:
    print("!! activitiesDatabase NOT FOUND in JS block !!")

# 3. Look for any syntax errors - unmatched braces in JS
open_braces = js_block.count('{')
close_braces = js_block.count('}')
print(f"\nJS braces: open={open_braces}, close={close_braces}")
if open_braces != close_braces:
    print(f"  !! MISMATCH: difference = {open_braces - close_braces} !!")

# 4. Count DOMContentLoaded instances
dom_count = js_block.count('DOMContentLoaded')
print(f"\nDOMContentLoaded instances in JS: {dom_count}")

# 5. Check if layer toggle code runs before or after activitiesDatabase
toggle_bg_idx = js_block.find('"toggle-bg"')
print(f"\ntoggle-bg listener at JS position: {toggle_bg_idx}")
print(f"activitiesDatabase at JS position: {act_db_idx}")
if act_db_idx < toggle_bg_idx:
    print("  -> activitiesDatabase is BEFORE toggle listeners (potential blocker if JSON fails)")
else:
    print("  -> activitiesDatabase is AFTER toggle listeners (safe)")

# 6. Check theme toggling code
theme_idx = js_block.find('v1-theme')
if theme_idx != -1:
    print(f"\n=== Theme toggle code ===")
    print(js_block[theme_idx-200:theme_idx+400])
