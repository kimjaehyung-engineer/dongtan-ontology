import os, sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

target_html = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\동탄트램_Time_Chainage_공정표_대시보드.html'

with open(target_html, 'r', encoding='utf-8') as f:
    html = f.read()

print("=== Checking HTML JavaScript Syntax & JSON Embed Integrity ===")

m_act = re.search(r'const RAW_ACTIVITIES = (\[[\s\S]*?\]);', html)
m_split = re.search(r'const SECTION_SPLITS = (\[[\s\S]*?\]);', html)

if not m_act:
    print("❌ RAW_ACTIVITIES match failed!")
else:
    try:
        acts = json.loads(m_act.group(1))
        print(f"✓ RAW_ACTIVITIES JSON successfully parsed: {len(acts)} items")
    except Exception as e:
        print(f"❌ RAW_ACTIVITIES JSON parse error: {e}")

if not m_split:
    print("❌ SECTION_SPLITS match failed!")
else:
    try:
        splits = json.loads(m_split.group(1))
        print(f"✓ SECTION_SPLITS JSON successfully parsed: {len(splits)} items")
    except Exception as e:
        print(f"❌ SECTION_SPLITS JSON parse error: {e}")

# Check script block
scripts = re.findall(r'<script>([\s\S]*?)<\/script>', html)
print(f"Found {len(scripts)} inline script blocks.")

for idx, sc in enumerate(scripts):
    # Save script to temp file and run node syntax check
    temp_js = f"c:/Users/sskjh/antigravity/01_전문업무_및_엔지니어링/11_현장_프로젝트/01_동탄트램/scratch/temp_script_{idx}.js"
    with open(temp_js, 'w', encoding='utf-8') as jf:
        jf.write(sc)
    print(f"Checking Script Block {idx}...")
