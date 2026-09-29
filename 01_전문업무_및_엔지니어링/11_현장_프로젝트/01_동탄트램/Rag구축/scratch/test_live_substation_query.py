# -*- coding: utf-8 -*-
import sys, json, urllib.request, time
sys.stdout.reconfigure(encoding="utf-8")

url = "http://127.0.0.1:8080/api/chat"
query = "301정거장 변전소에 대한 제안사항을 물어봣어. 전기, 건축, 토질/기초, 구조 등 전 공종의 제안사항을 비교 정리해줘."

payload = {
    "query": query,
    "user_id": "test_user"
}

print(f"Sending live query to {url}...")
start_time = time.time()
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        elapsed = time.time() - start_time
        print(f"\n[Response Received in {elapsed:.2f}s]")
        print("Source Document:", data.get("source_document"))
        print("Matched Sections:", data.get("matched_sections"))
        print("\n--- REPLY ---")
        print(data.get("reply", ""))
        if data.get("trace"):
            print("\n--- TRACE ---")
            for step in data["trace"].get("steps", []):
                print(f"Step {step.get('step')}: {step.get('title')} ({step.get('badge')})")
except Exception as e:
    print("Error:", e)
