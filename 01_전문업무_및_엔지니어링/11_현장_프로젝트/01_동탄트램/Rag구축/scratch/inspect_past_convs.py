import json, os

out_path = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\Rag구축\scratch\past_conv_summary.txt"

with open(out_path, "w", encoding="utf-8") as out:
    for cid in ["d4525787-9473-456b-9cbb-77bda59b7b52", "8949b40e-92be-4e90-afec-12ca34105b8e"]:
        out.write(f"\n========================================\n=== Conv: {cid} ===\n========================================\n")
        p = rf"C:\Users\sskjh\.gemini\antigravity-ide\brain\{cid}\.system_generated\logs\transcript.jsonl"
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                if d.get("type") == "USER_INPUT":
                    c = d.get("content", "")
                    if "<USER_REQUEST>" in c:
                        req = c.split("<USER_REQUEST>")[1].split("</USER_REQUEST>")[0].strip()
                        out.write(f"\n[USER]: {req}\n")
                elif d.get("type") == "PLANNER_RESPONSE" and d.get("status") == "DONE":
                    c = d.get("content", "")
                    lines = [l.strip() for l in c.split("\n") if l.strip()]
                    summary = " ".join(lines[:2])[:200]
                    if summary:
                        out.write(f"[ASSISTANT]: {summary}\n")

print("Finished!")
