import os, zipfile, re, sys

sys.stdout.reconfigure(encoding='utf-8')

search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'

target_file = None
for root, dirs, files in os.walk(search_dir):
    for f in files:
        if 'v7.xlsm' in f and 'BODY' in f and not f.startswith('~$'):
            target_file = os.path.join(root, f)
            break
    if target_file:
        break

print(f"Target File: {target_file}")

if target_file and os.path.exists(target_file):
    v6_matches = 0
    plain_matches = 0

    with zipfile.ZipFile(target_file, 'r') as z:
        for name in z.namelist():
            content = z.read(name).decode('utf-8', errors='ignore')
            if '첨부폴더' in content:
                v6_cnt = content.count('매뉴얼BODY(집행단계-첨부폴더)v6')
                plain_cnt = content.count('매뉴얼BODY(집행단계-첨부폴더)') - v6_cnt
                print(f"Found in {name}: v6={v6_cnt}, plain={plain_cnt}")
                v6_matches += v6_cnt
                plain_matches += plain_cnt
                
                urls = re.findall(r'Target="([^"]*첨부폴더[^"]*)"', content)
                for u in urls[:5]:
                    print("  Sample Target URL:", u)
                
                cell_refs = re.findall(r'[^"]*첨부폴더[^"]*', content)
                for cr in cell_refs[:5]:
                    if 'Target=' not in cr:
                        print("  Sample Cell Text:", cr[:100])

    print(f"\nTOTAL MATCHES in v7.xlsm:")
    print(f"  - 매뉴얼BODY(집행단계-첨부폴더)v6 : {v6_matches} 건")
    print(f"  - 매뉴얼BODY(집행단계-첨부폴더)   : {plain_matches} 건")
