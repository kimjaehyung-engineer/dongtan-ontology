import os, sys, json

sys.stdout.reconfigure(encoding='utf-8')

json_act_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\parsed_activities.json'
json_split_path = r'c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\scratch\section_splits.json'

with open(json_act_path, 'r', encoding='utf-8') as f:
    activities_data = json.load(f)

with open(json_split_path, 'r', encoding='utf-8') as f:
    splits_data = json.load(f)

print(f"Activities count: {len(activities_data)}")
print(f"Splits count: {len(splits_data)}")

# Sample inspection
print("First 3 splits sample:")
for sp in splits_data[:3]:
    print(sp, type(sp.get('startM')), type(sp.get('endM')))
