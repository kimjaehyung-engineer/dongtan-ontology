# -*- coding: utf-8 -*-
server_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'filename = headers.split(b\'filename="\')' in l:
        lines[i] = '                        filename = headers.split(b\'filename="\')[1].split(b\'"\')[0].decode(\'utf-8\', errors=\'ignore\')\n'
        print(f"Fixed line {i+1} indentation!")
        break

with open(server_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Saved corrected server.py")
