import urllib.request
import json

endpoints = [
    "/api/config",
    "/api/documents",
    "/api/graph/master"
]

for ep in endpoints:
    try:
        url = f"http://localhost:8080{ep}"
        req = urllib.request.urlopen(url, timeout=5)
        data = req.read().decode("utf-8")
        print(f"[{ep}] Status: {req.status}, Length: {len(data)}")
    except Exception as e:
        print(f"[{ep}] ERROR: {e}")
