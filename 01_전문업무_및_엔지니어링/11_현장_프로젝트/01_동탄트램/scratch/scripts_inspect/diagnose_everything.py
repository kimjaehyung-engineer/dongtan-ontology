import sys
import subprocess
import os

sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(f_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

print("File size:", len(html_content))

# Extract script blocks and test Node.js execution
import re
scripts = re.findall(r'<script[\s\S]*?</script>', html_content)
print(f"Found {len(scripts)} script blocks.")

# Test Node.js execution on JS code to find runtime errors or missing variables
js_code = ""
for s in scripts:
    s_clean = s.replace('<script>', '').replace('</script>', '')
    js_code += s_clean + "\n"

# Write JS to scratch file for node evaluation
scratch_js = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\test_full_dashboard.js'

# Mock DOM objects for Node.js environment test
mock_dom = """
global.window = { innerWidth: 1400, innerHeight: 900, print: () => {}, addEventListener: () => {} };
global.document = {
  getElementById: (id) => ({
    classList: { add: () => {}, remove: () => {} },
    setAttribute: () => {},
    style: {},
    appendChild: () => {},
    innerHTML: '',
    getBoundingClientRect: () => ({ width: 1200, height: 800, left: 0, top: 0 }),
    querySelectorAll: () => []
  }),
  querySelector: () => ({
    classList: { add: () => {}, remove: () => {} },
    style: {},
    getBoundingClientRect: () => ({ width: 1200, height: 800, left: 0, top: 0 })
  }),
  querySelectorAll: () => [],
  createElementNS: () => ({ setAttribute: () => {} }),
  addEventListener: () => {}
};
"""

with open(scratch_js, 'w', encoding='utf-8') as f:
    f.write(mock_dom + "\n" + js_code + "\nconsole.log('NODE_EVAL_SUCCESS');")

res = subprocess.run(['node', scratch_js], capture_output=True, text=True, encoding='utf-8')
print("--- NODE JS EVALUATION OUTPUT ---")
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
