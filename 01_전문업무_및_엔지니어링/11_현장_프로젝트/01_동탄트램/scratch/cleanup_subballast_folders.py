# -*- coding: utf-8 -*-
import os
import sys
import shutil

sys.path.append(os.path.abspath("scratch"))
from subballast_part1 import ALL_TASKS as PART1_TASKS
from subballast_part2 import PART2_TASKS

TOTAL_TASKS = PART1_TASKS + PART2_TASKS

def sanitize_filename(name):
    for ch in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
        name = name.replace(ch, '_')
    return name

canonical_folders = set(sanitize_filename(t[1]) for t in TOTAL_TASKS)
print(f"정규 폴더 개수: {len(canonical_folders)}")

base = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\4.상부강화노반")

for item in os.listdir(base):
    item_path = os.path.join(base, item)
    if os.path.isdir(item_path):
        if item not in canonical_folders:
            print(f"구버전/중복 폴더 삭제: {item}")
            shutil.rmtree(item_path)

remaining = [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
print(f"\n최종 정리 후 남은 디렉토리 수: {len(remaining)}개")
