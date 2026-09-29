import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx1 = text.find('📂 현장 기술문서 보관소')
idx2 = text.find('<div class="sidebar-footer">')
print(text[idx1-50:idx2])
