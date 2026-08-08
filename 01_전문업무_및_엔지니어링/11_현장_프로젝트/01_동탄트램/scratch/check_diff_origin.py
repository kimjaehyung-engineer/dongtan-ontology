import subprocess

res = subprocess.run(['git', 'diff', '--name-only', 'origin/main..main'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
lines = res.stdout.splitlines()
print(f"=== Files in unpushed commit (Total: {len(lines)}) ===")
for f in lines:
    print("  -", f)
