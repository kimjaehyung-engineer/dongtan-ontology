# -*- coding: utf-8 -*-
"""
동탄트램 매뉴얼BODY(집행단계-첨부폴더)v8
모든 11개 공종 1,346개 HTML 파일의 연계 네비게이션 버튼을 문서 최하단(바닥)으로 완벽 재배치하는 스크립트
"""

import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(r"08.메뉴얼 및 평면도\최종\02_메뉴얼 공종프로섹스(집행단계)\매뉴얼BODY(집행단계-첨부폴더)v8")

NAV_CSS = """
    /* Standardized Bottom Navigation Box */
    .nav-box { display: flex; gap: 12px; margin-top: 36px; padding-top: 24px; border-top: 1px solid #e2e8f0; width: 100%; box-sizing: border-box; }
    .nav-btn { flex: 1; text-align: center; padding: 14px 16px; border-radius: 6px; font-size: 13px; font-weight: 700; text-decoration: none; transition: 0.2s; display: inline-block; box-sizing: border-box; }
    .btn-std { background: #0f172a !important; color: #ffffff !important; }
    .btn-guide { background: #0284c7 !important; color: #ffffff !important; }
    .btn-chk { background: #d97706 !important; color: #ffffff !important; }
    .btn-std:hover { background: #1e293b !important; }
    .btn-guide:hover { background: #0369a1 !important; }
    .btn-chk:hover { background: #b45309 !important; }
"""

def clean_name(folder_or_file_name):
    name = re.sub(r'^\d+[\._\s]*', '', folder_or_file_name)
    name = name.replace('_표준서', '').replace('_수행지침', '').replace('_체크리스트', '').replace('.html', '')
    return name.strip()

total_processed = 0

