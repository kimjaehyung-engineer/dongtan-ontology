import json

p = r"C:\Users\sskjh\.gemini\antigravity-ide\brain\d4525787-9473-456b-9cbb-77bda59b7b52\.system_generated\logs\transcript_full.jsonl"
with open(p, "r", encoding="utf-8") as f:
    for line in f:
        d = json.loads(line)
        si = d.get("step_index")
        if si and si >= 150:
            print(f"Step {si}: type={d.get('type')}, source={d.get('source')}")
            tc = d.get("tool_calls", [])
            if tc:
                for c in tc:
                    print(f"  Tool: {c.get('name')}")
                    args = c.get("args")
                    if isinstance(args, dict):
                        for k, v in args.items():
                            print(f"    {k}: {str(v)[:150]}")
            cnt = d.get("content", "")
            if cnt:
                print(f"  Content: {cnt[:200]}")
