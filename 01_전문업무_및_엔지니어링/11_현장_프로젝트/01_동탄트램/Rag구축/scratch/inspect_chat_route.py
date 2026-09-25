# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

p = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
text = p.read_text(encoding="utf-8")

marker = 'elif self.path == "/api/chat":'
idx = text.find(marker)
print(f"Marker found at {idx}")
print(text[idx:idx+2500])
