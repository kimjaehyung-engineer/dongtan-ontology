import os
from bs4 import BeautifulSoup

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램"
sim_path = os.path.join(base_dir, "08.메뉴얼 및 평면도", "트램_검수고_디지털관제.html")
output_path = os.path.join(base_dir, "scratch", "depot_sim_structure.txt")

with open(sim_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

body_content = str(soup.body) if soup.body else "No body"
head_styles = [str(style) for style in soup.find_all('style')]
scripts = [str(script) for script in soup.find_all('script')]

with open(output_path, 'w', encoding='utf-8') as out:
    out.write("=== STYLES ===\n")
    for s in head_styles:
        out.write(s + "\n")
    out.write("\n=== BODY ===\n")
    out.write(body_content[:5000] + "... (truncated)\n")
    out.write("\n=== SCRIPTS ===\n")
    for scr in scripts:
        out.write(scr[:2000] + "... (truncated)\n\n")

print("Depot simulator structure written successfully.")
