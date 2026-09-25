import urllib.request
import json

def test_query(name, query):
    url = f"http://localhost:8080/api/graph/master?{query}"
    req = urllib.request.urlopen(url)
    res = json.loads(req.read().decode("utf-8"))
    bh_nodes = [n for n in res["nodes"] if n["type"] == "BORING"]
    print(f"[{name}] Total Nodes: {len(res['nodes'])}, Boreholes: {len(bh_nodes)}, Edges: {len(res['edges'])}, Discrepancies: {len(res['discrepancies'])}")

test_query("Section 1 (NH+GB)", "section=1")
test_query("Section 2 (DT)", "section=2")
test_query("Depot Only (GB)", "section=depot")
test_query("Risk Only (<3m, N<6)", "risk_only=true")
