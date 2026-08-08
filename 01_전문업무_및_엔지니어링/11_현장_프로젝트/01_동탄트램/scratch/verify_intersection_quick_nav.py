import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

print("HTML size:", len(text))
print("Contains intersection-quick-nav HTML:", 'id="intersection-quick-nav"' in text)
print("Contains intersectionQuickNav JS logic:", 'intersectionQuickNav.innerHTML' in text)
print("Contains event listener:", 'intersectionQuickNavEl.addEventListener' in text)

# Print snippet from header
m = re.search(r'<header[^>]*>(.*?)</header>', text, re.DOTALL)
if m:
    print("\n=== HEADER HTML SNIPPET ===")
    print(m.group(0))

# Print snippet from quickNav listener
idx = text.find('intersectionQuickNavEl.addEventListener')
if idx != -1:
    print("\n=== LISTENER JS SNIPPET ===")
    print(text[idx-100:idx+300])
