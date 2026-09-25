import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

rag_dir = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
sys.path.insert(0, str(rag_dir))

import graph_engine

data = graph_engine.build_master_graph()
print(f"Total nodes in master graph: {len(data['nodes'])}")
print(f"Total edges in master graph: {len(data['edges'])}")
print("Sample nodes:")
for n in data['nodes'][:30]:
    print(f"  {n['id']} | {n['label']} | group: {n.get('group')}")
