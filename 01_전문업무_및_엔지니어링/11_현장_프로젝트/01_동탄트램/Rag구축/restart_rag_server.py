import os
import subprocess
import time
import urllib.request

rag_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG"
log_file = os.path.join(rag_dir, "server.log")

# 1. Kill any process listening on 8080
res = subprocess.run("netstat -ano | findstr :8080", shell=True, capture_output=True, text=True)
pids = set()
for line in res.stdout.strip().split("\n"):
    parts = line.strip().split()
    if len(parts) >= 5 and "LISTENING" in line:
        pids.add(parts[-1])

for pid in pids:
    print(f"Terminating PID {pid} on port 8080...")
    subprocess.run(f"taskkill /F /PID {pid}", shell=True, capture_output=True)

time.sleep(1)

# 2. Launch server.py detached with output to server.log
py314_exe = r"C:\Users\sskjh\AppData\Local\Programs\Python\Python314\python.exe"
python_bin = py314_exe if os.path.exists(py314_exe) else "python"
with open(log_file, "a", encoding="utf-8") as f_log:
    p = subprocess.Popen(
        [python_bin, "server.py"],
        cwd=rag_dir,
        stdout=f_log,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.DETACHED_PROCESS if os.name == "nt" else 0
    )
print(f"Started server.py with PID {p.pid} using {python_bin}")

time.sleep(2)

# 3. Check health
try:
    with urllib.request.urlopen("http://127.0.0.1:8080/", timeout=5) as resp:
        print(f"Server is LIVE! Status code: {resp.status}")
except Exception as e:
    print(f"Server connection test failed: {e}")
