import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
lines = server_path.read_text(encoding='utf-8').splitlines()

def show_range(start, end):
    for i in range(start - 1, min(end, len(lines))):
        print(f"{i+1:4d}: {lines[i]}")

print("=== BLOCK 1 (3750-3780) ===")
show_range(3750, 3780)

print("\n=== BLOCK 2 (3850-3880) ===")
show_range(3850, 3880)

print("\n=== BLOCK 3 (3915-4025) ===")
show_range(3915, 4025)

print("\n=== BLOCK 4 (4060-4085) ===")
show_range(4060, 4085)

print("\n=== BLOCK 5 (4155-4225) ===")
show_range(4155, 4225)
