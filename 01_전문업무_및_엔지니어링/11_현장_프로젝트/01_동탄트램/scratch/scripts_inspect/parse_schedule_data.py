import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

js_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\assets\index-no5s-_SR.js'

with open(js_path, 'r', encoding='utf-8') as f:
    text = f.read()

print(f"JS Bundle size: {len(text)} bytes")

# Search for JSON or object arrays in JS bundle
# Let's search for keywords like 'gantt', 'chainage', 'activity', 'startSta', '1공구', '2공구', '일반부지', '트램부지', '공정', 'WBS'
keywords = ['1공구', '2공구', '일반부지', '트램부지', '정거장', '공사', '공정', '월', '개월', 'STA']
for kw in keywords:
    count = text.count(kw)
    print(f"  Keyword '{kw}': {count} occurrences")

# Find strings matching JSON-like activity objects
matches = re.findall(r'\{[^{}]*?"name"[^{}]*?\}', text)
print(f"\nFound {len(matches)} objects with 'name' property")
for m in matches[:10]:
    print("  ", m[:150])
