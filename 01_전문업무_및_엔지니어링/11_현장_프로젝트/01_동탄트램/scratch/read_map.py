import os

with open('08.메뉴얼 및 평면도/동탄트램_노선도.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if '연계 실무 매뉴얼 가이드' in line:
            start = max(0, i-5)
            end = min(len(lines), i+20)
            print("--- HTML ---")
            print(''.join(lines[start:end]))
            break

    print("--- SCRIPT DATA ---")
    for i, line in enumerate(lines):
        if 'stationMapData' in line or 'const mapData' in line or 'function selectStation' in line:
            start = max(0, i-5)
            end = min(len(lines), i+30)
            print(''.join(lines[start:end]))
            break
