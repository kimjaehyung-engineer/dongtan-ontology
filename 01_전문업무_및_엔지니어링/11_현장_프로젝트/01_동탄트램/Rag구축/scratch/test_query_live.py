import urllib.request
import json
import time

url = "http://127.0.0.1:8080/api/chat"
payload = {
    "query": "동탄역 핵심이슈는 머지?"
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    print("Sending query to /api/chat...")
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"Status 200 in {time.time()-t0:.2f}s!")
        print("Reply preview:", data.get("reply", "")[:200])
except urllib.error.HTTPError as e:
    print(f"HTTPError {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
