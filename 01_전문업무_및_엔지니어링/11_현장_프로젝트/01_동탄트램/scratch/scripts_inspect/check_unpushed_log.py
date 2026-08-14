import subprocess

res = subprocess.run(['git', 'log', 'origin/main..main', '--oneline'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
print("=== Unpushed commits in local branch ===")
print(res.stdout)
