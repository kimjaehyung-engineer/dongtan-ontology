import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect(r'C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\geotech_data.db')
c = conn.cursor()

generic_ids = [
    'struct_roadbed',
    'risk_settlement_or_interface',
    'mitigation_smart_construction',
    'spec_kds_47_10_05',
    'fac_dongtan_line1',
    'fac_depot'
]

placeholders = ', '.join(['?'] * len(generic_ids))

# 1. Delete edges
c.execute(f"DELETE FROM knowledge_edges WHERE src_id IN ({placeholders}) OR tgt_id IN ({placeholders})", (*generic_ids, *generic_ids))
deleted_edges = c.rowcount

# 2. Delete nodes
c.execute(f"DELETE FROM knowledge_nodes WHERE id IN ({placeholders})", generic_ids)
deleted_nodes = c.rowcount

conn.commit()

c.execute("SELECT COUNT(*) FROM knowledge_nodes")
rem_nodes = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM knowledge_edges")
rem_edges = c.fetchone()[0]

print(f"Deleted {deleted_nodes} generic nodes and {deleted_edges} connected edges.")
print(f"Remaining in DB: {rem_nodes} nodes, {rem_edges} edges.")

conn.close()
