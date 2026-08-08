import os, re, json

app_jsx_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\09.공정표\src\App.jsx'

with open(app_jsx_path, 'r', encoding='utf-8') as f:
    text = f.read()

print(f"App.jsx size: {len(text)} chars")

# Extract INITIAL_ACTIVITIES data or station data
pos_act = text.find('INITIAL_ACTIVITIES')
if pos_act != -1:
    print("\n=== Found INITIAL_ACTIVITIES snippet ===")
    print(text[pos_act:pos_act+1500])

pos_stn = text.find('STATIONS')
if pos_stn != -1:
    print("\n=== Found STATIONS snippet ===")
    print(text[pos_stn:pos_stn+1000])
