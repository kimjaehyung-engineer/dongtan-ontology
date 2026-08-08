import os, sys

path_gitignore = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\.gitignore'

ignore_patterns = """
# Ignore large binary build artifacts and node_modules
*.exe
*.zip
*.asar
*.pak
node_modules/
release/
dist_exe/
dist/
win-unpacked/
win-unpacked.tmp/
"""

if os.path.exists(path_gitignore):
    with open(path_gitignore, 'r', encoding='utf-8') as f:
        content = f.read()
else:
    content = ""

if "*.exe" not in content:
    content += "\n" + ignore_patterns

with open(path_gitignore, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated gitignore successfully!")
