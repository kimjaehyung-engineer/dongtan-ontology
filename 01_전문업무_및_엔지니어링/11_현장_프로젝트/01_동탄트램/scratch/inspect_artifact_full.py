import os
from bs4 import BeautifulSoup

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램"
artifact_file = os.path.join(base_dir, "08.메뉴얼 및 평면도", "code_artifact (1).html")
output_path = r"scratch\artifact_components.txt"

with open(artifact_file, 'r', encoding='utf-8') as f:
    text = f.read()

soup = BeautifulSoup(text, 'html.parser')

with open(output_path, "w", encoding="utf-8") as out:
    out.write("=== HEAD TAILS / STYLES / SCRIPTS ===\n")
    for s in soup.find_all('script'):
        out.write("SCRIPT SRC: " + str(s.get('src')) + "\n")
        if s.string:
            out.write(s.string[:500] + "\n...\n")
            
    out.write("\n=== BODY CONTENT SUMMARY ===\n")
    body = soup.find('body')
    if body:
        out.write(body.prettify()[:5000])

print("Extracted artifact components.")
