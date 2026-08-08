import os, sys

sys.stdout.reconfigure(encoding='utf-8')

search_roots = [
    r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램',
    r'C:\Users\sskjh\.gemini',
    r'C:\$Recycle.Bin'
]

keywords = ['전기', '통신', '전력', '변전', '배전', '급전', 'LTE', '광케이블', '방송', 'CCTV']

print("=== Searching for Electric & Telecom HTML files across system ===")

matches = []

for sroot in search_roots:
    if not os.path.exists(sroot):
        continue
    print(f"\nScanning: {sroot}...")
    for root, dirs, files in os.walk(sroot):
        if 'node_modules' in root or '.git' in root:
            continue
        for f in files:
            if f.endswith('.html') or f.endswith('.htm'):
                full_path = os.path.join(root, f)
                # Check if path or filename contains electric/telecom keywords
                if any(k in full_path for k in keywords):
                    matches.append((full_path, os.path.getmtime(full_path)))

print(f"\nFound {len(matches)} matching HTML files for Electric & Telecom!")
matches.sort(key=lambda x: x[1], reverse=True)

for p, mtime in matches[:50]:
    import datetime
    dt_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{dt_str}] {p}")
