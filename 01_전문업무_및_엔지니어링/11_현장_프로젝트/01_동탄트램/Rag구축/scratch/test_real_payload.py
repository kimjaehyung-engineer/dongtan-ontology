import sys, os, urllib.request, json, time, base64
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
rag_dir = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
sys.path.insert(0, str(rag_dir))
import server

env_file = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\.env")
api_key = ""
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()

query = "동탄역 핵심이슈는 머지?"
# Target doc
root = server.get_configured_docs_root()
fp = root / "02_기본설계_기술제안" / "기본설계 기술제안_ 건축.pdf"
if not fp.exists():
    matches = list(root.rglob("기본설계 기술제안_ 건축.pdf"))
    fp = matches[0]

pdf_bytes, info_msg, is_meta = server.get_smart_pdf_payload(fp, query)
print(f"pdf_bytes size: {len(pdf_bytes)} bytes")
pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")
print(f"b64 size: {len(pdf_b64)} chars ({len(pdf_b64)/1024/1024:.2f} MB)")

system_prompt = (
    "당신은 철도/건축 엔지니어링 전문가입니다. 핵심 내용을 3줄로 요약하세요."
)

models = ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-flash-latest", "gemini-3.8-flash"]

for m in models:
    print(f"\n---> Testing model {m} with 8.9MB inline PDF...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
    req_body = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"inline_data": {"mime_type": "application/pdf", "data": pdf_b64}},
                    {"text": query}
                ]
            }
        ],
        "generationConfig": {"temperature": 0.2}
    }
    t0 = time.time()
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(req_body).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            ans = data["candidates"][0]["content"]["parts"][0]["text"]
            print(f"[{m}] SUCCESS ({time.time()-t0:.2f}s)! Length: {len(ans)} chars")
            print(ans[:150])
            break
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="ignore")
        print(f"[{m}] HTTPError {e.code} ({time.time()-t0:.2f}s): {err[:200]}")
    except Exception as e:
        print(f"[{m}] Exception ({time.time()-t0:.2f}s): {e}")
