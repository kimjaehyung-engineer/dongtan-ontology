import sys
import os
import glob
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\intersections_segments.json', 'r', encoding='utf-8') as f:
    intersections = json.load(f)

print("Checking 1공구 #30 ~ #40 intersections:")
for item in intersections:
    if item['tool'] == '1공구' and 30 <= item['no'] <= 40:
        dx = item['x2'] - item['x1']
        dy = item['y2'] - item['y1']
        dist_px = (dx*dx + dy*dy)**0.5
        print(f"1공구 #{item['no']:2d} | {item['name']:25s} | STA: {item['startSta']}~{item['endSta']}m ({item['length']}m) | (x1:{item['x1']}, y1:{item['y1']}) -> (x2:{item['x2']}, y2:{item['y2']}) | Dist: {dist_px:.2f}px")
