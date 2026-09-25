import os
import json
import time
import hashlib
import shutil
import tempfile
from pathlib import Path
from google import genai

CACHE_FILE = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\_gemini_files_cache.json")

def load_cache():
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache_data):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Failed to save gemini file cache:", e)

def get_or_upload_file(client: genai.Client, file_path: Path):
    """
    Google GenAI Files API를 사용하여 파일을 1회 업로드하고 캐싱합니다.
    - 파일이 이미 업로드되어 있고 48시간 이내라면 구글 서버의 기존 File 참조를 반환합니다.
    - 만료되었거나 캐시가 없으면 새로 업로드하고 캐시를 갱신합니다.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    stat = file_path.stat()
    cache_key = f"{file_path.name}_{stat.st_size}_{stat.st_mtime}"
    cache = load_cache()

    now = time.time()

    if cache_key in cache:
        entry = cache[cache_key]
        file_name = entry.get("file_name")
        uploaded_at = entry.get("uploaded_at", 0)
        
        # 46시간 이내(Google File API 유지기간 48시간 대비 여유)인지 확인
        if file_name and (now - uploaded_at) < (46 * 3600):
            try:
                remote_file = client.files.get(name=file_name)
                if remote_file and remote_file.state.name == "ACTIVE":
                    print(f"[GeminiFileManager] Using cached Google File: {file_name} ({file_path.name})")
                    return remote_file
            except Exception as e:
                print(f"[GeminiFileManager] Cached file check failed ({e}), re-uploading...")

    print(f"[GeminiFileManager] Uploading {file_path.name} ({stat.st_size / (1024*1024):.1f}MB) to Google GenAI...")
    
    # 한글 파일명으로 인한 HTTP 헤더 ascii codec error 방지: 영문 안전 링크/복사본 활용
    safe_name = f"doc_{hashlib.md5(file_path.name.encode('utf-8')).hexdigest()[:10]}.pdf"
    temp_dir = Path(tempfile.gettempdir()) / "rag_safe_uploads"
    temp_dir.mkdir(exist_ok=True)
    safe_file_path = temp_dir / safe_name

    if not safe_file_path.exists() or safe_file_path.stat().st_size != stat.st_size:
        try:
            os.link(str(file_path), str(safe_file_path))
        except Exception:
            shutil.copy2(str(file_path), str(safe_file_path))

    uploaded_file = client.files.upload(file=str(safe_file_path))

    # 업로드 후 ACTIVE 상태 대기 (대용량의 경우 PROCESSING 상태일 수 있음)
    wait_count = 0
    while uploaded_file.state.name == "PROCESSING" and wait_count < 30:
        time.sleep(2)
        wait_count += 1
        uploaded_file = client.files.get(name=uploaded_file.name)

    if uploaded_file.state.name != "ACTIVE":
        raise RuntimeError(f"File upload failed or stuck in state: {uploaded_file.state.name}")

    cache[cache_key] = {
        "file_name": uploaded_file.name,
        "uri": uploaded_file.uri,
        "doc_name": file_path.name,
        "size_mb": round(stat.st_size / (1024 * 1024), 2),
        "uploaded_at": now
    }
    save_cache(cache)
    print(f"[GeminiFileManager] Successfully uploaded and cached: {uploaded_file.name}")
    return uploaded_file

if __name__ == "__main__":
    print("Gemini File Manager Ready.")
