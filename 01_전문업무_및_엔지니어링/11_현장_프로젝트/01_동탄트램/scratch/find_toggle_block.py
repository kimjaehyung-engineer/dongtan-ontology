import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Find the exact layer toggle block and wrap it in DOMContentLoaded-safe code
# The toggle code is at top-level scope BEFORE the first DOMContentLoaded

old_toggle_block = """// Layers toggling
document.getElementById("toggle-bg").addEventListener("change", (e) => {
  document.getElementById("bg-map").style.display = e.target.checked ? "block" : "none";
});
document.getElementById("toggle-routes").addEventListener("change", (e) => {
  document.getElementById("routes-group").style.display = e.target.checked ? "block" : "none";
});
document.getElementById("toggle-nodes").addEventListener("change", (e) => {
  document.getElementById("nodes-group").style.display = e.target.checked ? "block" : "none";
});
document.getElementById("toggle-labels").addEventListener("change", (e) => {
  document.getElementById("labels-group").style.display = e.target.checked ? "block" : "none";
});
document.getElementById("toggle-distances").addEventListener("change", (e) => {
  document.getElementById("distances-group").style.display = e.target.checked ? "block" : "none";
});
document.getElementById("toggle-turnouts").addEventListener("change", (e) => {
  document.getElementById("turnouts-group").style.display = e.target.checked ? "block" : "none";
});"""

# Check if there's intersection and construction toggle code too
idx = text.find(old_toggle_block)
if idx != -1:
    # Get more text after this block
    after = text[idx + len(old_toggle_block):idx + len(old_toggle_block) + 800]
    print("=== After toggle block ===")
    print(after)
else:
    print("!! Could not find exact toggle block. Searching for partial match...")
    partial_idx = text.find('// Layers toggling')
    if partial_idx != -1:
        print(text[partial_idx:partial_idx+1500])
