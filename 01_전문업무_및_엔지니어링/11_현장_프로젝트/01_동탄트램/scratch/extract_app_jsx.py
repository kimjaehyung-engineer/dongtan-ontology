import subprocess, os

commit = 'c896b9c'
rel_path = '01_전문업무_및_엔지니어링/동탄트램/09.공정표/time-chainage-mvp/src/App.jsx'

cmd = f'git show {commit}:"{rel_path}"'
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', shell=True)

if res.returncode == 0 and len(res.stdout) > 0:
    print(f"Successfully extracted App.jsx ({len(res.stdout)} chars)")
    out_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src'
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'App.jsx'), 'w', encoding='utf-8') as f:
        f.write(res.stdout)
    print("Saved to 09.공정표/src/App.jsx")
else:
    print("Failed to extract:", res.stderr)
