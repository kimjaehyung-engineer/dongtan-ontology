import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

pattern = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\**\지장물이설\**\*발주전략*KOM*(도급지분)*"
dirs = glob.glob(pattern, recursive=True)

if dirs:
    d = dirs[0]
    for sub in ['표준서', '수행지침', '체크리스트']:
        sub_dir = os.path.join(d, sub)
        if os.path.exists(sub_dir):
            files = os.listdir(sub_dir)
            if files:
                fp = os.path.join(sub_dir, files[0])
                print(f"=== PATH: {fp} ===")
                with open(fp, 'r', encoding='utf-8') as f:
                    print(f.read())
                print("\n" + "="*50 + "\n")
