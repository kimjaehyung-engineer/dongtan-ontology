import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\sskjh\.gemini\antigravity\brain\887aacfa-3165-4be1-8e89-29f90e47a298\.system_generated\logs"
t_file = os.path.join(log_dir, "transcript_full.jsonl")

print("Dumping raw jsonl match lines...")

match_count = 0
with open(t_file, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if "레일 용접장 선정" in line and "표준서" in line and ("write_to_file" in line or "replace_file_content" in line):
            print(f"\n--- MATCH {match_count} (Line {idx}) ---")
            print(line[:3000]) # Print first 3000 chars of raw json line
            match_count += 1
            if match_count >= 5:
                break
