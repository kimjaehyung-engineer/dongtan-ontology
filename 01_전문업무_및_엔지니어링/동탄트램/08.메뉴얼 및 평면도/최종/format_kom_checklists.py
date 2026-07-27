import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

targets = [
    {
        "gongjong": "사전토공사",
        "folder": "2_발주전략 KOM",
        "file": "발주전략 KOM_체크리스트.html"
    },
    {
        "gongjong": "상부강화노반",
        "folder": "2_발주전략 KOM",
        "file": "발주전략 KOM_체크리스트.html"
    },
    {
        "gongjong": "콘크리트도상",
        "folder": "4_발주전략 KOM",
        "file": "4_발주전략 KOM_체크리스트.html"
    }
]

def format_risk_checklist_text(raw_text):
    # Split text by typical delimiters (•, ·, div, p, li or newlines)
    text_stripped = re.sub(r'<(div|p|li)[^>]*>', '\n', raw_text)
    text_stripped = re.sub(r'</(div|p|li)>', '\n', text_stripped)
    raw_sentences = re.split(r'[•·\n]', text_stripped)
    
    cleaned_sentences = []
    for s in raw_sentences:
        s = re.sub(r'<[^>]*>', '', s).strip()
        if not s:
            continue
        # Remove ☐ and [ ]
        s = s.replace("☐", "").replace("[ ]", "").strip()
        if "상세 체크리스트 파일" in s or "더블클릭" in s or "---" in s:
            continue
        s = re.sub(r'\s+', ' ', s)
        if s:
            cleaned_sentences.append(s)
            
    formatted_html = ""
    for s in cleaned_sentences:
        formatted_html += f'                    <div style="margin-bottom: 8px;">• {s}</div>\n'
    return formatted_html

updated_count = 0
for t in targets:
    gongjong = t["gongjong"]
    folder = t["folder"]
    filename = t["file"]
    
    fp = os.path.join(base_dir, gongjong, folder, "체크리스트", filename)
    if not os.path.exists(fp):
        print(f"⚠️ File not found: {fp}")
        continue
        
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Replace pre-row, ing-row, post-row using Regex
    pre_pattern = r'(<tr class="pre-row">.*?<td class="category">.*?</td>\s*<td>)(.*?)(</td>)'
    def pre_repl(match):
        prefix = match.group(1)
        inner_td = match.group(2)
        suffix = match.group(3)
        new_inner = format_risk_checklist_text(inner_td)
        return f"{prefix}\n{new_inner}                {suffix}"

    ing_pattern = r'(<tr class="ing-row">.*?<td class="category">.*?</td>\s*<td>)(.*?)(</td>)'
    def ing_repl(match):
        prefix = match.group(1)
        inner_td = match.group(2)
        suffix = match.group(3)
        new_inner = format_risk_checklist_text(inner_td)
        return f"{prefix}\n{new_inner}                {suffix}"

    post_pattern = r'(<tr class="post-row">.*?<td class="category">.*?</td>\s*<td>)(.*?)(</td>)'
    def post_repl(match):
        prefix = match.group(1)
        inner_td = match.group(2)
        suffix = match.group(3)
        new_inner = format_risk_checklist_text(inner_td)
        return f"{prefix}\n{new_inner}                {suffix}"

    html_mod = re.sub(pre_pattern, pre_repl, html, flags=re.DOTALL)
    html_mod = re.sub(ing_pattern, ing_repl, html_mod, flags=re.DOTALL)
    html_mod = re.sub(post_pattern, post_repl, html_mod, flags=re.DOTALL)
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(html_mod)
        
    print(f"🎉 Standardized check-bullet format for: {gongjong}/{folder}/체크리스트/{filename}")
    updated_count += 1

print(f"\n🎉 Successfully formatted {updated_count} KOM checklist files while keeping original texts!")
