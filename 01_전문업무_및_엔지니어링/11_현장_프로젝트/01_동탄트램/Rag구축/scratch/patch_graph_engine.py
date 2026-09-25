# -*- coding: utf-8 -*-
import re

target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\graph_engine.py"
with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Check if knowledge_nodes already present
if "knowledge_nodes" in content:
    print("graph_engine.py already has knowledge_nodes integration.")
else:
    # 1. Don't close conn early at line 67
    content = content.replace("    conn.close()\n\n    # ", "    # conn 유지\n\n    # ")

    # 2. Add dynamic knowledge loading right before summary_text
    injection = '''
    # 5) 동적으로 확장된 문서 지식망 노드 및 엣지 결합
    try:
        cur_k = conn.cursor()
        # 테이블 존재 여부 확인
        tbl_check = cur_k.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='knowledge_nodes'").fetchone()
        if tbl_check:
            k_nodes = cur_k.execute("SELECT id, label, type, description, group_name, facility, doc_name, page, properties FROM knowledge_nodes").fetchall()
            for kn in k_nodes:
                k_fac = kn["facility"] or ""
                if section == "1" and "1공구" not in k_fac and "공통" not in k_fac:
                    continue
                if section == "2" and "2공구" not in k_fac and "공통" not in k_fac:
                    continue
                if section in ("depot", "prop") and "차량기지" not in k_fac and "공통" not in k_fac:
                    continue

                extra_props = {}
                if kn["properties"]:
                    try: extra_props = json.loads(kn["properties"])
                    except Exception: pass
                extra_props["doc_name"] = kn["doc_name"]
                extra_props["page"] = kn["page"]
                extra_props["facility"] = kn["facility"]

                add_node(
                    kn["id"],
                    kn["label"],
                    kn["type"],
                    desc=kn["description"] or "",
                    group=kn["group_name"] or kn["type"].lower(),
                    extra=extra_props
                )

            k_edges = cur_k.execute("SELECT src_id, tgt_id, relation, label, is_warning, doc_name, page FROM knowledge_edges").fetchall()
            for ke in k_edges:
                # 연결될 노드가 존재하는지 확인 후 엣지 추가
                if ke["src_id"] in node_set and ke["tgt_id"] in node_set:
                    add_edge(
                        ke["src_id"],
                        ke["tgt_id"],
                        ke["relation"],
                        label=ke["label"] or "",
                        is_warning=bool(ke["is_warning"])
                    )
    except Exception as e:
        print(f"[graph_engine] 동적 지식 노드 로딩 실패: {e}")
    finally:
        try: conn.close()
        except Exception: pass

    summary_text = (
'''
    content = content.replace("    summary_text = (\n", injection)

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully patched graph_engine.py!")
