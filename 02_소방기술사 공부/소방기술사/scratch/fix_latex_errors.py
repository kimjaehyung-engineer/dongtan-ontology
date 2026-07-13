import re
import os
import shutil

def fix_latex_errors(file_path):
    print(f"Fixing LaTeX escaping and ext typos inside: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_latex_fix"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    # Keep track of changes
    original_len = len(content)
    
    # 1. Fix "1.2extMPa" and other direct html typos
    # Sometimes it might be "1.2extMPa", "1.2 extMPa", or "1.2\text{MPa}" in plain HTML or title
    content = content.replace("1.2extMPa", "1.2 MPa")
    content = content.replace("1.2ext", "1.2 MPa")
    content = content.replace("1.2\\text{MPa}", "1.2 MPa")
    content = content.replace("1.2\\text{ MPa}", "1.2 MPa")
    
    # 2. Fix tab-escaped "ext{" (the tab character \t followed by ext{ which should be \text{)
    # \t is ASCII 9. re.sub using raw strings.
    content = re.sub(r'\t+ext\{', r'\\text{', content)
    
    # 3. Fix backslash-missing "ext{" when not part of standard words (e.g. (?<![a-zA-Z\\])ext{ -> \text{)
    content = re.sub(r'(?<![a-zA-Z\\])ext\{', r'\\text{', content)
    
    # 4. Fix any other tab-corrupted latex commands like \theta becoming \t-heta
    # We will look for \t-heta (tab + heta) and replace with \theta
    content = re.sub(r'\t+heta', r'\\theta', content)
    
    # \tau becoming \t-au
    content = re.sub(r'\t+au', r'\\tau', content)
    
    # \times becoming \t-imes
    content = re.sub(r'\t+imes', r'\\times', content)
    
    # \total becoming \t-otal
    content = re.sub(r'\t+otal', r'\\total', content)
    
    # 5. Save back
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"LaTeX escape fix completed. File saved. Size change: {original_len} -> {len(content)}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = fix_latex_errors(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied fixed HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
