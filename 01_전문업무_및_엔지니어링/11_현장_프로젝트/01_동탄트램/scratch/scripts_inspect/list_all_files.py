import os

def list_all():
    root = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램"
    with open("scratch/all_workspace_files.txt", "w", encoding="utf-8") as out:
        out.write("All files in workspace:\n")
        for dirpath, _, filenames in os.walk(root):
            if any(p in dirpath for p in [".gemini", ".git", "01_로컬_도커"]):
                continue
            for f in filenames:
                fp = os.path.join(dirpath, f)
                out.write(f"{os.path.relpath(fp, root)} (size: {os.path.getsize(fp)} bytes)\n")

if __name__ == '__main__':
    list_all()
