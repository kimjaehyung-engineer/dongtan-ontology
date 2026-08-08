# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

v1_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\동탄트램_업무_매뉴얼v1.html'
roadmap_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\동탄트램_업무_매뉴얼_로드맵.html'

with open(v1_path, 'r', encoding='utf-8') as f:
    v1_content = f.read()

with open(roadmap_path, 'r', encoding='utf-8') as f:
    roadmap_content = f.read()

# -------------------------------------------------------------
# 1. v1.html에서 2부 사이드바 리스트 및 본문 2부 추출
# -------------------------------------------------------------
nav_start = v1_content.find("<!-- 2부. 공종 간 인터페이스 및 간섭 관리 -->")
if nav_start == -1:
    nav_start = v1_content.find("2부. 인터페이스 &amp; 간섭 관리")
    if nav_start != -1:
        nav_start = v1_content.rfind("<li", 0, nav_start)
    else:
        # 혹은 직접 텍스트 매칭
        nav_start = v1_content.find('<li style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted);')

nav_end_candidate = v1_content.find("</ul>", nav_start)
new_nav_part2 = v1_content[nav_start:nav_end_candidate].strip()

print("Extracted new sidebar part 2 length:", len(new_nav_part2))

part2_start = v1_content.find('<section id="sec-interface-a"')
part2_end_candidate = v1_content.find('</section>', v1_content.find('<section id="sec-interface-d"')) + len('</section>')
new_body_part2 = v1_content[part2_start:part2_end_candidate].strip()

print("Extracted new body part 2 length:", len(new_body_part2))

# -------------------------------------------------------------
# 2. roadmap_content에 삽입
# -------------------------------------------------------------
# 2.1 사이드바 2부 삽입
# 로드맵 파일에서 'sec-construction-mgt' 또는 'sec-construction-mgt-3' 메뉴를 찾음
search_term = 'href="#sec-construction-mgt-3"'
idx_term = roadmap_content.find(search_term)
if idx_term == -1:
    search_term = 'href="#sec-construction-mgt"'
    idx_term = roadmap_content.find(search_term)

if idx_term != -1:
    # 그 뒤에 오는 </ul> 닫기 직전(또는 그 이전의 li 끝)을 찾아 삽입
    ul_close = roadmap_content.find("</ul>", idx_term)
    roadmap_updated = roadmap_content[:ul_close] + "\n    " + new_nav_part2 + "\n" + roadmap_content[ul_close:]
    print("Sidebar patched in roadmap!")
else:
    print("[ERROR] 10장 메뉴를 로드맵에서 찾을 수 없음!")
    sys.exit(1)

# 2.2 본문 2부 삽입
main_close = roadmap_updated.find("</main>")
if main_close != -1:
    roadmap_updated = roadmap_updated[:main_close] + "\n" + new_body_part2 + "\n" + roadmap_updated[main_close:]
    print("Body part 2 patched in roadmap!")
else:
    print("[ERROR] </main> 태그를 로드맵에서 찾을 수 없음!")
    sys.exit(1)

# 2.3 roadSectionIds 변수 업데이트
# 로드맵 스크립트 안에 'roadSectionIds' 또는 'roadSectionIds =' 가 있는지 찾음
# 2부의 신설된 섹션 아이디: 'sec-interface-a', 'sec-interface-b', 'sec-interface-c', 'sec-interface-d'
# (참고로 로드맵 모드 동작을 위해 'sec-interface-a', 'sec-interface-b', 'sec-interface-c', 'sec-interface-d' 추가)
match_ids = re.search(r'const\s+roadSectionIds\s*=\s*\[(.*?)\];', roadmap_updated, re.DOTALL)
if not match_ids:
    match_ids = re.search(r'roadSectionIds\s*=\s*\[(.*?)\]', roadmap_updated, re.DOTALL)

if match_ids:
    orig_ids_str = match_ids.group(1)
    if 'sec-interface-a' not in orig_ids_str:
        # 파싱 및 추가
        new_ids_str = orig_ids_str.strip()
        if new_ids_str.endswith(','):
            new_ids_str += " 'sec-interface-a', 'sec-interface-b', 'sec-interface-c', 'sec-interface-d'"
        else:
            # 쉼표가 없으면 붙임
            if new_ids_str:
                new_ids_str += ", 'sec-interface-a', 'sec-interface-b', 'sec-interface-c', 'sec-interface-d'"
            else:
                new_ids_str = "'sec-interface-a', 'sec-interface-b', 'sec-interface-c', 'sec-interface-d'"
        
        # 교체
        full_match_text = match_ids.group(0)
        # full_match_text에서 대괄호 내부를 교체
        new_match_text = full_match_text.replace(orig_ids_str, new_ids_str)
        roadmap_updated = roadmap_updated.replace(full_match_text, new_match_text)
        print("roadSectionIds updated in roadmap script!")

with open(roadmap_path, 'w', encoding='utf-8') as f:
    f.write(roadmap_updated)

print("Roadmap integration complete successfully!")
