# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

server_path = r'C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py'
with open(server_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for idx in range(1950, min(len(lines), 2000)):
    print(f"{idx+1:4d}: {lines[idx]}", end='')
