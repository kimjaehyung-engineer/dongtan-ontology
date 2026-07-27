import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\sskjh\.gemini\antigravity\brain\887aacfa-3165-4be1-8e89-29f90e47a298\.system_generated\logs"
t_file = os.path.join(log_dir, "transcript_full.jsonl")

if not os.path.exists(t_file):
    print(f"Log file not found: {t_file}")
    sys.exit(1)

print("Searching log file for '레일 용접장 선정' standard content...")

matches = []
with open(t_file, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if "레일 용접장 선정" in line and "표준서" in line:
            # We want to find steps where the HTML content was generated or modified
            try:
                data = json.loads(line)
                step_idx = data.get("step_index", idx)
                content = str(data.get("content", ""))
                tool_calls = str(data.get("tool_calls", ""))
                
                # Check if it has a file write or edit containing HTML
                if "write_to_file" in tool_calls or "replace_file_content" in tool_calls or "CodeContent" in tool_calls:
                    matches.append((step_idx, data))
                    print(f"Match found at Step {step_idx}")
            except Exception as e:
                pass

print(f"\nFound {len(matches)} potential matches. Displaying details of the latest matches:")
for step_idx, data in matches[-3:]:
    print(f"\n--- MATCH DETAIL FOR STEP {step_idx} ---")
    print(f"Source: {data.get('source')}, Type: {data.get('type')}")
    # Extract code contents or tool calls
    tc = data.get("tool_calls", [])
    for call in tc:
        if "write_to_file" in str(call) or "replace_file_content" in str(call):
            args = call.get("Arguments", {})
            code = args.get("CodeContent", args.get("ReplacementContent", ""))
            if "레일" in code and "용접장" in code:
                print(f"Tool: {call.get('ToolName')}")
                print(f"Code Preview (first 1000 chars):\n{code[:1000]}\n...")
