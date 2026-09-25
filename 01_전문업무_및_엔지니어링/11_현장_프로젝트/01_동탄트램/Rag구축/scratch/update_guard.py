from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
text = server_path.read_text(encoding="utf-8")
target = "if os.path.exists(py314_exe) and sys.executable.lower() != py314_exe.lower():"
replacement = "if __name__ == '__main__' and os.path.exists(py314_exe) and sys.executable.lower() != py314_exe.lower():"

if target in text:
    text = text.replace(target, replacement, 1)
    server_path.write_text(text, encoding="utf-8")
    print("Updated guard condition to check __name__ == '__main__'!")
else:
    print("Target already updated or not found.")
