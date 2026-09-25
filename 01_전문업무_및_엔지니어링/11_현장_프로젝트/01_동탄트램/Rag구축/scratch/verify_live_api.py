import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Documents API
res = urllib.request.urlopen('http://127.0.0.1:8080/api/documents')
docs = json.loads(res.read().decode('utf-8'))
for d in docs:
    if '입찰안내서' in d['name']:
        s_count = len(d.get('sections', []))
        print(f"Document: {d['name']}, pages: {d.get('total_pages')}, sections count: {s_count}")

# 2. Master Graph API
res = urllib.request.urlopen('http://127.0.0.1:8080/api/graph/master')
graph = json.loads(res.read().decode('utf-8'))
print(f"Master Graph: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges")
bidding_nodes = [n for n in graph['nodes'] if any(k in n['label'] for k in ['입찰', '설계지침', '계약특수조건', '인터페이스', '비탈면', '노반'])]
print(f"Found {len(bidding_nodes)} relevant engineering/bidding nodes in live master graph:")
for n in bidding_nodes:
    print(f" - {n['id']} | {n['label']} (group: {n.get('group')})")
