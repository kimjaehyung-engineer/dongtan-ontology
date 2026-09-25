server_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

with open("scratch/inspect_render_tree.txt", "w", encoding="utf-8") as out:
    for j in range(1830, min(len(lines), 2000)):
        out.write(f"{j+1}: {lines[j]}")

print("Saved inspect_render_tree.txt")
