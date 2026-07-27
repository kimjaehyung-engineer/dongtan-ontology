import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_attach_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

fixed_count = 0

for root, dirs, files in os.walk(base_attach_dir):
    for f in files:
        if f.endswith(('_표준서.html', '_수행지침.html', '_체크리스트.html')):
            file_path = os.path.join(root, f)
            with open(file_path, 'r', encoding='utf-8') as h_file:
                content = h_file.read()
            
            # Check if subcontractor-advisory-box is placed AFTER </html> or after main container close
            if 'subcontractor-advisory-box' in content:
                # Remove any box placed outside body/container
                box_match = re.search(r'(<div class="subcontractor-advisory-box".*?</div>\s*</div>)', content, re.DOTALL)
                if not box_match:
                    box_match = re.search(r'(<div class="subcontractor-advisory-box".*?</div>)', content, re.DOTALL)
                
                if box_match:
                    box_html = box_match.group(1)
                    # Clean out box from wherever it currently is
                    clean_content = content.replace(box_html, '')
                    
                    # Insert box right before the footer div
                    footer_pattern = r'(<div class="(?:footer-note|bg-slate-900[^"]*footer[^"]*|bg-slate-900[^"]*text-slate-400)">)'
                    if re.search(footer_pattern, clean_content):
                        new_content = re.sub(footer_pattern, box_html + '\n\\1', clean_content)
                    else:
                        # Fallback insert before </body>
                        new_content = re.sub(r'(</body>)', box_html + '\n\\1', clean_content)
                        
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as h_file:
                            h_file.write(new_content)
                        fixed_count += 1

print(f"Refined layout placement for {fixed_count} HTML files!")
