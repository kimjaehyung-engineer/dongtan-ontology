import urllib.request
import json
import time

url = "http://localhost:8080/api/chat"
payload = {
    "query": "문서 87페이지의 4.4.1 지층분포 특성 절에 기술된 내용과 구성상태 설명을 요약해줘",
    "document": "#3편 증빙자료_토질 및 기초.pdf"
}

print("Testing pure document query on #3편 증빙자료 (342MB)...")
start_t = time.time()

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req, timeout=180) as resp:
        res_data = json.loads(resp.read().decode("utf-8"))
        elapsed = time.time() - start_t
        print(f"\nResponse received in {elapsed:.1f}s!")
        print("Source Document:", res_data.get("source_document"))
        
        reply = res_data.get("reply", "")
        with open("scratch/long_context_success.txt", "w", encoding="utf-8") as f:
            f.write(reply)
        print("Saved reply to scratch/long_context_success.txt")
except Exception as e:
    print("Request failed:", e)
