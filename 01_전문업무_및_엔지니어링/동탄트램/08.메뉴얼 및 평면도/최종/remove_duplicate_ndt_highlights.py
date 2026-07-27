import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

target_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"

files_to_check = [
    os.path.join(target_base, "수행지침", "레일 용접장 선정_수행지침.html"),
    os.path.join(target_base, "수행지침", "3_레일 용접장 선정_수행지침.html"),
    os.path.join(target_base, "표준서", "레일 용접장 선정_표준서.html"),
    os.path.join(target_base, "표준서", "3_레일 용접장 선정_표준서.html"),
    os.path.join(target_base, "체크리스트", "레일 용접장 선정_체크리스트.html"),
    os.path.join(target_base, "체크리스트", "3_레일 용접장 선정_체크리스트.html")
]

for fp in files_to_check:
    if not os.path.exists(fp):
        continue
        
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
        
    before_len = len(content)
    
    # 1. Guideline specific duplicate NDT link removal
    content = content.replace(
        'NDT <span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴검사(NDT)</span> 전용 암실',
        'NDT 비파괴검사(NDT) 전용 암실'
    )
    content = content.replace(
        'NDT <span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴검사(NDT)</span>',
        'NDT 비파괴검사(NDT)'
    )
    
    # 2. General duplicate check for other files
    ndt_spans = list(re.finditer(r'<span class="term-highlight" onclick="openGlossary\(\'ndt\'\)">([^<]+)</span>', content))
    if len(ndt_spans) > 1:
        new_content = ""
        last_idx = 0
        for i, match in enumerate(ndt_spans):
            start, end = match.span()
            inner_text = match.group(1)
            if i == 0:
                continue
            else:
                new_content += content[last_idx:start] + inner_text
                last_idx = end
        new_content += content[last_idx:]
        content = new_content
        
    after_len = len(content)
    if before_len != after_len:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"🎉 Successfully cleaned duplicate NDT links in: {os.path.basename(fp)}")
    else:
        print(f"ℹ️ No duplicate NDT links found in: {os.path.basename(fp)}")
