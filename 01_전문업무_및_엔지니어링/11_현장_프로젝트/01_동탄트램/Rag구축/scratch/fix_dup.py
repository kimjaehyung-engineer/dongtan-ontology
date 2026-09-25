server_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if i < 2000 and "let currentViewingDoc = null;" in l:
        lines[i] = "  // currentViewingDoc declared below\n"
        print(f"Removed duplicate at line {i+1}")
        break

with open(server_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Saved server.py without duplicate declaration.")
