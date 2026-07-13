import os
import re
import shutil
from bs4 import BeautifulSoup

def sync_dashboard(file_path):
    print(f"Syncing dashboard with sidebar in: {file_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. 28개 챕터별 아이콘(이모지) 및 색상 매핑 정의
    icon_map = {
        "소방화학": "🧪",
        "연소공학": "🔥",
        "열전달": "🌡️",
        "방폭공학": "🛡️",
        "유체역학": "🌊",
        "배관재료": "🔧",
        "배관설계": "📐",
        "소방펌프": "⚙️",
        "수계일반": "💧",
        "스프링클러설비": "🚿",
        "물분무": "🌫️",
        "포 소화설비": "🫧",
        "가스계 소화설비": "💨",
        "분말": "📦",
        "연기의 특성": "☁️",
        "제연설비": "🌀",
        "화재경보설비": "🚨",
        "소방전기설비": "🔌",
        "비상전원": "⚡",
        "위험물": "☣️",
        "실내화재": "🏠",
        "건축방화": "🧱",
        "건축피난": "🏃",
        "방재대책": "⚠️",
        "성능위주설계": "🎯",
        "위험성평가": "📊",
        "소방법령": "📜",
        "소방실무": "💼"
    }
    
    colors = [
        "#EF4444", "#3B82F6", "#10B981", "#06B6D4", "#8B5CF6", 
        "#F59E0B", "#EC4899", "#14B8A6", "#6366F1", "#F97316"
    ]
    
    def get_icon(ch_title):
        for key, val in icon_map.items():
            if key in ch_title:
                return val
        return "📁"
        
    # 2. Extract chapters and questions from sidebar
    chapters_data = []
    containers = soup.find_all("div", class_="nav-chapter-container")
    print(f"Found {len(containers)} chapter containers in sidebar.")
    
    for c_idx, container in enumerate(containers):
        header = container.find("div", class_="nav-chapter-header")
        header_text = header.get_text(strip=True) if header else f"Chapter {c_idx+1}"
        
        # Parse chapter title and range
        # e.g. "📁 [소방화학] (Q1~Q5)" -> title="[소방화학]", range="Q1~Q5"
        ch_title = header_text.replace("📁", "").strip()
        ch_range = ""
        
        range_match = re.search(r"\((Q\d+[^)]*)\)", ch_title)
        if range_match:
            ch_range = range_match.group(1)
            ch_title = ch_title.replace(range_match.group(0), "").strip()
            
        ch_title = re.sub(r"▼|▲", "", ch_title).strip()
        
        # Get questions
        questions = []
        links = container.find_all("a", class_="nav-link")
        for link in links:
            href = link.get("href", "")
            q_num_el = link.find(class_="nav-num")
            q_num_text = q_num_el.get_text(strip=True) if q_num_el else ""
            
            # Extract only digits from "Question XX"
            q_num = re.sub(r"[^\d]", "", q_num_text)
            
            # Extract title
            spans = link.find_all("span")
            if len(spans) >= 2:
                q_title = spans[1].get_text(strip=True)
            else:
                q_title = link.get_text(strip=True).replace(q_num_text, "").strip()
                
            # Truncate title if too long to look clean in dashboard card
            if len(q_title) > 28:
                q_title = q_title[:26] + "..."
                
            questions.append({
                "id": href.replace("#", ""),
                "num": q_num,
                "title": q_title
            })
            
        chapters_data.append({
            "index": c_idx + 1,
            "title": ch_title,
            "range": ch_range if ch_range else "등록된 문제 없음",
            "icon": get_icon(ch_title),
            "color": colors[c_idx % len(colors)],
            "questions": questions
        })
        
    # 3. Build new Dashboard Grid Container HTML
    grid_html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-bottom: 40px;">\n'
    
    for ch in chapters_data:
        rgb_style = "background: var(--bg-primary); border: 1px solid var(--border); border-radius: 12px; padding: 20px; box-shadow: var(--shadow-xs); transition: all 0.3s ease;"
        
        grid_html += f'<!-- 카테고리 {ch["index"]}: {ch["title"]} -->\n'
        grid_html += f'<div class="dashboard-card" style="{rgb_style}">\n'
        grid_html += f'  <h4 style="margin: 0 0 12px 0; font-size: 0.95rem; font-weight: 700; color: {ch["color"]}; border-bottom: 1.5px solid var(--border); padding-bottom: 8px; display: flex; justify-content: space-between;">\n'
        grid_html += f'    <span>{ch["icon"]} {ch["title"]}</span>\n'
        grid_html += f'    <span style="font-size: 0.8rem; background: rgba(120, 120, 120, 0.08); color: var(--text-secondary); padding: 1px 6px; border-radius: 4px;">{ch["range"]}</span>\n'
        grid_html += '  </h4>\n'
        grid_html += '  <ul style="list-style: none; padding: 0; margin: 0; font-size: 0.85rem; line-height: 1.8;">\n'
        
        if ch["questions"]:
            for q in ch["questions"]:
                grid_html += f'    <li style="margin-bottom: 6px;"><a href="#{q["id"]}" style="color: var(--text-primary); text-decoration: none; display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"><strong>Q{q["num"]}.</strong> {q["title"]}</a></li>\n'
        else:
            grid_html += '    <li style="margin-bottom: 6px; color: var(--text-muted); font-style: italic;">등록된 문제 없음</li>\n'
            
        grid_html += '  </ul>\n'
        grid_html += '</div>\n'
        
    grid_html += '</div>'
    
    # 4. Find the original dashboard container and replace it in the soup
    # Search for the div having 'grid-template-columns' and '280px' (or repeat(auto-fill, ...))
    grid_element = soup.find(lambda tag: tag.name == 'div' and tag.get('style') and 'grid-template-columns' in tag.get('style'))
    
    if grid_element:
        # Create a new BeautifulSoup tag with the grid content and replace
        new_soup = BeautifulSoup(grid_html, "html.parser")
        grid_element.replace_with(new_soup.div)
        print("Successfully replaced original dashboard container in DOM.")
        
        # Save back to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Successfully wrote synced dashboard to: {file_path}")
        return True
    else:
        print("Error: Could not find original grid dashboard container in HTML.")
        return False

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = sync_dashboard(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied synced HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
