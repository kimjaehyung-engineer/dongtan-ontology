import urllib.request
import json
import time

for _ in range(5):
    try:
        req = urllib.request.urlopen("http://localhost:8080/api/graph/master", timeout=5)
        res = json.loads(req.read().decode("utf-8"))
        print("Success! HTTP Status:", req.status)
        print("Nodes count:", len(res.get("nodes", [])))
        print("Edges count:", len(res.get("edges", [])))
        print("Summary:", res.get("summary"))
        print("Discrepancies count:", len(res.get("discrepancies", [])))
        print("Sample node:", res.get("nodes", [])[0])
        break
    except Exception as e:
        print("Waiting for server...", e)
        time.sleep(1)
