import urllib.request
import json
import time

for _ in range(5):
    try:
        req = urllib.request.urlopen("http://localhost:8080/api/config", timeout=5)
        res = json.loads(req.read().decode("utf-8"))
        print("Server is UP! Config:", res)
        break
    except Exception as e:
        print("Waiting for server...", e)
        time.sleep(1)
