import sys
from pathlib import Path

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
lines = server_path.read_text(encoding='utf-8').splitlines()

print(f"Total lines: {len(lines)}")
for idx, line in enumerate(lines):
    if any(k in line.lower() for k in ["models_to_try", "gemini-flash-latest", "응답 생성 실패", "503", "models ="]):
        print(f"{idx+1}: {line}")
