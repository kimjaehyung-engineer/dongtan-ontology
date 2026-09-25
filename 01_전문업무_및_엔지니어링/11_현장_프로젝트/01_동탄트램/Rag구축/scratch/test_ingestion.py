# -*- coding: utf-8 -*-
import sys
sys.path.append(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
import knowledge_ingestion
from pathlib import Path

rag_dir = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
target_pdf = rag_dir / "documents" / "토질_차량기지 비탈면 안정성 검토-rev01_260630.pdf"

# Load API key
api_key = None
env_file = rag_dir / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                api_key = line.strip().split("=", 1)[1]

print(f"Testing ingestion on: {target_pdf.name}")
print(f"API key loaded: {bool(api_key)}")

res = knowledge_ingestion.ingest_file(target_pdf, api_key=api_key)
print("=== Ingestion Result ===")
import json
print(json.dumps(res, ensure_ascii=False, indent=2))
