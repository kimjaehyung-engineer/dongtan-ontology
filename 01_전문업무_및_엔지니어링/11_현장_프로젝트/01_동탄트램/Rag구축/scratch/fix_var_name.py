from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

old_code = "file_ref = gemini_file_manager.get_or_upload_file(client, file_path)"
new_code = "file_ref = gemini_file_manager.get_or_upload_file(client, target_file_path)"

if old_code in content:
    content = content.replace(old_code, new_code)
    server_path.write_text(content, encoding="utf-8")
    print("Fixed file_path -> target_file_path successfully!")
else:
    print("Pattern not found!")
