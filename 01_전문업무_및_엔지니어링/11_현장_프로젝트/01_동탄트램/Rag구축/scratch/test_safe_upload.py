import hashlib
import shutil
import tempfile
from pathlib import Path
from google import genai
import os

pdf_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\documents\#3편 증빙자료_토질 및 기초.pdf")
print("Target file exists:", pdf_path.exists(), pdf_path.stat().st_size)

# API Key 로드
api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    env_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\.env")
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("GEMINI_API_KEY="):
                api_key = line.split("=", 1)[1].strip()

client = genai.Client(api_key=api_key)

# 영문 안전 파일명으로 임시 생성 또는 config 전달
safe_name = f"doc_{hashlib.md5(pdf_path.name.encode('utf-8')).hexdigest()[:8]}.pdf"
print("Safe name:", safe_name)

# 임시 폴더에 영문명으로 하드링크 또는 복사
temp_dir = Path(tempfile.gettempdir()) / "rag_safe_uploads"
temp_dir.mkdir(exist_ok=True)
safe_file_path = temp_dir / safe_name

if not safe_file_path.exists() or safe_file_path.stat().st_size != pdf_path.stat().st_size:
    print("Creating safe link/copy...")
    try:
        os.link(str(pdf_path), str(safe_file_path))
    except Exception:
        shutil.copy2(str(pdf_path), str(safe_file_path))

print("Uploading safe file:", safe_file_path)
uploaded = client.files.upload(file=str(safe_file_path))
print("Uploaded file name:", uploaded.name, "state:", uploaded.state.name)
