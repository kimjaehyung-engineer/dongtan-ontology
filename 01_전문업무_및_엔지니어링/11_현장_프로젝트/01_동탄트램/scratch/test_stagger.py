import sys
import os
import glob
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\intersections_segments.json', 'r', encoding='utf-8') as f:
    intersections = json.load(f)

search_dir = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램'
files = glob.glob(os.path.join(search_dir, '**', '*노선평면도V1.html'), recursive=True)
file_v1 = files[0]

with open(file_v1, 'r', encoding='utf-8') as f:
    content = f.read()

print("File V1 loaded. Intersections count:", len(intersections))

# Test staggering algorithm
for i in range(10):
    item = intersections[i]
    dx = item['x2'] - item['x1']
    dy = item['y2'] - item['y1']
    length = (dx*dx + dy*dy)**0.5 or 1.0
    
    # Perpendicular unit vector
    px = -dy / length
    py = dx / length
    
    # Alternate offset side (+15px or -15px)
    offset_dist = 16 if (i % 2 == 0) else -16
    lx = item['x'] + px * offset_dist
    ly = item['y'] + py * offset_dist
    
    print(f"#{item['no']:2d} {item['name']:22s} | Track (x:{item['x']:5.1f}, y:{item['y']:5.1f}) => Badge (x:{lx:5.1f}, y:{ly:5.1f}) | Offset: {offset_dist:+3d}px")
