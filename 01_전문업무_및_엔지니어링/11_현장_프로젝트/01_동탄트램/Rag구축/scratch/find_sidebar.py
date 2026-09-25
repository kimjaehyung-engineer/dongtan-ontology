import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

server_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
text = server_file.read_text(encoding='utf-8')

print("Length of server.py:", len(text))
pos = 0
while True:
    p = text.find('sidebar', pos)
    if p == -1: break
    print(f"Found 'sidebar' at {p}: {repr(text[p-20:p+50])}")
    pos = p + 20
    if pos > p + 1000: break
