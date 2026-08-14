import os

dist_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist'
assets_dir = os.path.join(dist_dir, 'assets')

for f in os.listdir(assets_dir):
    fpath = os.path.join(assets_dir, f)
    print(f"File: {f} (size: {os.path.getsize(fpath)} bytes)")
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
        snippet = fp.read(300)
        print(f"  Snippet: {snippet[:150]}...")
