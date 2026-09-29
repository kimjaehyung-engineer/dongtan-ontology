import sys, os, urllib.request, json, time, base64, re
from pathlib import Path
from pypdf import PdfReader, PdfWriter

sys.stdout.reconfigure(encoding='utf-8')
rag_dir = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
sys.path.insert(0, str(rag_dir))

query = "동탄역 핵심이슈는 머지?"
META_INDEX_FILE = rag_dir / "meta_index.json"

with open(META_INDEX_FILE, "r", encoding="utf-8") as f:
    meta_index = json.load(f)

# Let's inspect scoring
query_terms = [t.strip().lower() for t in re.split(r'[\s,._\-/]+', query) if len(t.strip()) >= 2]
print("Query terms:", query_terms)

# Read server.py scoring lines
lines = (rag_dir / "server.py").read_text(encoding="utf-8").splitlines()
# Let's see lines 3510 to 3650
for i in range(3510, 3600):
    if "doc_bonus" in lines[i] or "score +=" in lines[i] or "scored_sections" in lines[i]:
        print(f"{i+1}: {lines[i]}")
