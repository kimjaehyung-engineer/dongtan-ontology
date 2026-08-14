import re

path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\동탄트램_노선평면도V1.html"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to catch the specific broken syntax
pattern = re.compile(r"\};\)[^\"]+도입\"\s*\],\s*rfp:", re.MULTILINE | re.DOTALL)
replacement = r"""  },
  "동탄역_특화": {
    issues: [
      "스카이브릿지(E/V, E/S 포함) 도입"
    ],
    rfp:"""

new_content = pattern.sub(replacement, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Replacement successful:", new_content != content)
