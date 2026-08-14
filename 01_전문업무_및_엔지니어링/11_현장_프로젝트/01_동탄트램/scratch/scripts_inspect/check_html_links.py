import os
import re

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램"

files_to_check = [
    r"08.메뉴얼 및 평면도\동탄트램_업무_매뉴얼.html",
    r"08.메뉴얼 및 평면도\동탄트램 노선평면도\동탄트램_노선평면도V1.html",
    r"08.메뉴얼 및 평면도\동탄트램_업무_매뉴얼_로드맵.html",
    r"08.메뉴얼 및 평면도\동탄트램_정거장_노반_분리형_공정_매뉴얼_포털.html",
    r"08.메뉴얼 및 평면도\deploy\dongtan_dashboard.html",
    r"08.메뉴얼 및 평면도\restored_dashboard.html"
]

print("=== CHECKING HTML LINKS AND REFERENCES ===")

for rel_path in files_to_check:
    full_path = os.path.join(base_dir, rel_path)
    if os.path.exists(full_path):
        print(f"\n--- File: {rel_path} ---")
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # 1. Search href / onclick / window.open
        hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
        onclicks = re.findall(r'window\.open\(["\']([^"\']+)["\']', content)
        locs = re.findall(r'location\.href\s*=\s*["\']([^"\']+)["\']', content)
        
        all_links = set([l for l in hrefs + onclicks + locs if '.html' in l or 'http' in l or '?' in l])
        print("  Extracted Links:")
        for l in sorted(all_links):
            print("    -", l)
            
        # 2. Search for 노선평면도 in text
        matches = re.findall(r'.{0,30}노선평면도.{0,30}', content)
        if matches:
            print("  '노선평면도' snippet samples (up to 5):")
            for m in matches[:5]:
                print("    *", m.strip())
