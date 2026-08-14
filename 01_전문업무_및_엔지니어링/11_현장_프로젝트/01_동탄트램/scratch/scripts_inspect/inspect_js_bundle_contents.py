import sys, re
sys.stdout.reconfigure(encoding='utf-8')

js_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\assets\index-no5s-_SR.js'

with open(js_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Find Korean strings in JS bundle
korean_strings = re.findall(r'[\uac00-\ud7a3]{2,}', text)
print(f"Total Korean strings found in bundle: {len(korean_strings)}")

# Print unique Korean terms
unique_terms = sorted(list(set(korean_strings)))
print("\nSample Korean terms in bundle:")
for t in unique_terms[:50]:
    print(f"  {t}")
