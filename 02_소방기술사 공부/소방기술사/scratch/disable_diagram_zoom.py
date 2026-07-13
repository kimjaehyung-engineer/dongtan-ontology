import os
import shutil
from bs4 import BeautifulSoup

def disable_diagram_zoom(file_path):
    print(f"Disabling zoom overlay on interactive diagram inside: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_disable_zoom"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. Find the interactive SVG
    svg = soup.find("svg", id="pipeTreeSvg")
    if not svg:
        print("Error: Could not find SVG with id='pipeTreeSvg'")
        return False
        
    # 2. Get its parent div
    parent_div = svg.parent
    if parent_div and "zoomable-media" in parent_div.get("class", []):
        # Remove zoomable-media from class list
        classes = parent_div.get("class", [])
        classes.remove("zoomable-media")
        classes.append("interactive-pipe-container")
        parent_div["class"] = classes
        
        # Remove data-title to be safe
        if "data-title" in parent_div.attrs:
            del parent_div["data-title"]
            
        print("Successfully replaced 'zoomable-media' class with 'interactive-pipe-container' to block zoom overlay.")
    else:
        print("Warning: Parent div of SVG did not have 'zoomable-media' class or not found.")
        
    # 3. Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Successfully saved updated HTML to: {file_path}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = disable_diagram_zoom(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied updated HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
