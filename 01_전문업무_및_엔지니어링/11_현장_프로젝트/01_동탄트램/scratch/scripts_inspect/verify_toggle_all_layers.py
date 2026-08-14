import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Check HTML
has_btn = 'id="btn-toggle-all-layers"' in text
# Check CSS
has_css = '.btn-layer-all' in text
# Check JS
has_js = 'const btnToggleAll = document.getElementById("btn-toggle-all-layers");' in text

print("=== VERIFICATION ===")
print(f"  Button HTML: {has_btn}")
print(f"  Button CSS:  {has_css}")
print(f"  Button JS:   {has_js}")

# Check JS syntax/braces balance
script_start = text.find('<script>')
script_end = text.find('</script>')
js_block = text[script_start+8:script_end]
open_b = js_block.count('{')
close_b = js_block.count('}')
print(f"  JS brace match: {open_b == close_b} (open={open_b}, close={close_b})")

if has_btn and has_css and has_js and open_b == close_b:
    print("\n✅ ALL TOGGLE ALL LAYER CHECKS PASSED!")
else:
    print("\n❌ VERIFICATION FAILED!")
