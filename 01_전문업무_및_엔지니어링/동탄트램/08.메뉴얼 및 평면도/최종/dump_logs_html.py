import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_dir = r"C:\Users\sskjh\.gemini\antigravity\brain\887aacfa-3165-4be1-8e89-29f90e47a298\.system_generated\logs"
t_file = os.path.join(log_dir, "transcript_full.jsonl")

steps_to_inspect = [1544, 1560, 1562, 1566, 1574, 1578, 1604]

with open(t_file, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            step_idx = data.get("step_index")
            if step_idx in steps_to_inspect:
                print(f"\n==================== STEP {step_idx} ====================")
                # Check for write_to_file calls inside tool_calls
                tool_calls = data.get("tool_calls", [])
                if not tool_calls and "planner_response" in str(data.get("type")):
                    # It might be in the model response
                    pass
                for tc in tool_calls:
                    method = tc.get("ToolName", "")
                    args = tc.get("Arguments", {})
                    target = args.get("TargetFile", args.get("Target", ""))
                    if "레일" in str(target) or "용접장" in str(target) or "3_" in str(target):
                        print(f"Tool Call Method: {method}")
                        print(f"Target File: {target}")
                        code = args.get("CodeContent", args.get("ReplacementContent", ""))
                        if code:
                            print("--- CODE CONTENT ---")
                            print(code[:2000]) # Print first 2000 chars of code
                            print("... [TRUNCATED] ...")
        except Exception as e:
            print(f"Error parsing line: {e}")
