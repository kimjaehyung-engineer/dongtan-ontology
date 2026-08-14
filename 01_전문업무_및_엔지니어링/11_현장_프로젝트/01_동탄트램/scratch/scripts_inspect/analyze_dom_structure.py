import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print(f"File size: {len(text)} bytes")

# Find the first DOMContentLoaded
dom_idx = text.find('DOMContentLoaded')
if dom_idx != -1:
    # Show context
    print("\n=== DOMContentLoaded context ===")
    print(text[dom_idx-100:dom_idx+600])
else:
    print("!! No DOMContentLoaded found")

# Find end of the DOMContentLoaded block
# It starts with addEventListener("DOMContentLoaded", () => { 
# and ends with }); at the matching brace level
dom_full_start = text.rfind('addEventListener', max(0, dom_idx - 50), dom_idx + 1)
brace_start = text.find('{', dom_idx)
depth = 0
i = brace_start
dom_end = -1
while i < len(text):
    if text[i] == '{':
        depth += 1
    elif text[i] == '}':
        depth -= 1
        if depth == 0:
            dom_end = i
            break
    i += 1

print(f"\nDOMContentLoaded block: chars {dom_full_start} to {dom_end}")
print(f"Content: {text[dom_full_start:dom_end+5]}")

# Check what code comes after DOMContentLoaded  
after_dom = text[dom_end:dom_end+500]
print(f"\n=== After DOMContentLoaded block ===")
print(after_dom)

# Find </script> position
script_end = text.find('</script>')
print(f"\n</script> at position: {script_end}")
print(f"Code between DOMContentLoaded end and </script>: {script_end - dom_end} chars")
if script_end - dom_end > 0:
    remaining_js = text[dom_end+3:script_end]
    print(f"Remaining JS: {remaining_js[:500]}")
