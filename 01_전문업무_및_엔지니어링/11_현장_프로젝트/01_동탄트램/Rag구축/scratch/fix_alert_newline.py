# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Replace the alert line with a single clean string
old_alert = 'alert("상위 폴더가 설정되었습니다:\n" + data.docs_root_path);'
# In text, it might have literal newline:
bad_alert_re = r'alert\("상위 폴더가 설정되었습니다:[\r\n]+" \+ data\.docs_root_path\);'

import re
text = re.sub(bad_alert_re, 'alert("상위 폴더가 설정되었습니다: " + data.docs_root_path);', text)

with open(server_path, "w", encoding="utf-8") as f:
    f.write(text)

# Extract and test
idx1 = text.find('<script>')
idx2 = text.rfind('</script>')
script_body = text[idx1+8:idx2]
with open("scratch/test_verify.js", "w", encoding="utf-8") as f:
    f.write(script_body)

r = subprocess.run(["node", "--check", "scratch/test_verify.js"], capture_output=True, text=True, encoding="utf-8")
if r.returncode != 0:
    print("[ERROR] Node check still failing:", r.stderr)
else:
    print("[SUCCESS] NODE CHECK PASSED PERFECTLY!")
