import sys
sys.stdout.reconfigure(encoding="utf-8")

with open(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py.bak", "r", encoding="utf-8") as f:
    code = f.read()

pos = code.find("function appendMessage")
print(code[pos:pos+600])
