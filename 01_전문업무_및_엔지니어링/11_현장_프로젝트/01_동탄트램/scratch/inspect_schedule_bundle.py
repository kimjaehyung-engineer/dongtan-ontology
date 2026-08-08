import os, sys
sys.stdout.reconfigure(encoding='utf-8')

rule_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\.agents\rules\schedule.md'
if os.path.exists(rule_path):
    with open(rule_path, 'r', encoding='utf-8') as f:
        print("=== .agents/rules/schedule.md ===")
        print(f.read())

js_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\time-chainage-mvp\dist\assets\index-no5s-_SR.js'
if os.path.exists(js_path):
    with open(js_path, 'r', encoding='utf-8') as f:
        js_text = f.read(5000)
        print("\n=== index-no5s-_SR.js header ===")
        print(js_text[:500])
