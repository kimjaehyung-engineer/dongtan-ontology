import json

with open('all_station_rels.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

markdown = '# 정거장 설계 관련 기준 및 리스크 분석\n\n'

markdown += '## ⚠️ 기술 제약 및 기준 (TECHNICAL_REQ & HUB_LINK)\n'
reqs = set()
for d in data:
    if d['rel'] in ['TECHNICAL_REQ', 'HUB_LINK', 'CONFLICT']:
        reqs.add(f"- {d['source']} ➡️ [{d['rel']}] ➡️ {d['target']}")
markdown += '\n'.join(sorted(reqs)) + '\n\n'

markdown += '## 🚨 리스크 파급 (RISK_IMPACT)\n'
risks = set()
for d in data:
    if d['rel'] == 'RISK_IMPACT':
        risks.add(f"- {d['source']} ➡️ [{d['rel']}] ➡️ {d['target']}")
markdown += '\n'.join(sorted(risks)) + '\n'

with open('station_analysis.md', 'w', encoding='utf-8') as f:
    f.write(markdown)
