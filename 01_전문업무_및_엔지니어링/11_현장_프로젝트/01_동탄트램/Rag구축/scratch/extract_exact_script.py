import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

server_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
text = server_file.read_text(encoding='utf-8')

script_start = text.find('<script>\n    let activeDoc = "";')
if script_start == -1:
    script_start = text.find('<script>')
script_end = text.find('</script>', script_start)

script_text = text[script_start+8:script_end]
print(f"Script length: {len(script_text)}")

# Let's write the exact script text as sent by the server to a file and run node --check
with open('scratch/exact_server_script.js', 'w', encoding='utf-8') as f:
    f.write(script_text)

print("Wrote scratch/exact_server_script.js")
