from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

old_models = 'models_to_try = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash"]'
new_models = 'models_to_try = ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-flash-latest"]'

if old_models in content:
    content = content.replace(old_models, new_models)
    server_path.write_text(content, encoding="utf-8")
    print("Updated models_to_try in server.py to gemini-3.6-flash!")
else:
    import re
    content = re.sub(
        r'models_to_try\s*=\s*\["gemini-2\.0-flash"[^\]]+\]',
        new_models,
        content
    )
    server_path.write_text(content, encoding="utf-8")
    print("Updated models_to_try via regex!")
