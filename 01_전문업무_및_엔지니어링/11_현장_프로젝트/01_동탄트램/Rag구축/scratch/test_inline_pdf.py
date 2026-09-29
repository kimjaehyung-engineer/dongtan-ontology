import sys, os, urllib.request, json, time, base64
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Import get_smart_pdf_payload from server or mock it
sys.path.insert(0, r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
try:
    import server
    print("Successfully imported server!")
except Exception as e:
    print(f"Import error: {e}")

env_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\.env")
api_key = ""
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()

# Let's see what target_file_path is selected for query "동탄역 핵심이슈는 머지?"
# Let's inspect the routing / scoring logic in server
# Or let's test a simple 1-page sample PDF
import pypdf, io
writer = pypdf.PdfWriter()
writer.add_blank_page(width=100, height=100)
buf = io.BytesIO()
writer.write(buf)
sample_pdf_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

models_to_test = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-2.5-flash-lite"
]

for m in models_to_test:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
    req_body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "application/pdf",
                            "data": sample_pdf_b64
                        }
                    },
                    {
                        "text": "이 PDF는 무엇인가요? 한 줄로 답하세요."
                    }
                ]
            }
        ]
    }
    t0 = time.time()
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(req_body).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            reply = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            print(f"[{m}] SUCCESS ({time.time()-t0:.2f}s): {reply[:50]}")
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        print(f"[{m}] HTTP {e.code} ({time.time()-t0:.2f}s): {err_msg[:120]}")
    except Exception as e:
        print(f"[{m}] ERR ({time.time()-t0:.2f}s): {e}")
