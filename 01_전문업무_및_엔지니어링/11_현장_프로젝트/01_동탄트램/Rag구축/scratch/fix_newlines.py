# -*- coding: utf-8 -*-
server_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Fix newline in prompt
text = text.replace(
    "const name = prompt('생성할 새 폴더명을 입력하세요:\n(예: 05. 정거장 건축설계 / 06. 트램 궤도공사)');",
    "const name = prompt('생성할 새 폴더명을 입력하세요 (예: 05. 정거장 건축설계 / 06. 트램 궤도공사):');"
)

# Also check promptMoveDocFolder message
text = text.replace(
    "const msg = \"'\" + docName + \"' 문서를 이동할 폴더 번호를 입력하거나 새 폴더명을 입력하세요:\\n\\n\" + \n      allFolders.map((f, i) => (i + 1) + '. ' + f).join('\\n');",
    "const msg = `'${docName}' 문서를 이동할 폴더 번호를 입력하거나 새 폴더명을 입력하세요:\\n\\n` + allFolders.map((f, i) => (i + 1) + '. ' + f).join('\\n');"
)

with open(server_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed prompt string newlines!")
