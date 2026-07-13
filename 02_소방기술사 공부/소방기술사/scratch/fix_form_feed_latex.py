import os
import shutil

def fix_form_feed_latex(file_path):
    print(f"Fixing Form Feed (\\x0c) LaTeX errors inside: {file_path}")
    
    # 0. Backup
    backup_path = file_path + ".bak_form_feed_fix"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    original_len = len(content)
    
    # 1. Replace form feed character (\x0c) + rac with \\frac
    # In python string: '\x0crac' or '\frac' when unescaped.
    # Let's target the exact byte sequence or characters.
    # ASCII Form Feed is \x0c. We can search for '\x0crac'
    
    # Check count of occurrences
    count = content.count('\x0crac')
    print(f"Found {count} occurrences of '\\x0crac' (form feed + rac)")
    
    content = content.replace('\x0crac', '\\frac')
    
    # Let's also check for other \x0c occurrences in case there are others
    x0c_count = content.count('\x0c')
    print(f"Remaining '\\x0c' characters: {x0c_count}")
    
    # If there are any remaining \x0c, let's see where they are
    if x0c_count > 0:
        # If it's followed by alphabetic characters, it's likely a broken command
        content = content.replace('\x0c', '\\f')
        print("Replaced all remaining '\\x0c' with '\\f'")
        
    # 2. Save back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Form Feed fix completed. Size change: {original_len} -> {len(content)}")
    return True

if __name__ == "__main__":
    v2_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\소방기술사 비주얼 싱킹 최다빈출_모범답안v2.html"
    public_path = r"c:\Users\sskjh\antigravity\02_소방기술사 공부\소방기술사\public\index.html"
    
    if os.path.exists(v2_path):
        success = fix_form_feed_latex(v2_path)
        
        if success and os.path.exists(public_path):
            print(f"\nSyncing updated HTML directly to public/index.html...")
            shutil.copy2(v2_path, public_path)
            print("Successfully copied fixed HTML to public/index.html.")
    else:
        print(f"Error: {v2_path} does not exist!")
