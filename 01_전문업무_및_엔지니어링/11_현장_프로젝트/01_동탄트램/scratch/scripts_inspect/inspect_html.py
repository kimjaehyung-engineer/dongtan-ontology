with open("동탄트램_업무_매뉴얼.html", "r", encoding="utf-8") as f:
    content = f.read()

print(f"Length of 동탄트램_업무_매뉴얼.html: {len(content)}")
# Print first 20 lines that contain <section or h1 or h2
import re
sections = re.findall(r'<section[^>]*id="[^"]+"[^>]*>|<h[12][^>]*>.*?</h[12]>', content)
print("Found sections/headings:")
for s in sections[:30]:
    print(s)
