import json
import os
import sys
import time
import urllib.request
import base64

sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path
rag_dir = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
sys.path.insert(0, str(rag_dir))

from server import DOCS_DIR, get_smart_pdf_payload

env_path = rag_dir / ".env"
api_key = ""
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()

target_doc = DOCS_DIR / "기본설계 시추주상도(1공구)_45공.pdf"
query = "차량기지 시추주상도 알려줘"

pdf_bytes, info_msg, is_meta_only = get_smart_pdf_payload(target_doc, query)
pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")

print(f"Sending payload ({len(pdf_b64)} chars) to Gemini API...")
t0 = time.time()

model_name = "gemini-flash-lite-latest"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
req_body = {
    "systemInstruction": {
        "parts": [{
            "text": "당신은 토목 엔지니어링 전문 AI입니다. 제공된 시추주상도를 간결하게 표로 정리하세요."
        }]
    },
    "contents": [
        {
            "role": "user",
            "parts": [
                {"inline_data": {"mime_type": "application/pdf", "data": pdf_b64}},
                {"text": query}
            ]
        }
    ]
}

req = urllib.request.Request(
    url,
    data=json.dumps(req_body).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req, timeout=90) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    reply = data["candidates"][0]["content"]["parts"][0]["text"]
    elapsed = time.time() - t0
    print(f"API call succeeded in: {elapsed:.2f}s")
    print(f"Reply sample: {reply[:200]}...")
