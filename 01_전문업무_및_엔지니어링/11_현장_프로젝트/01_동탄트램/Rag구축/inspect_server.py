# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

server_path = r'C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py'
with open(server_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'id="fileInput"' in line or 'async function uploadDoc' in line:
        print(f'L{idx+1}: {line.strip()[:100]}')
        for j in range(max(0, idx-5), min(len(lines), idx+30)):
            print(f'  {j+1:4d}: {lines[j]}', end='')
        print('\n' + '='*50)
