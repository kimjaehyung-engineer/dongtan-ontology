import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect what happens in /api/chat when routing the query "동탄역 핵심이슈는 머지?"
# Specifically, what document was selected, what pages were extracted, and what error each model returned!
lines = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py").read_text(encoding='utf-8').splitlines()

# Let's see lines 3700-3840 to understand how target_doc and pdf_bytes are obtained
for i in range(3700, 3760):
    print(f"{i+1:4d}: {lines[i]}")
