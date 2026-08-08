import os

target_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(target_html, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print(f"HTML file length: {len(text)} chars")
# Find </script> position
script_end = text.find('</script>', 100000)
if script_end != -1:
    print("\n=== Last 300 chars inside <script type='module'> ===")
    print(text[script_end-300:script_end])
else:
    print("!! </script> not found")
