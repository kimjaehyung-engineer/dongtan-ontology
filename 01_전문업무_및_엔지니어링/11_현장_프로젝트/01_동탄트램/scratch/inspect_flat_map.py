import os

def inspect_map():
    filepath = "08.메뉴얼 및 평면도/동탄트램_노선평면도.html"
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Search for iframe, fetch, and .html references
    lines = content.split('\n')
    print("=== HTML/iframe/fetch references in 동탄트램_노선평면도.html ===")
    for idx, line in enumerate(lines):
        if 'iframe' in line.lower() or 'fetch(' in line.lower() or '.html' in line or '.png' in line:
            print(f"Line {idx+1}: {line.strip()}")

if __name__ == '__main__':
    inspect_map()
