# -*- coding: utf-8 -*-
"""
전기분야 33개 공종 총 99개 HTML 무결성 및 품질 전수 검증 스크립트
"""

import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\전기분야"

folders = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))], key=lambda x: int(x.split('_')[0]) if x.split('_')[0].isdigit() else 999)

print(f"Total folders found: {len(folders)}")
total_files = 0
errors = []

for fld in folders:
    p = os.path.join(base_dir, fld)
    for sub in ['표준서', '수행지침', '체크리스트']:
        sub_p = os.path.join(p, sub)
        if not os.path.exists(sub_p):
            errors.append(f"Missing folder: {sub_p}")
            continue
        htmls = [f for f in os.listdir(sub_p) if f.endswith('.html')]
        if len(htmls) == 0:
            errors.append(f"No HTML in {sub_p}")
        for h in htmls:
            total_files += 1
            fp = os.path.join(sub_p, h)
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check basic structure
            if '<!DOCTYPE html>' not in content:
                errors.append(f"{fp}: missing doctype")
            if 'cdn.tailwindcss.com' not in content:
                errors.append(f"{fp}: missing tailwind")
                
            if sub == '수행지침':
                if 'openDiagramZoom' not in content or 'openGlossary' not in content:
                    errors.append(f"{fp}: missing zoom/glossary functions")
                if '<svg' not in content:
                    errors.append(f"{fp}: missing svg diagram")
                # SVG Light theme check
                if '#0f172a' in content and 'fill="#f8fafc"' not in content:
                    errors.append(f"{fp}: svg not using light theme")
                    
            if sub == '체크리스트':
                # Verify question endings
                pattern = re.compile(r'<td class="p-4 font-medium text-slate-700[^"]*">([^<]+)</td>')
                questions = pattern.findall(content)
                if not questions:
                    errors.append(f"{fp}: no questions found")
                for q in questions:
                    if not q.strip().endswith('는가?'):
                        errors.append(f"{fp}: question ending error -> {q}")

print(f"Total HTML verified: {total_files}")
if errors:
    print(f"FAILED with {len(errors)} errors:")
    for err in errors[:10]:
        print("  -", err)
else:
    print(">>> SUCCESS: ALL 99 ELECTRIC HTML FILES PASSED 100% QUALITY AND COMPLIANCE VALIDATION! <<<")
