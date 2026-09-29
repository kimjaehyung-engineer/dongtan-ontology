import os
import json
import urllib.request

env_file = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\.env"
api_key = ""
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                api_key = line.strip().split("=", 1)[1].strip("\"'")
                break

payload = {
    "query": "동탄 트램 총 연장은 얼마인가요?",
    "api_key": api_key
}

req = urllib.request.Request(
    "http://127.0.0.1:8080/api/chat",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    print("Sending query to http://127.0.0.1:8080/api/chat with timeout=90s...")
    with urllib.request.urlopen(req, timeout=90) as res:
        data = json.loads(res.read().decode("utf-8"))
        print("\nResponse received successfully!")
        print("Response keys:", list(data.keys()))
        if "usage" in data:
            print("Usage data:", json.dumps(data["usage"], indent=2, ensure_ascii=False))
        if "reply" in data:
            print("\nReply excerpt:\n", data["reply"][:200], "...")
        elif "answer" in data:
            print("\nAnswer excerpt:\n", data["answer"][:200], "...")
except Exception as e:
    print("Error during request:", e)
