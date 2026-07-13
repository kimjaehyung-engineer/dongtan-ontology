import re
from bs4 import BeautifulSoup

def diagnose():
    html_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        
    articles = soup.find_all("article")
    print(f"Total articles in body: {len(articles)}")
    
    # Analyze body articles
    body_qs = []
    for idx, art in enumerate(articles):
        q_id = art.get("id", "NO_ID")
        h2 = art.find("h2")
        h2_text = h2.get_text(strip=True) if h2 else "NO_H2"
        
        # Check badge/category
        badge_text = ""
        badge = art.select_one(".category-badge")
        if badge:
            badge_text = badge.get_text(strip=True)
            
        body_qs.append({
            "index": idx + 1,
            "id": q_id,
            "h2": h2_text,
            "badge": badge_text
        })
        
    # Analyze sidebar
    sidebar_qs = []
    chapters = []
    
    # Try finding nav-chapter-container or ul.nav-list
    containers = soup.find_all("div", class_="nav-chapter-container")
    if containers:
        print(f"Found {len(containers)} nav-chapter-containers in sidebar.")
        for c_idx, container in enumerate(containers):
            header = container.find("div", class_="nav-chapter-header")
            header_text = header.get_text(strip=True) if header else f"Chapter {c_idx+1}"
            
            # Find all links inside this chapter
            links = container.find_all("a", class_="nav-link")
            ch_links = []
            for link in links:
                href = link.get("href", "")
                q_num_el = link.find(class_="nav-num")
                q_num = q_num_el.get_text(strip=True) if q_num_el else ""
                
                # Title part
                spans = link.find_all("span")
                if len(spans) >= 2:
                    q_title = spans[1].get_text(strip=True)
                else:
                    q_title = link.get_text(strip=True).replace(q_num, "").strip()
                    
                ch_links.append({
                    "href": href,
                    "num": q_num,
                    "title": q_title
                })
                sidebar_qs.append({
                    "chapter": header_text,
                    "href": href,
                    "num": q_num,
                    "title": q_title
                })
            chapters.append({
                "name": header_text,
                "links": ch_links
            })
    else:
        # Fallback to simple nav-list
        nav_list = soup.find("ul", class_="nav-list")
        if nav_list:
            print("Found simple ul.nav-list in sidebar.")
            links = nav_list.find_all("a", class_="nav-link")
            for link in links:
                href = link.get("href", "")
                q_num_el = link.find(class_="nav-num")
                q_num = q_num_el.get_text(strip=True) if q_num_el else ""
                
                spans = link.find_all("span")
                if len(spans) >= 2:
                    q_title = spans[1].get_text(strip=True)
                else:
                    q_title = link.get_text(strip=True).replace(q_num, "").strip()
                    
                sidebar_qs.append({
                    "chapter": "N/A",
                    "href": href,
                    "num": q_num,
                    "title": q_title
                })
        else:
            print("No sidebar navigation structure found!")

    # Print out summary to a diagnostic file
    with open("scratch/diagnose_output.txt", "w", encoding="utf-8") as out:
        out.write(f"=== BODY ARTICLES ({len(body_qs)}) ===\n")
        for q in body_qs:
            out.write(f"#{q['index']} ID: {q['id']} | Badge: {q['badge']} | H2: {q['h2']}\n")
            
        out.write(f"\n=== SIDEBAR QUESTIONS ({len(sidebar_qs)}) ===\n")
        for idx, q in enumerate(sidebar_qs):
            out.write(f"#{idx+1} Chapter: {q['chapter']} | Href: {q['href']} | Num: {q['num']} | Title: {q['title']}\n")
            
        if chapters:
            out.write("\n=== CHAPTERS DETAIL ===\n")
            for idx, ch in enumerate(chapters):
                out.write(f"\nCh {idx+1}. {ch['name']} (Count: {len(ch['links'])})\n")
                for link in ch['links']:
                    out.write(f"  - {link['num']} | Href: {link['href']} | Title: {link['title']}\n")
                    
    print("Diagnostics written to scratch/diagnose_output.txt")

if __name__ == "__main__":
    diagnose()
