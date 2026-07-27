import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"

# Modify Standard HTML (1회만 치환하도록 limit=1 설정)
def modify_standard_first_only(fp):
    if not os.path.exists(fp):
        return
    
    # We restore from clean state first by copying backup versions or reverting if needed
    # Actually, we can read the original from 메일송부(0723) and re-apply styling to ensure a clean run!
    backup_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\메일송부(0723)\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"
    sub_dir = "표준서"
    fn = os.path.basename(fp)
    src_clean = os.path.join(backup_base, sub_dir, fn)
    if not os.path.exists(src_clean):
        # Fallback to general base name
        src_clean = os.path.join(backup_base, sub_dir, "발주전략 KOM_표준서.html" if "KOM" in fn else "레일 용접장 선정_표준서.html")
        
    with open(src_clean, 'r', encoding='utf-8') as f:
        html = f.read()
        
    from implement_welding_glossary_interactive import common_style, common_modal_html
    
    # Inject CSS
    if "</style>" in html:
        html = html.replace("</style>", common_style + "\n    </style>")
        
    # Inject highlights inside body - LIMIT 1 (replace third argument as 1)
    html = html.replace("정척레일 15본", '<span class="term-highlight" onclick="openGlossary(\'standard_rail\')">정척레일</span> 15본', 1)
    html = html.replace("정척레일(25m)", '<span class="term-highlight" onclick="openGlossary(\'standard_rail\')">정척레일(25m)</span>', 1)
    html = html.replace("장대레일 제작하는", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span> 제작하는', 1)
    html = html.replace("장대로 용접하는", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span>로 용접하는', 1)
    html = html.replace("테르밋 및", '<span class="term-highlight" onclick="openGlossary(\'thermit\')">테르밋</span> 및', 1)
    html = html.replace("가스압접 용접을", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접 용접</span>을', 1)
    html = html.replace("NDT 작업 공간", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">NDT(비파괴검사)</span> 작업 공간', 1)
    
    # Inject scene view button inside body
    html = html.replace("레일 용접장 선정 정량적", '레일 용접장 선정 <span class="scene-link" onclick="openScene(\'yard\')">📸 용접장 전경 보기</span> 정량적', 1)
    
    # Inject Modal Div & JS right before </body>
    if "</body>" in html:
        html = html.replace("</body>", common_modal_html + "\n</body>")
        
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"🎉 Cleaned and updated Standard (First-time highlight only): {os.path.basename(fp)}")

# Modify Guideline HTML (1회만 치환)
def modify_guideline_first_only(fp):
    if not os.path.exists(fp):
        return
        
    backup_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\메일송부(0723)\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"
    src_clean = os.path.join(backup_base, "수행지침", "레일 용접장 선정_수행지침.html")
    
    with open(src_clean, 'r', encoding='utf-8') as f:
        html = f.read()
        
    from implement_welding_glossary_interactive import common_style, common_modal_html
    
    # Inject CSS
    if "</style>" in html:
        html = html.replace("</style>", common_style + "\n    </style>")
        
    # Inject highlights inside body - LIMIT 1
    html = html.replace("정척 레일을", '<span class="term-highlight" onclick="openGlossary(\'standard_rail\')">정척레일</span>을', 1)
    html = html.replace("장대레일로 1차", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span>로 1차', 1)
    html = html.replace("장대레일 반출", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span> 반출', 1)
    html = html.replace("가스압접/플래시버트 용접하기", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접</span>/<span class="term-highlight" onclick="openGlossary(\'flash_butt\')">플래시버트 용접</span>하기', 1)
    html = html.replace("가스압접/플래시버트 용접용", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접</span>/<span class="term-highlight" onclick="openGlossary(\'flash_butt\')">플래시버트 용접</span>용', 1)
    html = html.replace("가스압접/플래시버트 용접 및", '<span class="term-highlight" onclick="openGlossary(\'gas_pressure\')">가스압접</span>/<span class="term-highlight" onclick="openGlossary(\'flash_butt\')">플래시버트 용접</span> 및', 1)
    
    html = html.replace("비파괴 검사장", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴 검사(NDT)장</span>', 1)
    html = html.replace("비파괴검사(초음파/자분)", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴검사(NDT)</span>', 1)
    html = html.replace("비파괴 시험(UT/MT)", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴 시험(NDT)</span>', 1)
    
    # Inject scene view buttons
    html = html.replace("용접장 입지 검토", '용접장 입지 검토 <span class="scene-link" onclick="openScene(\'yard\')">📸 용접장 전경 보기</span>', 1)
    html = html.replace("버(Burr) 전단", '버(Burr) 전단 <span class="scene-link" onclick="openScene(\'flash_butt\')">📸 용접 과정 보기</span>', 1)
    html = html.replace("장대레일 반출", '장대레일 반출 <span class="scene-link" onclick="openScene(\'launching\')">📸 인입(Launching) 보기</span>', 1)
    
    # Inject Modal Div & JS right before </body>
    if "</body>" in html:
        html = html.replace("</body>", common_modal_html + "\n</body>")
        
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"🎉 Cleaned and updated Guideline (First-time highlight only): {os.path.basename(fp)}")

# Modify Checklist HTML (1회만 치환)
def modify_checklist_first_only(fp):
    if not os.path.exists(fp):
        return
        
    backup_base = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\메일송부(0723)\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"
    fn = os.path.basename(fp)
    src_clean = os.path.join(backup_base, "체크리스트", fn)
    if not os.path.exists(src_clean):
        src_clean = os.path.join(backup_base, "체크리스트", "레일 용접장 선정_체크리스트.html")
        
    with open(src_clean, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # We must apply check-list formatting first (div wrapping, etc.)
    from format_kom_checklists import format_risk_checklist_text
    import re
    
    pre_pattern = r'(<tr class="pre-row">.*?<td class="category">.*?</td>\s*<td>)(.*?)(</td>)'
    def pre_repl(match):
        return f"{match.group(1)}\n{format_risk_checklist_text(match.group(2))}                {match.group(3)}"
    ing_pattern = r'(<tr class="ing-row">.*?<td class="category">.*?</td>\s*<td>)(.*?)(</td>)'
    def ing_repl(match):
        return f"{match.group(1)}\n{format_risk_checklist_text(match.group(2))}                {match.group(3)}"
    post_pattern = r'(<tr class="post-row">.*?<td class="category">.*?</td>\s*<td>)(.*?)(</td>)'
    def post_repl(match):
        return f"{match.group(1)}\n{format_risk_checklist_text(match.group(2))}                {match.group(3)}"

    html = re.sub(pre_pattern, pre_repl, html, flags=re.DOTALL)
    html = re.sub(ing_pattern, ing_repl, html, flags=re.DOTALL)
    html = re.sub(post_pattern, post_repl, html, flags=re.DOTALL)
    
    from implement_welding_glossary_interactive import common_style, common_modal_html
    
    # Inject CSS
    if "</style>" in html:
        html = html.replace("</style>", common_style + "\n    </style>")
        
    # Inject highlights inside body - LIMIT 1
    html = html.replace("장대레일 제작 시", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span> 제작 시', 1)
    html = html.replace("장대레일 영구", '<span class="term-highlight" onclick="openGlossary(\'cwr\')">장대레일</span> 영구', 1)
    html = html.replace("비파괴 시험(UT/MT)", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">비파괴 시험(NDT)</span>', 1)
    html = html.replace("NDT 용접부", '<span class="term-highlight" onclick="openGlossary(\'ndt\')">NDT 용접부</span>', 1)
    
    # Inject scene link inside risk checkbox list
    html = html.replace("수평 오차 초과로", '수평 오차 초과로 <span class="scene-link" onclick="openScene(\'yard\')">📸 롤러 가이드 베드 보기</span>', 1)
    
    # Inject Modal Div & JS right before </body>
    if "</body>" in html:
        html = html.replace("</body>", common_modal_html + "\n</body>")
        
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"🎉 Cleaned and updated Checklist (First-time highlight only): {os.path.basename(fp)}")

# Target files
std_files = [
    os.path.join(base_dir, "표준서", "레일 용접장 선정_표준서.html"),
    os.path.join(base_dir, "표준서", "3_레일 용접장 선정_표준서.html")
]
gui_files = [
    os.path.join(base_dir, "수행지침", "레일 용접장 선정_수행지침.html"),
    os.path.join(base_dir, "수행지침", "3_레일 용접장 선정_수행지침.html")
]
chk_files = [
    os.path.join(base_dir, "체크리스트", "레일 용접장 선정_체크리스트.html"),
    os.path.join(base_dir, "체크리스트", "3_레일 용접장 선정_체크리스트.html")
]

# Run first-only conversion
for sf in std_files: modify_standard_first_only(sf)
for gf in gui_files: modify_guideline_first_only(gf)
for cf in chk_files: modify_checklist_first_only(cf)

print("\n🎉 Format polishing complete! Term popups are now limited to the first occurrence only.")
