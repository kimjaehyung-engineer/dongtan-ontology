import os

for fname in ['ingest_geotech.py', 'gemini_file_manager.py']:
    fpath = os.path.join(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG", fname)
    if os.path.exists(fpath):
        print(f"=== {fname} ===")
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for i in range(min(50, len(lines))):
                print(f"{i+1}: {lines[i]}", end="")
        print("\n" + "="*50)
