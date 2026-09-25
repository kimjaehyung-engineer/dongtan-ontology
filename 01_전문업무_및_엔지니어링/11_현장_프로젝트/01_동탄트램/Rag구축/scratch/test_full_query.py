import sys
import os
import json
import time

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
import server
from pathlib import Path

DOCS_DIR = server.DOCS_DIR
query = "입찰안내서상 지반조사 관련사항"
api_key = server.load_env_api_key()

print("1. Start testing query:", query)
t0 = time.time()

# Simulate routing in /api/chat
query_lower = query.lower()
import re
query_tokens = [w for w in re.split(r'[\s,._/?!~()\[\]]+', query_lower) if len(w) >= 1]
target_nums = server.extract_target_numbers(query_lower)

with open(server.META_INDEX_FILE, "r", encoding="utf-8") as f:
    meta_map = json.load(f)

is_base = any(k in query_lower for k in ["차량기지", "건축기지", "기지", "gb"])
scored_sections = []

for dn, dm in meta_map.items():
    fp = DOCS_DIR / dn
    if not fp.exists(): continue
    doc_bonus = 0
    if any(k in query_lower for k in ["보링", "시추", "주상도", "n치", "n<", "n<=", "n=", "연약", "spt", "관입"]):
        if "주상도" in dn: doc_bonus += 40
    if "입찰안내서" in query_lower and "입찰안내서" in dn: doc_bonus += 60
    if ("기술제안" in query_lower or "4편" in query_lower) and "4편" in dn: doc_bonus += 30
    if "본선" in query_lower and "본선" in dn: doc_bonus += 15
    if ("차량기지" in query_lower or "기지" in query_lower) and "차량기지" in dn: doc_bonus += 15
    if ("3편" in query_lower or "증빙" in query_lower or "기준" in query_lower) and "3편" in dn: doc_bonus += 10
    if (is_base or "1공구" in query_lower or "nh" in query_lower) and "1공구" in dn: doc_bonus += 15
    if ("2공구" in query_lower or "dt" in query_lower) and "2공구" in dn: doc_bonus += 10

    for s in dm.get("sections", []):
        sc = doc_bonus
        sec_title = s.get("title", "")
        for fac in s.get("facility", []):
            if fac.lower() in query_lower: sc += 8
        for kw in s.get("keywords", []):
            if kw.lower() in query_lower: sc += 6
        if sec_title.lower() in query_lower: sc += 10
        if s.get("task_id", "").lower() in query_lower: sc += 8
        if sc > 0:
            scored_sections.append((sc, dn, fp, s))

scored_sections.sort(key=lambda x: x[0], reverse=True)
top_sc, target_doc_name, target_file_path, top_sec = scored_sections[0]
print(f"2. Routed to: {target_doc_name} (Score: {top_sc})")

pdf_bytes, info_msg, is_meta_only = server.get_smart_pdf_payload(target_file_path, query)
print(f"3. Payload generated! pdf_bytes is None: {pdf_bytes is None}, info_msg: {info_msg[:80]}")

if pdf_bytes is None:
    from google import genai
    import gemini_file_manager
    client = genai.Client(api_key=api_key)
    file_ref = gemini_file_manager.get_or_upload_file(client, target_file_path)
    print("4. File ref active:", file_ref.name)
    
    resp = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=[file_ref, query]
    )
    print("5. Response generated in:", round(time.time() - t0, 2), "seconds!")
    print(resp.text[:300])
else:
    print(f"Normal REST path! pdf_bytes size: {round(len(pdf_bytes)/(1024*1024), 2)}MB")
    import base64
    pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    model_name = "gemini-3.8-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    req_body = {
        "contents": [{
            "parts": [
                {"inline_data": {"mime_type": "application/pdf", "data": pdf_b64}},
                {"text": query}
            ]
        }]
    }
    import urllib.request
    req = urllib.request.Request(url, data=json.dumps(req_body).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        ans = res["candidates"][0]["content"]["parts"][0]["text"]
        print("5. Response generated in:", round(time.time() - t0, 2), "seconds!")
        print(ans[:300])
