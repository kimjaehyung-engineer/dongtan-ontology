import sys
sys.stdout.reconfigure(encoding='utf-8')

f_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(f_path, 'r', encoding='utf-8') as f:
    text = f.read()

print(f"File Size: {len(text)} bytes")

import re
matches = re.findall(r'<script[\s\S]*?</script>', text)
print(f"Total script tags: {len(matches)}")

# Print initial data structures in script
if matches:
    first_script = matches[0]
    print("\nScript Preview (first 1000 chars):")
    print(first_script[:1000])
