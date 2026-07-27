import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\sskjh\.gemini\antigravity\brain\887aacfa-3165-4be1-8e89-29f90e47a298\.system_generated\logs"
t_file = os.path.join(log_dir, "transcript_full.jsonl")

steps_to_inspect = [1398, 1404, 1412]

with open(t_file, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            step_idx = data.get("step_index")
            if step_idx in steps_to_inspect:
                print(f"\n==================== STEP {step_idx} ====================")
                tool_calls = data.get("tool_calls", [])
                for tc in tool_calls:
                    name = tc.get("name", "")
                    args = tc.get("args", {})
                    target = args.get("TargetFile", args.get("Target", ""))
                    print(f"Tool Call: {name}, Target: {target}")
                    code = args.get("CodeContent", args.get("ReplacementContent", ""))
                    if code:
                        print("--- CODE ---")
                        print(code[:2000])
                        print("... [TRUNCATED] ...")
        except Exception as e:
            pass
