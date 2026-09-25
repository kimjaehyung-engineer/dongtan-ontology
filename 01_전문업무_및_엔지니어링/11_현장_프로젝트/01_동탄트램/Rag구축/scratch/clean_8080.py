import subprocess

res = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
pids_to_kill = set()
for line in res.stdout.splitlines():
    if ":8080" in line and "LISTENING" in line:
        parts = line.strip().split()
        pid = parts[-1]
        pids_to_kill.add(pid)

print("Found PIDs on 8080:", pids_to_kill)
for pid in pids_to_kill:
    print(f"Killing PID {pid}...")
    subprocess.run(["taskkill", "/F", "/PID", pid])
print("Cleanup done.")
