# -*- coding: utf-8 -*-
from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Replace line 2148
old_line = 'alert("상위 폴더가 설정되었습니다:\n" + data.docs_root_path);'
new_line = 'alert("상위 폴더가 설정되었습니다: " + data.docs_root_path);'

if old_line in text:
    text = text.replace(old_line, new_line, 1)
    print("[OK] Replaced old_line directly")
else:
    # Try replacing any alert with docs_root_path
    import re
    text = re.sub(r'alert\("상위 폴더가 설정되었습니다:[^\"]*"\s*\+\s*data\.docs_root_path\);', new_line, text)
    print("[OK] Replaced with regex")

with open(server_path, "w", encoding="utf-8") as f:
    f.write(text)

# Now verify the HTML rendered by Python by importing or loading HTML_TEMPLATE
import server
html = server.HTML_TEMPLATE
idx1 = html.find('<script>')
idx2 = html.rfind('</script>')
script_body = html[idx1+8:idx2]

with open("scratch/rendered_live_script.js", "w", encoding="utf-8") as f:
    f.write(script_body)

import subprocess
r = subprocess.run(["node", "--check", "scratch/rendered_live_script.js"], capture_output=True, text=True, encoding="utf-8")
if r.returncode != 0:
    print("[ERROR] Node check failed on rendered HTML_TEMPLATE:\n", r.stderr)
else:
    print("[SUCCESS] NODE CHECK PASSED ON RENDERED HTML_TEMPLATE WITH ZERO ERRORS!")
