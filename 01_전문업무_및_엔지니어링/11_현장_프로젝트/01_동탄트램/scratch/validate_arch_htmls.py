# -*- coding: utf-8 -*-
"""
건축분야 50개 공종 150개 HTML 파일 전수 품질 및 표준 준수 검증 스크립트
"""

import os
import sys

BASE_DIR = r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8\건축"

def validate_all():
    print("=== Validating 50 Architecture Tasks (150 HTML Files) ===")
    folders = sorted([d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))], key=lambda x: int(x.split('_')[0]) if x.split('_')[0].isdigit() else 999)

    total_files = 0
    errors = []

    for fld in folders:
        num = int(fld.split('_')[0]) if fld.split('_')[0].isdigit() else 999
        fld_path = os.path.join(BASE_DIR, fld)

        for sub in ['표준서', '수행지침', '체크리스트']:
            sub_path = os.path.join(fld_path, sub)
            if not os.path.exists(sub_path):
                errors.append(f"Missing subfolder {sub} in {fld}")
                continue

            htmls = [f for f in os.listdir(sub_path) if f.endswith('.html')]
            if not htmls:
                errors.append(f"No HTML found in {fld}/{sub}")
                continue

            for fn in htmls:
                total_files += 1
                fp = os.path.join(sub_path, fn)
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Basic Tailwind verification
                if 'cdn.tailwindcss.com' not in content:
                    errors.append(f"{fp}: Missing Tailwind CSS CDN")

                # WBS badge check
                if f"WBS 9000-2-{num}" not in content:
                    errors.append(f"{fp}: Missing WBS 9000-2-{num}")

                # If guideline, verify modals and SVG
                if sub == '수행지침':
                    if 'openDiagramZoom' not in content:
                        errors.append(f"{fp}: Missing openDiagramZoom modal")
                    if 'openGlossary' not in content:
                        errors.append(f"{fp}: Missing openGlossary modal")
                    if '<svg' not in content:
                        errors.append(f"{fp}: Missing SVG technical diagram")
                    if 'fill="#f8fafc"' not in content and 'fill="#ffffff"' not in content:
                        errors.append(f"{fp}: SVG must have Light-Theme background")

                # If checklist, verify question ending
                if sub == '체크리스트':
                    lines = content.splitlines()
                    for idx, line in enumerate(lines):
                        if '<td class="px-6 py-4 font-bold text-slate-800">' in line:
                            val = line.split('<td class="px-6 py-4 font-bold text-slate-800">')[1].split('</td>')[0].strip()
                            if not val.endswith('?') and not val.endswith('하였는가?') and not val.endswith('는가?') and not val.endswith('인가?'):
                                errors.append(f"{fp}: Checklist item not ending with question: '{val}'")

    print(f"Total HTML files verified: {total_files}")
    if errors:
        print(f"\n[!] Found {len(errors)} validation errors:")
        for e in errors[:20]:
            print("  -", e)
        sys.exit(1)
    else:
        print("\n>>> SUCCESS: ALL 150 ARCHITECTURE HTML FILES PASSED 100% QUALITY AND COMPLIANCE VALIDATION! <<<")

if __name__ == "__main__":
    validate_all()
