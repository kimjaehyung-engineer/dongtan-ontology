import subprocess, os

commit = '4b92153'
files = [
    '01_전문업무_및_엔지니어링/동탄트램/09.공정표/time-chainage-mvp/src/index.css',
]

out_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src'
os.makedirs(out_dir, exist_ok=True)

for rel_path in files:
    cmd = f'git show {commit}:"{rel_path}"'
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', shell=True)
    if res.returncode == 0:
        fname = os.path.basename(rel_path)
        with open(os.path.join(out_dir, fname), 'w', encoding='utf-8') as f:
            f.write(res.stdout)
        print(f"Extracted {fname} ({len(res.stdout)} chars)")
