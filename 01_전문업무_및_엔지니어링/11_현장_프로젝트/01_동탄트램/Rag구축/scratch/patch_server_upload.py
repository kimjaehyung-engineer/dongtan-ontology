# -*- coding: utf-8 -*-
import re

server_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# 1. Update backend do_POST for /api/upload
old_backend = '''                        filename = headers.split(b'filename="')[1].split(b'"')[0].decode('utf-8', errors='ignore')
                        if filename.lower().endswith('.pdf'):
                            save_path = DOCS_DIR / filename
                            with open(save_path, "wb") as out_f:
                                out_f.write(file_data)
                            self.respond_json({"status": "uploaded"})'''

new_backend = '''                        filename = headers.split(b'filename="')[1].split(b'"')[0].decode('utf-8', errors='ignore')
                        if filename.lower().endswith(('.pdf', '.xlsx', '.csv')):
                            save_path = DOCS_DIR / filename
                            with open(save_path, "wb") as out_f:
                                out_f.write(file_data)
                            
                            # 자동 온톨로지 지식망 확장 파이프라인 가동
                            ingest_data = {}
                            try:
                                import knowledge_ingestion
                                ingest_data = knowledge_ingestion.ingest_file(save_path, api_key=load_env_api_key())
                            except Exception as e:
                                print(f"[KnowledgeIngestion] Error: {e}")
                                ingest_data = {"status": "partial", "message": str(e)}

                            self.respond_json({"status": "uploaded", "filename": filename, "ingest": ingest_data})'''

if old_backend in code:
    code = code.replace(old_backend, new_backend)
    print("Backend /api/upload updated!")
else:
    print("Warning: old_backend pattern not found exactly, attempting regex replace...")
    code = re.sub(
        r'filename = headers\.split\(b\'filename="\'\)\[1\]\.split\(b\'"\'\)\[0\]\.decode\(\'utf-8\', errors=\'ignore\'\)\s+if filename\.lower\(\)\.endswith\(\'\.pdf\'\):\s+save_path = DOCS_DIR / filename\s+with open\(save_path, "wb"\) as out_f:\s+out_f\.write\(file_data\)\s+self\.respond_json\(\{"status": "uploaded"\}\)',
        new_backend,
        code
    )

# 2. Update frontend uploadDoc to show the rich notification and refresh graph
old_frontend = '''      if (total > 1) {
        alert(`총 ${total}개 문서 중 ${successCount}개 문서가 서재에 추가되었습니다!`);
      }'''

new_frontend = '''      if (typeof loadMasterGraph === 'function') {
        loadMasterGraph();
      }
      if (lastUploadedData && lastUploadedData.ingest && lastUploadedData.ingest.summary) {
        alert(lastUploadedData.ingest.summary);
      } else if (total > 1) {
        alert(`총 ${total}개 문서 중 ${successCount}개 문서가 서재 및 지식망에 추가되었습니다!`);
      } else if (successCount === 1) {
        alert(`문서가 서재 및 지식망에 성공적으로 반영되었습니다!`);
      }'''

if old_frontend in code:
    code = code.replace(old_frontend, new_frontend)
    print("Frontend uploadDoc alert updated!")

# Also capture lastUploadedData in upload loop
code = code.replace(
    "            if (res.ok) {\n              successCount++;\n              lastUploadedName = file.name;\n            }",
    "            if (res.ok) {\n              successCount++;\n              lastUploadedName = file.name;\n              try { lastUploadedData = await res.json(); } catch(err){}\n            }"
)

# Insert let lastUploadedData = null before loop
code = code.replace(
    "      let successCount = 0;\n      let lastUploadedName = null;",
    "      let successCount = 0;\n      let lastUploadedName = null;\n      let lastUploadedData = null;"
)

with open(server_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Finished updating server.py!")
