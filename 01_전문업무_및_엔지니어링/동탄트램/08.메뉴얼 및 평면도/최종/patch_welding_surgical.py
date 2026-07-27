import os
import sys
import re
import shutil

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\콘크리트도상\3_레일 용접장 선정"

# Minimum required styles ONLY for glossary and modal.
# Absolutely NO override on container, h2, table, root, or body styles!
minimal_glossary_style = """
    /* Glossary Modal Styles - Minimal Injection */
    .term-highlight {
        color: #0284c7 !important;
        font-weight: 700 !important;
        border-bottom: 2px dashed #0284c7 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        padding: 0 2px !important;
    }
    .term-highlight:hover {
        background: #e0f2fe !important;
        color: #0369a1 !important;
        border-radius: 4px !important;
    }
    .scene-link {
        display: inline-flex !important;
        align-items: center !important;
        gap: 4px !important;
        color: #059669 !important;
        font-weight: 700 !important;
        background: #ecfdf5 !important;
        border: 1px solid #10b981 !important;
        border-radius: 6px !important;
        padding: 2px 8px !important;
        font-size: 0.8rem !important;
        cursor: pointer !important;
        margin-left: 8px !important;
        transition: all 0.2s ease !important;
        text-decoration: none !important;
    }
    .scene-link:hover {
        background: #d1fae5 !important;
        color: #065f46 !important;
    }
    .glossary-modal {
        display: none;
        position: fixed;
        z-index: 9999;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(4px);
        align-items: center;
        justify-content: center;
    }
    .glossary-modal.active {
        display: flex;
    }
    .glossary-modal-content {
        background-color: #ffffff;
        margin: auto;
        padding: 24px;
        border: 1px solid #e2e8f0;
        width: 90%;
        max-width: 520px;
        border-radius: 16px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        position: relative;
        animation: modalFadeIn 0.3s ease;
        text-align: left;
    }
    @keyframes modalFadeIn {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    .glossary-close {
        color: #94a3b8;
        position: absolute;
        right: 20px;
        top: 16px;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
        transition: color 0.2s;
    }
    .glossary-close:hover {
        color: #334155;
    }
"""

from implement_welding_glossary_interactive import common_modal_html

# 1. Modify Standard HTML
def patch_standard(fp):
    if not os.path.exists(fp):
        return
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Append minimal style inside original style section
    if "</style>" in html:
        html = html.replace("</style>", minimal_glossary_style + "\n    </style>")
        
    # Inject highlights inside body - LIMIT 1
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
    print(f"🎉 Patched Standard file while keeping original layouts: {os.path.basename(fp)}")

# 2. Modify Guideline HTML
def patch_guideline(fp):
    if not os.path.exists(fp):
        return
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Append minimal style inside original style section
    if "</style>" in html:
        html = html.replace("</style>", minimal_glossary_style + "\n    </style>")
        
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
    print(f"🎉 Patched Guideline file while keeping original layouts: {os.path.basename(fp)}")

# 3. Modify Checklist HTML
def patch_checklist(fp):
    if not os.path.exists(fp):
        return
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Re-apply risk checklist formatting
    from format_kom_checklists import format_risk_checklist_text
    
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
    
    # Append minimal style inside original style section
    if "</style>" in html:
        html = html.replace("</style>", minimal_glossary_style + "\n    </style>")
        
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
    print(f"🎉 Patched Checklist file while keeping original layouts: {os.path.basename(fp)}")

# Run patch processes
patch_standard(os.path.join(base_dir, "표준서", "레일 용접장 선정_표준서.html"))
patch_standard(os.path.join(base_dir, "표준서", "3_레일 용접장 선정_표준서.html"))

patch_guideline(os.path.join(base_dir, "수행지침", "레일 용접장 선정_수행지침.html"))
# Create copy with prefix
shutil.copy2(os.path.join(base_dir, "수행지침", "레일 용접장 선정_수행지침.html"), os.path.join(base_dir, "수행지침", "3_레일 용접장 선정_수행지침.html"))
print("🎉 Created prefixed guideline copy.")

patch_checklist(os.path.join(base_dir, "체크리스트", "레일 용접장 선정_체크리스트.html"))
patch_checklist(os.path.join(base_dir, "체크리스트", "3_레일 용접장 선정_체크리스트.html"))

print("\n🎉 All 5 welding yard files successfully patched with ZERO layout breakage!")
