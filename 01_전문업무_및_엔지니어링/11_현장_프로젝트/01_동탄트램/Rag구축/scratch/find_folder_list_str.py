import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

server_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
text = server_file.read_text(encoding='utf-8')

pos = text.find('folderListStr')
if pos != -1:
    print("Found folderListStr at", pos)
    print(text[pos-100:pos+300])
else:
    print("folderListStr NOT found")
