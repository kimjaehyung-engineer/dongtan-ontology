import subprocess
import time
import os
import re
import sys
from pathlib import Path

# 콘솔 UTF-8 출력 강제
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

RAG_DIR = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
EXE_PATH = RAG_DIR / "cloudflared.exe"
LOG_FILE = RAG_DIR / "tunnel.log"
URL_FILE = RAG_DIR / "public_url.txt"

# 1. 기존 cloudflared 프로세스 종료
subprocess.run("taskkill /F /IM cloudflared.exe", shell=True, capture_output=True)
time.sleep(1)

# 2. 터널 백그라운드 실행
print("Starting Cloudflare Tunnel...")
with open(LOG_FILE, "w", encoding="utf-8") as f_log:
    p = subprocess.Popen(
        [str(EXE_PATH), "tunnel", "--url", "http://127.0.0.1:8080"],
        cwd=str(RAG_DIR),
        stdout=f_log,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.DETACHED_PROCESS if os.name == "nt" else 0
    )

print(f"Cloudflared PID: {p.pid}")

# 3. URL 발급 대기 (최대 20초)
tunnel_url = None
for _ in range(20):
    time.sleep(1)
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                matches = re.findall(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', content)
                if matches:
                    tunnel_url = matches[0]
                    break
        except Exception:
            pass

if tunnel_url:
    print(f"\n============================================================")
    print(f"🎉 [동탄트램 RAG 외부 안전 공인 주소 발급 성공!]")
    print(f"• 공인 HTTPS 주소: {tunnel_url}")
    print(f"• 카카오 웹훅 주소: {tunnel_url}/api/kakao/webhook")
    print(f"• 모바일 웹 접속 : {tunnel_url}")
    print(f"============================================================")
    with open(URL_FILE, "w", encoding="utf-8") as f:
        f.write(tunnel_url)
else:
    print("URL 발급 대기 시간 초과. tunnel.log 내용을 확인해 주세요.")
    if LOG_FILE.exists():
        with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
            print(f.read()[:500])
