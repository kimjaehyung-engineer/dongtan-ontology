# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

GRAPH_ENGINE_PATH = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\graph_engine.py")

with open(GRAPH_ENGINE_PATH, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# 1. Update borehole filtering
target_bh = '''        # 필터링 조건
        if section == "1" and not (is_sec1 or is_depot):
            continue'''

replacement_bh = '''        # 필터링 조건
        if section == "proposals":
            continue
        if section == "1" and not (is_sec1 or is_depot):
            continue'''

if target_bh in code:
    code = code.replace(target_bh, replacement_bh, 1)
    print("Patched borehole filter for proposals view")

# 2. Update knowledge_nodes filtering
target_kn = '''            for kn in k_nodes:
                k_fac = kn["facility"] or ""'''

replacement_kn = '''            for kn in k_nodes:
                k_fac = kn["facility"] or ""
                k_type = kn["type"] or ""
                if section == "geotech" and "PROPOSAL" in k_type:
                    continue'''

if target_kn in code:
    code = code.replace(target_kn, replacement_kn, 1)
    print("Patched knowledge_nodes filter for geotech view")

with open(GRAPH_ENGINE_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved graph_engine.py")
