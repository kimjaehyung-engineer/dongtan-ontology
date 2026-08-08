import os, sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

target_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(target_html, 'r', encoding='utf-8') as f:
    html = f.read()

m_act = re.search(r'const RAW_ACTIVITIES = (\[[\s\S]*?\]);', html)
m_split = re.search(r'const SECTION_SPLITS = (\[[\s\S]*?\]);', html)

acts = json.loads(m_act.group(1))
splits = json.loads(m_split.group(1))

print(f"Loaded {len(acts)} activities and {len(splits)} splits from target HTML")

split_groups = sorted(list(set(f"{s['zone']}_{s['splitGroup']}" for s in splits)))
print("\n=== Split Groups in HTML ===")
for sg in split_groups[:20]:
    print("  -", sg)

act_groups = sorted(list(set(f"{a['zone']}_{a.get('splitGroup', 'NONE')}" for a in acts)))
print("\n=== Act Groups in HTML ===")
for ag in act_groups[:20]:
    print("  -", ag)
