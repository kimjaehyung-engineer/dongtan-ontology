import urllib.request
import json
import time

url = "http://localhost:8080/api/chat"
payload = {
    "query": "문서 87페이지의 제안설계 지층분포 특성 표에 있는 NGB 시추공들의 지층과 N값을 요약해줘",
    "document": "#3편 증빙자료_토질 및 기초.pdf"
}

print("Sending request to /api/chat with #3편 증빙자료 (342MB)...")
start_t = time.time()

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        res_data = json.loads(resp.read().decode("utf-8"))
        elapsed = time.time() - start_t
        print(f"\nResponse received in {elapsed:.1f}s!")
        print("Source Document:", res_data.get("source_document"))
        print("Source Page:", res_data.get("source_page"))
        reply = res_data.get("reply", "")
        print("\n=== Reply Preview ===")
        print(reply[:600] if reply else "Empty reply")
        
        with open("scratch/long_context_test_result.txt", "w", encoding="utf-8") as f:
            f.write(reply)
            
except Exception as e:
    print("Request failed:", e)
