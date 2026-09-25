import json

p = r"C:\Users\sskjh\.gemini\antigravity-ide\brain\d4525787-9473-456b-9cbb-77bda59b7b52\.system_generated\logs\transcript.jsonl"
with open(p, "r", encoding="utf-8") as f:
    lines = f.readlines()

out = []
out.append(f"Total lines: {len(lines)}")
for idx, l in enumerate(lines):
    d = json.loads(l)
    t = d.get("type")
    s = d.get("status")
    c = d.get("content", "")
    tc = d.get("tool_calls", [])
    out.append(f"Line {idx}: type={t}, status={s}, tools={len(tc)}")
    if t == "USER_INPUT":
        out.append(f"  Content: {c[:200]}")
    elif t == "PLANNER_RESPONSE":
        out.append(f"  Content: {c[:200]}")
        if tc:
            out.append(f"  Tool calls: {[call.get('name') for call in tc]}")

with open(r"scratch\d4525_summary.txt", "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(out))

print("Dumped summary")
