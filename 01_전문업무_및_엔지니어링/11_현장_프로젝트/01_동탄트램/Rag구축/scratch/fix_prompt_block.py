# -*- coding: utf-8 -*-
server_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

bad_block = """    const msg = "'" + docName + "' 문서를 이동할 폴더 번호를 입력하거나 새 폴더명을 입력하세요:

" + 
      allFolders.map((f, i) => (i + 1) + '. ' + f).join('
');"""

good_block = """    const folderListStr = allFolders.map((f, i) => `${i + 1}. ${f}`).join('\\n');
    const msg = `'${docName}' 문서를 이동할 폴더 번호(또는 새 폴더명)를 입력하세요:\\n\\n` + folderListStr;"""

if bad_block in text:
    text = text.replace(bad_block, good_block)
    print("Replaced bad_block successfully!")
else:
    import re
    text = re.sub(
        r'const msg = [^\n]*문서를 이동할 폴더[\s\S]*?const selected = prompt',
        good_block + '\n    const selected = prompt',
        text
    )
    print("Regex replaced prompt message block!")

with open(server_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved server.py cleanly!")
