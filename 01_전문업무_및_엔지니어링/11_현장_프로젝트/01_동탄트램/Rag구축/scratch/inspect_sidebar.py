import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

server_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
text = server_file.read_text(encoding='utf-8')

sb_start = text.find('<div class="sidebar">')
sb_end = text.find('<div class="main">', sb_start)
print("=== SIDEBAR HTML ===")
print(text[sb_start:sb_end])
