with open(r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\Rag구축\extracted.js", "r", encoding="utf-8") as f:
    js = f.read()

for kw in ["appendMessage", "scrollToBottom", "escapeHtml"]:
    pos = js.find(kw)
    print(f"{kw} at {pos}")
