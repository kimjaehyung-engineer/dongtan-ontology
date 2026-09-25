import json
import time
from pathlib import Path

pdf_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\documents\#3편 증빙자료_토질 및 기초.pdf")
stat = pdf_path.stat()
cache_key = f"{pdf_path.name}_{stat.st_size}_{stat.st_mtime}"

cache_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\_gemini_files_cache.json")
cache = {}
if cache_file.exists():
    try:
        cache = json.loads(cache_file.read_text(encoding="utf-8"))
    except Exception:
        cache = {}

cache[cache_key] = {
    "file_name": "files/rpfjfbyylm31",
    "uri": "https://generativelanguage.googleapis.com/v1beta/files/rpfjfbyylm31",
    "doc_name": pdf_path.name,
    "size_mb": round(stat.st_size / (1024 * 1024), 2),
    "uploaded_at": time.time()
}

cache_file.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Registered {pdf_path.name} in cache with file_name: files/rpfjfbyylm31")
