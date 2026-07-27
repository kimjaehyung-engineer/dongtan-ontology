import os
import glob
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

# Find all checklist HTML files in all folders (including 상부강화노반)
all_checklist_files = glob.glob(os.path.join(base_dir, "**", "*체크리스트.html"), recursive=True)

def process_cell_text(html_td_content):
    # This splits original td content by <br>, <div...>, <li>, bullet marks (•, ·) or newlines
    # First, strip existing div/li wrapper tags but keep content
    content_stripped = re.sub(r'<(div|p|li)[^>]*>', '\n', html_td_content)
    content_stripped = re.sub(r'</(div|p|li)>', '\n', content_stripped)
    
    # Split by bullets or newlines
    raw_sentences = re.split(r'[•·\n]', content_stripped)
    
    cleaned_sentences = []
    for s in raw_sentences:
        # Strip HTML tags like <br>
        s = re.sub(r'<[^>]*>', '', s).strip()
        if not s:
            continue
        
        # Remove ☐ and [ ] and double bullet remnants
        s = s.replace("☐", "").replace("[ ]", "").strip()
        
        # Skip generic placeholder instructions in the manual
        if "상세 체크리스트 파일" in s or "더블클릭" in s or "---" in s:
            continue
            
        # Clean double whitespaces
        s = re.sub(r'\s+', ' ', s)
        
        if s:
            cleaned_sentences.append(s)
            
    # Wrap each sentence in a div with bottom margin for perfect line separation in browser
    formatted_html = ""
    for s in cleaned_sentences:
        formatted_html += f'                    <div style="margin-bottom: 8px;">• {s}</div>\n'
        
    return formatted_html

updated_count = 0
error_count = 0

for file_path in all_checklist_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse pre-row, ing-row, post-row using regex
        # We need to find the <td> following the category <td> in each row type

        # 1. Pre-row replacement
        pre_pattern = r'(<tr class="pre-row">.*?<td class="category">.*?</td>\s*<td>)(.*?)(</td>)'
        def pre_repl(match):
            prefix = match.group(1)
            inner_td = match.group(2)
            suffix = match.group(3)
            new_inner = process_cell_text(inner_td)
            return f"{prefix}\n{new_inner}                {suffix}"

        # 2. Ing-row replacement
        ing_pattern = r'(<tr class="ing-row">.*?<td class="category">.*?</td>\s*<td>)(.*?)(</td>)'
        def ing_repl(match):
            prefix = match.group(1)
            inner_td = match.group(2)
            suffix = match.group(3)
            new_inner = process_cell_text(inner_td)
            return f"{prefix}\n{new_inner}                {suffix}"

        # 3. Post-row replacement
        post_pattern = r'(<tr class="post-row">.*?<td class="category">.*?</td>\s*<td>)(.*?)(</td>)'
        def post_repl(match):
            prefix = match.group(1)
            inner_td = match.group(2)
            suffix = match.group(3)
            new_inner = process_cell_text(inner_td)
            return f"{prefix}\n{new_inner}                {suffix}"

        # Apply regex replacement flags re.DOTALL to match multiline inner td
        content_mod = re.sub(pre_pattern, pre_repl, content, flags=re.DOTALL)
        content_mod = re.sub(ing_pattern, ing_repl, content_mod, flags=re.DOTALL)
        content_mod = re.sub(post_pattern, post_repl, content_mod, flags=re.DOTALL)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content_mod)
        
        updated_count += 1
        # Print status of progress
        if updated_count % 30 == 0 or updated_count == len(all_checklist_files):
            print(f"[{updated_count}/{len(all_checklist_files)}] Checklist files formatted successfully.")

    except Exception as e:
        error_count += 1
        print(f"❌ Error processing '{file_path}': {e}")

print(f"\n🎉 Completed formatting all checklist files!")
print(f"• Successfully Formatted: {updated_count}")
print(f"• Errors: {error_count}")
