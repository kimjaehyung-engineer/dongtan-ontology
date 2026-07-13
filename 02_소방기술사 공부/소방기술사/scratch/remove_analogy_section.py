import os
import shutil
from bs4 import BeautifulSoup

def remove_analogy_section(file_path):
    print(f"Removing analogy section from card in: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_remove_analogy"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. Target card element
    card = soup.find(id="common_pipe_classification")
    if not card:
        print("Error: Could not find element with id='common_pipe_classification'")
        return False
        
    # 2. Find the analogy section container.
    # It starts with an h3 containing "1. 소방 배관의 성질별 직관적 비유와 이해"
    h3_analogy = None
    for h3 in card.find_all("h3"):
        if "소방 배관의 성질별 직관적 비유와 이해" in h3.text:
            h3_analogy = h3
            break
            
    if h3_analogy:
        # The analogy container is actually the div wrap around this h3 and the grid
        parent_div = h3_analogy.parent
        parent_div.decompose()
        print("Successfully removed analogy section container.")
    else:
        print("Warning: Analogy section h3 not found.")
        
    # 3. Renumber remaining section headings inside the card
    # Change "2. 소방 파이프 종류별 엔지니어링 특징 비교" -> "1. 소방 파이프 종류별 엔지니어링 특징 비교"
    for h3 in card.find_all("h3"):
        if "소방 파이프 종류별 엔지니어링 특징 비교" in h3.text:
            h3.string = "1. 소방 파이프 종류별 엔지니어링 특징 비교"
            print("Renumbered comparison table heading to '1.'")
            break
            
    # Change "3. 소방 배관의 위치별·용도별 적합 관종 종합 단면 계통도" -> "2. 소방 배관의 위치별·용도별 적합 관종 종합 단면 계통도"
    # Note: This is an h4 or h3 depending on the prior injection. Let's check both h3 and h4.
    found_map_heading = False
    for heading in card.find_all(["h3", "h4"]):
        if "소방 배관의 위치별·용도별 적합 관종 종합 단면 계통도" in heading.text:
            heading.string = "2. 소방 배관의 위치별·용도별 적합 관종 종합 단면 계통도"
            # If it's h4, let's keep it as h4 or change to h3 to match the table.
            # Let's standardize it to h3 for structural consistency!
            heading.name = "h3"
            heading['style'] = "font-size: 1.2rem; font-weight: 800; color: var(--accent); margin-top: 35px; margin-bottom: 18px; border-left: 4px solid var(--accent); padding-left: 10px;"
            print("Renumbered and standardized sectional heading of the map diagram to '2.'")
            found_map_heading = True
            break
            
    if not found_map_heading:
        print("Warning: Location map diagram heading not found.")
        
    # 4. Save back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Successfully saved updated HTML to: {file_path}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = remove_analogy_section(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied updated HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
