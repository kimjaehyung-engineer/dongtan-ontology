import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램"

def inspect_file_details(rel_path):
    full_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(full_path):
        print("File not found:", rel_path)
        return
    
    print("==================================================")
    print("FILE:", rel_path)
    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    print("Length:", len(content))
    
    # 1. Search for top bar or fixed header buttons
    top_bar = re.findall(r'<div[^>]*class=["\'][^"\']*(?:top-bar|header|nav|navbar|menu|quick)[^"\']*["\'][^>]*>.*?</div>', content, re.DOTALL | re.IGNORECASE)
    print("\n--- Header / Nav / TopBar Blocks count:", len(top_bar))
    for tb in top_bar[:3]:
        clean_tb = ' '.join(tb.split())
        print("  TOPBAR:", clean_tb[:300])

    # 2. Search for links containing 노선, 평면도, 매뉴얼, 대시보드, V1, html
    links = re.findall(r'<a [^>]*>.*?</a>|<button [^>]*>.*?</button>', content, re.DOTALL | re.IGNORECASE)
    print(f"\n--- Links / Buttons total count: {len(links)} ---")
    for l in links:
        if any(k in l for k in ['노선', '평면도', '매뉴얼', '대시보드', 'V1', 'v1', 'html', 'Time', '공정표', 'href', 'onclick']):
            clean_l = ' '.join(l.split())
            if len(clean_l) < 300:
                print("  MATCH BTN/LINK:", clean_l)

inspect_file_details(r"08.메뉴얼 및 평면도\동탄트램_업무_매뉴얼.html")
inspect_file_details(r"08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html")
inspect_file_details(r"09_공정표\동탄트램_Time_Chainage_공정표_대시보드.html")
