import urllib.request

url = 'http://localhost:5173/index.html'

try:
    req = urllib.request.urlopen(url)
    content = req.read().decode('utf-8')
    print("=== HTTP GET http://localhost:5173/index.html ===")
    print(f"Status: {req.status}")
    print(content[:300])
except Exception as e:
    print(f"Error fetching {url}: {e}")

url_js = 'http://localhost:5173/assets/index-no5s-_SR.js'
try:
    req = urllib.request.urlopen(url_js)
    print(f"\n=== HTTP GET {url_js} ===")
    print(f"Status: {req.status}, Content-Length: {len(req.read())}")
except Exception as e:
    print(f"Error fetching {url_js}: {e}")
