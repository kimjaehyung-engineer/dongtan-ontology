import urllib.request
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = 'http://localhost:8080/api/chat'
payload = {
    'query': '입찰안내서상 계약상 리스크',
    'document': '입찰안내서(동탄트램).pdf'
}

print('Testing query: "입찰안내서상 계약상 리스크"...')
start = time.time()
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        elapsed = time.time() - start
        reply = data.get('reply', '')
        print(f"\n[BENCHMARK RESULT]")
        print(f"Elapsed Time: {elapsed:.2f} seconds")
        print(f"Reply Length: {len(reply)} chars")
        print(f"Route: {data.get('route')}")
        print(f"Source Document: {data.get('source_document')}")
        print(f"Source Page: {data.get('source_page')}")
        print(f"\n--- Output Content ---")
        print(reply)
except Exception as e:
    print(f"Error: {e}")
