import os
import sys
import subprocess
import time

rag_dir = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG"
log_file = os.path.join(rag_dir, "telegram_bot.log")

# 1. Kill any existing telegram_bot process
try:
    res = subprocess.run(
        'wmic process where "commandline like \'%telegram_bot.py%\' and name like \'%python%\'" get processid',
        shell=True, capture_output=True, text=True
    )
    for line in res.stdout.strip().split("\n"):
        line = line.strip()
        if line.isdigit():
            print(f"Stopping existing telegram_bot process PID {line}...")
            subprocess.run(f"taskkill /F /PID {line}", shell=True, capture_output=True)
except Exception:
    pass

time.sleep(1)

# 2. Launch telegram_bot.py detached
py_bin = sys.executable

with open(log_file, "a", encoding="utf-8") as f_log:
    p = subprocess.Popen(
        [py_bin, "-u", "telegram_bot.py"],
        cwd=rag_dir,
        stdout=f_log,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.DETACHED_PROCESS if os.name == "nt" else 0
    )

print(f"Telegram Bot started successfully! PID: {p.pid}")
print(f"Logs: {log_file}")
