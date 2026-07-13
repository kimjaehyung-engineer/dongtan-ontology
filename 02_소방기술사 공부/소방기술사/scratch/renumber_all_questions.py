import re
import os
import shutil
from bs4 import BeautifulSoup

def format_q_range(q_nums):
    if not q_nums:
        return ""
    q_nums = sorted(list(set(q_nums)))
    ranges = []
    start = q_nums[0]
    end = q_nums[0]
    
    for n in q_nums[1:]:
        if n == end + 1:
            end = n
        else:
            if start == end:
                ranges.append(f"Q{start}")
            else:
                ranges.append(f"Q{start}~Q{end}")
            start = n
            end = n
    if start == end:
        ranges.append(f"Q{start}")
    else:
        ranges.append(f"Q{start}~Q{end}")
    
    return ", ".join(ranges)

def extract_clean_title(h2_text):
    # 1. Remove Question prefix inside brackets
    clean = re.sub(r"^\[Question\s*\d+(?:-\d+)?\]\s*", "", h2_text, flags=re.IGNORECASE)
    # 2. Remove chapter brackets
    clean = re.sub(r"^\[[^\]]+\]\s*", "", clean)
    # 3. Remove Question_Temp prefix
    clean = re.sub(r"Question_Temp_\d+\.\s*", "", clean, flags=re.IGNORECASE)
    # 4. Remove Question XX. prefix
    clean = re.sub(r"^(?:Question|Q)\s*\d+(?:-\d+)?\.\s*", "", clean, flags=re.IGNORECASE)
    # 5. Remove number only prefix like "44-1. "
    clean = re.sub(r"^\d+(?:-\d+)?\.\s*", "", clean)
    return clean.strip()

