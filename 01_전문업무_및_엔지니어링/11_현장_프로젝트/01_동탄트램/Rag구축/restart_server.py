# -*- coding: utf-8 -*-
import subprocess, time, os, signal

out = subprocess.check_output('netstat -ano | findstr :8080', shell=True).decode()
pids = set()
for line in out.strip().split('\n'):
    parts = line.strip().split()
    if len(parts) >= 5 and 'LISTENING' in parts:
        pids.add(int(parts[-1]))

for pid in pids:
    try:
        os.kill(pid, signal.SIGTERM)
        print('Killed PID:', pid)
    except:
        pass

time.sleep(1)

rag_dir = r'C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG'
bat_file = os.path.join(rag_dir, 'run_server.bat')
cmd = f"Start-Process -FilePath '{bat_file}' -WorkingDirectory '{rag_dir}'"
subprocess.run(['powershell', '-Command', cmd])
print('Restarted server successfully!')
