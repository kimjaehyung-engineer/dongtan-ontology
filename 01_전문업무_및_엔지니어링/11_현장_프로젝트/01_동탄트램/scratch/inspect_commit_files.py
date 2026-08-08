import subprocess

res = subprocess.run(['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
print("=== Files in current HEAD commit ===")
lines = res.stdout.splitlines()
print(f"Total files in commit: {len(lines)}")
for f in lines[:20]:
    print("  -", f)

# Check if any .exe or node_modules remain in git tracking
res_all = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
large_tracked = [f for f in res_all.stdout.splitlines() if f.endswith(('.exe', '.zip', '.asar', '.pak')) or 'node_modules' in f]
print(f"\nLarge tracked files in git index: {len(large_tracked)}")
for f in large_tracked[:10]:
    print("  !! Tracked large file:", f)
