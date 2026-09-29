import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx1 = text.find('function getCustomFolders() {')
idx2 = text.find('function viewDoc(name) {')
print(text[idx1:idx2])
