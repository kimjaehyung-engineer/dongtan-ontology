import os
import shutil
from bs4 import BeautifulSoup

def fix_table_borders(file_path):
    print(f"Applying soft borders to all tables inside: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_table_borders"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 1. Inject Premium Soft Table Border CSS into first style tag
    style_tag = soup.find("style")
    if style_tag:
        table_css = """
        /* Premium Soft Table Grid Borders */
        table, .comparison-table, .data-table, .premium-table {
            width: 100% !important;
            border-collapse: collapse !important;
            margin: 24px 0 !important;
            border: 1px solid var(--border) !important;
            background-color: var(--bg-primary) !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.02) !important;
            border-radius: 8px !important;
            overflow: hidden !important;
        }
        table th, .comparison-table th, .data-table th, .premium-table th {
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            font-weight: 800 !important;
            text-align: center !important;
            padding: 12px 16px !important;
            border: 1px solid var(--border) !important;
            font-size: 0.9rem !important;
        }
        table td, .comparison-table td, .data-table td, .premium-table td {
            padding: 12px 16px !important;
            color: var(--text-secondary) !important;
            line-height: 1.6 !important;
            border: 1px solid var(--border) !important;
            font-size: 0.88rem !important;
            background-color: var(--bg-primary) !important;
        }
        /* Zebra striping for premium look */
        table tr:nth-child(even) td, 
        .comparison-table tr:nth-child(even) td, 
        .data-table tr:nth-child(even) td, 
        .premium-table tr:nth-child(even) td {
            background-color: rgba(var(--accent-rgb), 0.01) !important;
        }
        """
        style_tag.append(table_css)
        print("Table border CSS injected.")
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Successfully saved updated HTML to: {file_path}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = fix_table_borders(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied updated HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
