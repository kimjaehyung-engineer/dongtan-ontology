import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Search path safely using glob
pattern = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\**\지장물이설\**\*발주전략*KOM*(도급지분)*"
dirs = glob.glob(pattern, recursive=True)

if not dirs:
    print("No directory found.")
    sys.exit(0)

target_dir = dirs[0]
print(f"Target Directory: {target_dir}\n")

# List files inside target_dir
for root, _, files in os.walk(target_dir):
    for f in files:
        if f.endswith('.html'):
            fp = os.path.join(root, f)
            print(f"=== File: {f} ===")
            with open(fp, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                # Print first 50 lines to see structure and format
                print("".join(lines[:60]))
                print("...\n")
