import urllib.request
import urllib.error
import json

url = "http://localhost:8080/api/chat"
payload = {
    "query": "문서 87페이지의 4.4.1 지층분포 특성 절에 기술된 내용과 구성상태 설명을 요약해줘",
    "document": "#3편 증빙자료_토질 및 기초.pdf"
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        print("Success:", resp.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Error Body:", e.read().decode("utf-8", errors="replace"))
except Exception as e:
    print("Other Error:", e)