for root, dirs, files in os.walk(BASE_DIR):
    subdirs = [d for d in dirs if d in ['표준서', '수행지침', '체크리스트']]
    if len(subdirs) >= 2:
        activity_dir = root
        activity_folder_name = os.path.basename(activity_dir)
        task_name = clean_name(activity_folder_name)

        std_dir = os.path.join(activity_dir, '표준서')
        guide_dir = os.path.join(activity_dir, '수행지침')
        chk_dir = os.path.join(activity_dir, '체크리스트')

        std_files = [f for f in os.listdir(std_dir) if f.endswith('.html')] if os.path.exists(std_dir) else []
        guide_files = [f for f in os.listdir(guide_dir) if f.endswith('.html')] if os.path.exists(guide_dir) else []
        chk_files = [f for f in os.listdir(chk_dir) if f.endswith('.html')] if os.path.exists(chk_dir) else []

        def pick_main(files_list, keyword):
            if not files_list: return None
            for f in files_list:
                if keyword in f and not f.startswith('9000-'):
                    return f
            for f in files_list:
                if keyword in f:
                    return f
            return files_list[0]

        main_std = pick_main(std_files, '표준서')
        main_guide = pick_main(guide_files, '수행지침') or pick_main(guide_files, '절차서') or (guide_files[0] if guide_files else None)
        main_chk = pick_main(chk_files, '체크리스트')

        for dtype, dpath, main_f, target_type in [
            ('표준서', std_dir, main_std, 'std'),
            ('수행지침', guide_dir, main_guide, 'guide'),
            ('체크리스트', chk_dir, main_chk, 'chk')
        ]:
            if not os.path.exists(dpath):
                continue
            
            html_in_dir = [f for f in os.listdir(dpath) if f.endswith('.html')]
            for hf in html_in_dir:
                file_full = os.path.join(dpath, hf)
                try:
                    with open(file_full, 'r', encoding='utf-8', errors='ignore') as fp:
                        content = fp.read()

                    # 1. 기존에 잘못 삽입된 nav-box 전면 제거 (head 및 body 전체에서 삭제)
                    content = re.sub(r'<div class=[\'"]nav-box[\'"][\s\S]*?</div>', '', content)

                    # 2. 새로운 바닥 네비게이션 HTML 생성
                    btn_htmls = []
                    if target_type == 'std':
                        if main_guide:
                            btn_htmls.append(f'<a href="../수행지침/{main_guide}" class="nav-btn btn-guide">📘 [연계] {task_name} 수행지침서 열기 ➔</a>')
                        if main_chk:
                            btn_htmls.append(f'<a href="../체크리스트/{main_chk}" class="nav-btn btn-chk">📋 [연계] {task_name} 체크리스트 열기 ➔</a>')
                    elif target_type == 'guide':
                        if main_std:
                            btn_htmls.append(f'<a href="../표준서/{main_std}" class="nav-btn btn-std">📄 [연계] {task_name} 표준서 열기 ➔</a>')
                        if main_chk:
                            btn_htmls.append(f'<a href="../체크리스트/{main_chk}" class="nav-btn btn-chk">📋 [연계] {task_name} 체크리스트 열기 ➔</a>')
                    elif target_type == 'chk':
                        if main_std:
                            btn_htmls.append(f'<a href="../표준서/{main_std}" class="nav-btn btn-std">📄 [연계] {task_name} 표준서 열기 ➔</a>')
                        if main_guide:
                            btn_htmls.append(f'<a href="../수행지침/{main_guide}" class="nav-btn btn-guide">📘 [연계] {task_name} 수행지침서 열기 ➔</a>')

                    if not btn_htmls:
                        continue

                    nav_box_block = f'\n    <!-- Bottom Navigation Block -->\n    <div class="nav-box">\n      ' + '\n      '.join(btn_htmls) + '\n    </div>\n'

                    # 3. CSS 정리 및 head 내 주입
                    # 기존 .nav-box 관련 CSS 제거 후 깔끔하게 재주입
                    content = re.sub(r'/\* Standardized Bottom Navigation Box \*/[\s\S]*?\.btn-chk:hover \{[^\}]*\}', '', content)
                    
                    if '</style>' in content:
                        content = content.replace('</style>', NAV_CSS + '\n  </style>', 1)
                    elif '</head>' in content:
                        content = content.replace('</head>', f'<style>{NAV_CSS}</style>\n</head>', 1)

                    # 4. 바디 영역 최하단에 정확히 삽입
                    # body 태그 시작 위치 파악
                    idx_body = content.find('<body')
                    if idx_body != -1:
                        head_part = content[:idx_body]
                        body_part = content[idx_body:]

                        # 바디 파트에서 삽입 위치 결정:
                        # 1순위: <div id="zoomModal" 바로 앞
                        # 2순위: <div id="glossaryModal" 바로 앞
                        # 3순위: 바디 내 마지막 <script 태그 바로 앞
                        # 4순위: </body> 바로 앞
                        if '<div id="zoomModal"' in body_part:
                            body_part = body_part.replace('<div id="zoomModal"', nav_box_block + '\n  <div id="zoomModal"', 1)
                        elif '<div id="glossaryModal"' in body_part:
                            body_part = body_part.replace('<div id="glossaryModal"', nav_box_block + '\n  <div id="glossaryModal"', 1)
                        elif '<script' in body_part:
                            # 바디 내의 첫번째 script 직전
                            idx_s = body_part.find('<script')
                            body_part = body_part[:idx_s] + nav_box_block + '\n  ' + body_part[idx_s:]
                        elif '</body>' in body_part:
                            body_part = body_part.replace('</body>', nav_box_block + '\n</body>', 1)
                        else:
                            body_part = body_part + nav_box_block

                        new_content = head_part + body_part
                    else:
                        new_content = content + nav_box_block

                    with open(file_full, 'w', encoding='utf-8') as fp:
                        fp.write(new_content)
                    total_processed += 1

                except Exception as e:
                    print(f"Error: {file_full} - {e}")

print(f"\n=======================================================")
print(f"총 {total_processed}개 HTML 파일 바닥(최하단) 네비게이션 재배치 완벽 완료!")
print(f"=======================================================")
