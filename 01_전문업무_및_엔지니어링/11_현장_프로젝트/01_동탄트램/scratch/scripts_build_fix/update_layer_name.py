import sys
import os
import glob

sys.stdout.reconfigure(encoding='utf-8')

# Target V1 HTML file
search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]
print("Updating layer item label in V1 HTML:", file_v1)

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

if "정거장 노드 마커" in content:
    content = content.replace("정거장 노드 마커", "정거장 노드")
    print("Successfully replaced '정거장 노드 마커' with '정거장 노드'!")

with open(file_v1, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished updating layer name in V1 HTML!")
