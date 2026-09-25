import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

server_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
text = server_file.read_text(encoding='utf-8')

import re
matches = [m.start() for m in re.finditer(r'<script', text, re.IGNORECASE)]
print(f"Found {len(matches)} <script> tags at indices: {matches}")
for i, m in enumerate(matches):
    print(f"--- Script {i} (pos {m}) ---")
    print(text[m:m+200])
