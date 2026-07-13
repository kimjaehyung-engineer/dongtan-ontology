import os
import shutil
import re
from bs4 import BeautifulSoup

def standardize_headers(file_path):
    print(f"Standardizing all article headers inside: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_standard_headers"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. Update CSS styles (inject new layout rules inside <style> tags)
    # We will search for a style tag and append our CSS helper classes at the end of the first style block.
    style_tag = soup.find("style")
    if style_tag:
        additional_css = """
        /* Premium Standardized Article Headers */
        .sheet-header {
            display: flex !important;
            justify-content: space-between !important;
            align-items: flex-start !important;
            border-bottom: 2px solid var(--border) !important;
            padding-bottom: 24px !important;
            margin-bottom: 35px !important;
            gap: 20px !important;
        }
        .header-left {
            flex: 1 !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: flex-start !important;
            text-align: left !important;
        }
        .header-right {
            display: flex !important;
            flex-direction: column !important;
            align-items: flex-end !important;
            gap: 12px !important;
            flex-shrink: 0 !important;
        }
        .header-right .q-toggle-btn {
            margin-top: 0 !important; /* Reset margin since flexbox handles gap */
        }
        """
        style_tag.append(additional_css)
        print("CSS classes injected into style tag.")
        
    # 2. Refactor HTML DOM of each article's header
    articles = soup.find_all("article", class_="answer-sheet")
    print(f"Refactoring {len(articles)} article headers...")
    
    updated_count = 0
    for art in articles:
        header = art.find(class_="sheet-header")
        if not header:
            # Fallback check for header tags
            header = art.find("header")
            if not header:
                continue
                
        # Extract elements to arrange
        category_container = header.find(class_="category-path-container")
        question_meta = header.find(class_="question-meta")
        question_title = header.find(class_="question-title")
        if not question_title:
            question_title = header.find("h2")
            
        score_badge = header.find(class_="score-badge")
        
        # If we didn't find them inside header directly, search inside any inner divs
        if not category_container:
            category_container = art.find(class_="category-path-container")
        if not question_meta:
            question_meta = art.find(class_="question-meta")
        if not question_title:
            question_title = art.find("h2")
        if not score_badge:
            score_badge = art.find(class_="score-badge")
            
        # Create new structure
        header_left = soup.new_tag("div", attrs={"class": "header-left"})
        header_right = soup.new_tag("div", attrs={"class": "header-right"})
        
        # Append elements in correct order
        if category_container:
            header_left.append(category_container.extract())
        if question_meta:
            header_left.append(question_meta.extract())
        if question_title:
            header_left.append(question_title.extract())
            
        if score_badge:
            header_right.append(score_badge.extract())
            
        # Clear original header contents and drop in new structured divs
        header.clear()
        header.append(header_left)
        header.append(header_right)
        updated_count += 1
        
    print(f"Successfully restructured {updated_count} headers in DOM.")
    
    # 3. Update JavaScript logic for toggle button insertion
    # We look for: toggleBtn = document.createElement('span'); ... header.appendChild(toggleBtn);
    # and replace with append to .header-right
    html_content = str(soup)
    
    original_js_part = "header.appendChild(toggleBtn);"
    replacement_js_part = """const headerRight = header.querySelector('.header-right');
                if (headerRight) {
                    headerRight.appendChild(toggleBtn);
                } else {
                    header.appendChild(toggleBtn);
                }"""
                
    if original_js_part in html_content:
        html_content = html_content.replace(original_js_part, replacement_js_part)
        print("Successfully updated JavaScript toggle button injection target.")
    else:
        # Attempt regex matching if formatting is slightly different
        html_content = re.sub(
            r"header\.appendChild\(\s*toggleBtn\s*\);",
            "const headerRight = header.querySelector('.header-right'); if (headerRight) { headerRight.appendChild(toggleBtn); } else { header.appendChild(toggleBtn); }",
            html_content
        )
        print("Attempted regex replacement for JavaScript injection.")
        
    # 4. Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Saved standardized file to: {file_path}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = standardize_headers(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied standardized HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
