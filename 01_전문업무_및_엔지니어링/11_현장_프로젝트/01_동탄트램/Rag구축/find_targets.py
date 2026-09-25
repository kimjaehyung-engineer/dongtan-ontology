target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(target_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

targets = [
    "function fetchDocs",
    "function selectDoc",
    "function selectAllDocsMode",
    "function sendQuery",
    "function loadViewerDoc",
    "function downloadActiveDoc",
    ".doc-item.active",
    ".doc-item {"
]

for i, l in enumerate(lines):
    for t in targets:
        if t in l:
            print(f"Line {i+1}: {l.strip()[:80]}")
