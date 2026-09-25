import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

server_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
text = server_file.read_text(encoding='utf-8')

# Let's inspect the entire HTML_TEMPLATE as Python evaluates it!
# How does Python evaluate HTML_TEMPLATE?
# We can import or exec or extract the string from server.py!
d = {}
exec("from pathlib import Path\nDOCS_DIR = Path('.')\nMETA_INDEX_FILE = Path('.')\nPORT=8080\n" + text[:text.find('class SiteRAGHandler')], d)
rendered_html = d.get('HTML_TEMPLATE', '')
print(f"Evaluated HTML_TEMPLATE length: {len(rendered_html)}")

# Extract script tag
m = re.search(r'<script>\s*let activeDoc =[\s\S]*?</script>', rendered_html, re.IGNORECASE)
if m:
    script = m.group(0)[8:-9]
    print(f"Main script extracted, length: {len(script)}")
    with open('scratch/evaluated_main_script.js', 'w', encoding='utf-8') as f:
        f.write(script)
    print("Wrote scratch/evaluated_main_script.js")
else:
    print("Could not find main script tag in evaluated HTML!")
