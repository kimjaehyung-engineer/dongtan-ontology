import subprocess

res = subprocess.run(['git', 'log', '--all', '--name-only', '--oneline', '--', '09.공정표'], capture_output=True, text=True, encoding='utf-8', errors='ignore')

print("=== Git History for 09.공정표 ===")
lines = res.stdout.splitlines()
print(f"Total lines: {len(lines)}")
for line in lines[:100]:
    print(line)