def process_html_file(file_path):
    print(f"\nProcessing file: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_renumber"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. Map current sidebar structure to identify chapters and their respective question IDs
    original_id_to_chapter = {}
    chapter_info = [] # list of dicts: { index, name, original_header_text, original_ids }
    
    containers = soup.find_all("div", class_="nav-chapter-container")
    print(f"Found {len(containers)} chapter containers in sidebar.")
    
    for c_idx, container in enumerate(containers):
        header = container.find("div", class_="nav-chapter-header")
        header_text = header.get_text(strip=True) if header else f"Chapter {c_idx+1}"
        
        # Clean chapter name to extract bracket category
        # e.g., "📁 [소방화학] (Q1~Q5)▼" -> "[소방화학]"
        ch_name_match = re.search(r"(\[[^\]]+\])", header_text)
        ch_name = ch_name_match.group(1) if ch_name_match else header_text.replace("📁", "").strip()
        
        # Extract links
        links = container.find_all("a", class_="nav-link")
        q_ids = []
        for link in links:
            href = link.get("href", "")
            if href.startswith("#"):
                q_id = href[1:]
                q_ids.append(q_id)
                original_id_to_chapter[q_id] = {
                    "ch_index": c_idx + 1,
                    "ch_name": ch_name
                }
                
        chapter_info.append({
            "index": c_idx + 1,
            "name": ch_name,
            "container": container,
            "original_ids": q_ids,
            "new_nums": []
        })
        
    # 2. Find all body articles
    articles = soup.find_all("article")
    print(f"Found {len(articles)} articles in body.")
    
    old_id_to_new_id = {}
    old_id_to_new_num = {}
    art_info_list = []
    
    # 3. First pass: assign new sequential numbers based on physical order in body
    for idx, art in enumerate(articles):
        old_id = art.get("id", "")
        if not old_id:
            continue
            
        new_num = idx + 1
        new_id = f"q{new_num}"
        old_id_to_new_id[old_id] = new_id
        old_id_to_new_num[old_id] = new_num
        
        # Get chapter mapping
        ch_map = original_id_to_chapter.get(old_id, {"ch_index": 1, "ch_name": "[기타]"})
        ch_idx = ch_map["ch_index"]
        ch_name = ch_map["ch_name"]
        
        # Record new num under the chapter
        chapter_info[ch_idx - 1]["new_nums"].append(new_num)
        
        h2 = art.find("h2")
        h2_text = h2.get_text(strip=True) if h2 else ""
        clean_title = extract_clean_title(h2_text)
        
        art_info_list.append({
            "element": art,
            "old_id": old_id,
            "new_id": new_id,
            "new_num": new_num,
            "ch_index": ch_idx,
            "ch_name": ch_name,
            "clean_title": clean_title
        })
        
    # 4. Second pass: Update body article IDs, H2s, badges, and cross-links
    for info in art_info_list:
        art = info["element"]
        new_id = info["new_id"]
        new_num = info["new_num"]
        ch_name = info["ch_name"]
        clean_title = info["clean_title"]
        
        # Update id
        art["id"] = new_id
        
        # Update H2
        h2 = art.find("h2")
        if h2:
            h2.string = f"{ch_name} Question {new_num}. {clean_title}"
            
        # Update Category Badge inside body
        path_container = art.select_one(".category-path-container")
        if path_container:
            badge = path_container.select_one(".category-badge")
            if badge:
                # Remove brackets for badge display
                badge.string = ch_name.replace("[", "").replace("]", "")
                
    # Update all internal cross-reference links (href="#old_id" -> href="#new_id")
    cross_links_updated = 0
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("#"):
            target_id = href[1:]
            if target_id in old_id_to_new_id:
                a["href"] = f"#{old_id_to_new_id[target_id]}"
                cross_links_updated += 1
    print(f"Updated {cross_links_updated} internal cross-reference links in body.")
    
    # 5. Third pass: Rebuild sidebar navigation items with correct numbering
    for ch in chapter_info:
        container = ch["container"]
        header = container.find("div", class_="nav-chapter-header")
        content_ul = container.find("ul", class_="nav-chapter-content")
        
        # 5.1 Re-format header range
        range_str = format_q_range(ch["new_nums"])
        range_suffix = f" ({range_str})" if range_str else ""
        
        if header:
            # Build new header text: 📁 [소방화학] (Q1~Q5)
            # Find the text span or set it directly
            # Preserve chevron icon if it exists
            span_chevron = header.find("span", class_="chevron-icon")
            
            header.clear()
            span_title = soup.new_tag("span")
            span_title.string = f"📁 {ch['name']}{range_suffix}"
            header.append(span_title)
            
            if span_chevron:
                header.append(span_chevron)
            else:
                # Add default chevron
                span_chev = soup.new_tag("span", attrs={"class": "chevron-icon"})
                span_chev.string = "▼"
                header.append(span_chev)
                
        # 5.2 Re-format questions list inside this chapter
        if content_ul:
            content_ul.clear()
            
            # Find all body articles that belong to this chapter
            ch_arts = [info for info in art_info_list if info["ch_index"] == ch["index"]]
            
            if not ch_arts:
                li = soup.new_tag("li", attrs={"class": "nav-chapter-empty"})
                li.string = "등록된 문제 없음"
                content_ul.append(li)
            else:
                for q in ch_arts:
                    li = soup.new_tag("li", attrs={"class": "nav-item"})
                    a_link = soup.new_tag("a", href=f"#{q['new_id']}", attrs={"class": "nav-link"})
                    
                    span_num = soup.new_tag("span", attrs={"class": "nav-num"})
                    span_num.string = f"Question {q['new_num']}"
                    
                    span_title = soup.new_tag("span")
                    span_title.string = q["clean_title"]
                    
                    a_link.append(span_num)
                    a_link.append(span_title)
                    li.append(a_link)
                    content_ul.append(li)
                    
    # Save back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Successfully updated and saved: {file_path}")

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        process_html_file(v2_path)
        
        # Sync to public/index.html as well
        if os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            # We can run the same process on public/index.html or copy the updated v2 file there.
            # Copying is much safer and ensures 100% equivalence!
            shutil.copy2(v2_path, public_path)
            print("Successfully copied updated HTML to public/index.html.")
        else:
            print(f"Warning: public/index.html does not exist at {public_path}")
    else:
        print(f"Error: {v2_path} does not exist!")
