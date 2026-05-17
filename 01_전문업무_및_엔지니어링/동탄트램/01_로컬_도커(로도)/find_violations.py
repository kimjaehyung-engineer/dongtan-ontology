import json
from neo4j import GraphDatabase

URI = 'bolt://localhost:7687'
driver = GraphDatabase.driver(URI, auth=('', ''))

results = []
with driver.session() as session:
    q = '''
    MATCH (n)
    WHERE n.name CONTAINS '위배' OR n.name CONTAINS '미달' OR n.name CONTAINS '부족' OR n.name CONTAINS '초과' OR n.name CONTAINS '불가' OR n.name CONTAINS '불일치' OR n.name CONTAINS '상충' OR n.name CONTAINS '미확보' OR n.name CONTAINS '충돌'
    RETURN n.name as name
    '''
    res = session.run(q)
    for r in res:
        results.append(r['name'])

    q2 = '''
    MATCH (a)-[r]-(b)
    WHERE (a.name CONTAINS '정거장' OR b.name CONTAINS '정거장') AND (b.name CONTAINS '위배' OR b.name CONTAINS '미달' OR b.name CONTAINS '미확보' OR b.name CONTAINS '불일치' OR b.name CONTAINS '충돌')
    RETURN a.name as src, type(r) as rel, b.name as dst
    '''
    res2 = session.run(q2)
    rels = []
    for r in res2:
        rels.append(f"{r['src']} - [{r['rel']}] -> {r['dst']}")

with open('violations.json', 'w', encoding='utf-8') as f:
    json.dump({'nodes': results, 'rels': rels}, f, ensure_ascii=False, indent=2)
driver.close()
