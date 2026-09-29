import re

server_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"

with open(server_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update is_meta_only block to include usage
old_meta_only = """                if is_meta_only:
                    self.respond_json({
                        "reply": info_msg,
                        "source_document": target_doc_name,
                        "source_page": target_start_page,
                        "matched_sections": matched_section_titles
                    })
                    return"""

new_meta_only = """                if is_meta_only:
                    try:
                        u_info = usage_cost_tracker.get_tracker().record_usage(
                            prompt_tokens=0,
                            candidate_tokens=0,
                            cached_tokens=0,
                            model="local-metadata",
                            status="LOCAL_CACHE"
                        )
                    except Exception:
                        u_info = None
                    self.respond_json({
                        "reply": info_msg,
                        "source_document": target_doc_name,
                        "source_page": target_start_page,
                        "matched_sections": matched_section_titles,
                        "usage": u_info
                    })
                    return"""

if old_meta_only in content:
    content = content.replace(old_meta_only, new_meta_only)
    print("1. Patched is_meta_only block with usage!")
else:
    print("1. Old meta_only pattern not found exactly, skipping or already patched.")

# 2. Update File API usage tracking in first block
old_track_block = """                        try:
                            meta = getattr(resp, "usage_metadata", None) if "resp" in locals() else None
                            pt = getattr(meta, "prompt_token_count", 0) if meta else 0
                            ct = getattr(meta, "candidates_token_count", 0) if meta else 0
                            cached = getattr(meta, "cached_content_token_count", 0) if meta else 0
                            tracker = usage_cost_tracker.get_tracker()
                            u_info = tracker.record_usage(prompt_tokens=pt, candidate_tokens=ct, cached_tokens=cached, model=m_name, status="OK")
                        except Exception as ue:
                            print(f"[Usage Track Error]: {ue}")
                            u_info = None"""

new_track_block = """                        try:
                            meta = getattr(resp, "usage_metadata", None) if "resp" in locals() else None
                            pt = int(getattr(meta, "prompt_token_count", 0) or 0) if meta else 0
                            ct = int(getattr(meta, "candidates_token_count", 0) or 0) if meta else 0
                            cached = int(getattr(meta, "cached_content_token_count", 0) or 0) if meta else 0
                            tracker = usage_cost_tracker.get_tracker()
                            u_info = tracker.record_usage(prompt_tokens=pt, candidate_tokens=ct, cached_tokens=cached, model=m_name, status="OK")
                        except Exception as ue:
                            print(f"[Usage Track Error]: {ue}", flush=True)
                            u_info = None"""

if old_track_block in content:
    content = content.replace(old_track_block, new_track_block)
    print("2. Robustified File API usage tracking block 1!")

# 3. Add usage tracking to line 4700 block (second File API return)
old_second_ret = """                        self.respond_json({
                            "reply": text,
                            "source_document": target_doc_name,
                            "source_page": target_start_page or 1,
                            "matched_sections": matched_section_titles,
                            "trace": rag_trace
                        })
                        return"""

new_second_ret = """                        try:
                            meta = getattr(resp, "usage_metadata", None) if "resp" in locals() else None
                            pt = int(getattr(meta, "prompt_token_count", 0) or 0) if meta else 0
                            ct = int(getattr(meta, "candidates_token_count", 0) or 0) if meta else 0
                            cached = int(getattr(meta, "cached_content_token_count", 0) or 0) if meta else 0
                            tracker = usage_cost_tracker.get_tracker()
                            u_info = tracker.record_usage(prompt_tokens=pt, candidate_tokens=ct, cached_tokens=cached, model=m_name if "m_name" in locals() else "gemini", status="OK")
                        except Exception as ue:
                            print(f"[Usage Track Error 2]: {ue}", flush=True)
                            u_info = None
                        self.respond_json({
                            "reply": text,
                            "source_document": target_doc_name,
                            "source_page": target_start_page or 1,
                            "matched_sections": matched_section_titles,
                            "trace": rag_trace,
                            "usage": u_info
                        })
                        return"""

if old_second_ret in content:
    content = content.replace(old_second_ret, new_second_ret)
    print("3. Patched second File API return with usage tracking!")

with open(server_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Finished patching server.py!")
