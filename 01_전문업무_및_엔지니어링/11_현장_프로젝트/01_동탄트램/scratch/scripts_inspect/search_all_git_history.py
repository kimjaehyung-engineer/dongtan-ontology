import subprocess

res = subprocess.run(['git', 'log', '--all', '--name-only', '--oneline'], capture_output=True, text=True, encoding='utf-8', errors='ignore')

print("=== Searching for time-chainage or App.jsx in git history ===")
matches = []
current_commit = ""
for line in res.stdout.splitlines():
    if len(line) > 7 and line[7] == ' ':
        current_commit = line[:7]
    elif 'chainage' in line.lower() or 'time-chainage' in line.lower() or 'mvp' in line.lower():
        matches.append(f"{current_commit}: {line}")

print(f"Total matching files in history: {len(matches)}")
for m in matches[:30]:
    print(m)
