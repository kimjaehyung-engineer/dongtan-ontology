import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

# 1. Add import usage_cost_tracker at the top
if "import usage_cost_tracker" not in content:
    content = content.replace("import socket\n", "import socket\nimport usage_cost_tracker\n", 1)
    print("1. Added import usage_cost_tracker!")
else:
    print("1. import usage_cost_tracker already exists.")

# 2. Add /api/usage endpoint to do_GET
get_usage_block = """        elif self.path == "/api/usage" or self.path.startswith("/api/usage"):
            try:
                tracker = usage_cost_tracker.get_tracker()
                self.respond_json(tracker.get_summary())
            except Exception as e:
                self.respond_json({"error": str(e)}, 500)
"""
if "/api/usage" not in content:
    content = content.replace(
        'elif self.path.startswith("/api/documents"):',
        get_usage_block + '\n        elif self.path.startswith("/api/documents"):',
        1
    )
    print("2. Added /api/usage endpoint to do_GET!")
else:
    print("2. /api/usage endpoint already exists.")

# 3. In do_POST /api/chat: Add usage tracking to SQL Route
old_sql_block = """                    if sql_res and sql_res.get("reply"):
                        print(f" -> [SQL Route Success] Returning {len(sql_res['reply'])} chars")"""

new_sql_block = """                    if sql_res and sql_res.get("reply"):
                        print(f" -> [SQL Route Success] Returning {len(sql_res['reply'])} chars")
                        try:
                            tracker = usage_cost_tracker.get_tracker()
                            sql_res["usage"] = tracker.record_usage(
                                prompt_tokens=0, candidate_tokens=0, cached_tokens=0,
                                model="Text-to-SQL (Local DB)", status="FREE_LOCAL_SQL"
                            )
                        except Exception as ue:
                            print(f"[Usage Track Error]: {ue}")"""

if old_sql_block in content and 'sql_res["usage"]' not in content:
    content = content.replace(old_sql_block, new_sql_block, 1)
    print("3. Added usage tracking to Text-to-SQL route!")
else:
    print("3. Text-to-SQL usage tracking already exists or pattern not found.")

# 4. Multi-doc fusion usage tracking
old_fusion_resp = """                        resp_data = {
                            "reply": source_notice + text,
                            "source_document": f"다중 공종 복합 제안 ({', '.join(doc_short_names)})",
                            "source_page": 1,
                            "matched_sections": all_matched_titles[:6],
                            "active_sections": all_active_sections[:10],
                            "trace": rag_trace
                        }
                        self.respond_json(resp_data)"""

new_fusion_resp = """                        meta = resp_data.get("usageMetadata", {}) if "resp_data" in locals() and isinstance(resp_data, dict) else {}
                        pt = meta.get("promptTokenCount", 0)
                        ct = meta.get("candidatesTokenCount", 0)
                        try:
                            tracker = usage_cost_tracker.get_tracker()
                            u_info = tracker.record_usage(prompt_tokens=pt, candidate_tokens=ct, cached_tokens=0, model=model_name, status="OK")
                        except Exception:
                            u_info = None

                        resp_data = {
                            "reply": source_notice + text,
                            "source_document": f"다중 공종 복합 제안 ({', '.join(doc_short_names)})",
                            "source_page": 1,
                            "matched_sections": all_matched_titles[:6],
                            "active_sections": all_active_sections[:10],
                            "trace": rag_trace,
                            "usage": u_info
                        }
                        self.respond_json(resp_data)"""

if old_fusion_resp in content:
    content = content.replace(old_fusion_resp, new_fusion_resp, 1)
    print("4. Added usage tracking to Multi-Doc Fusion route!")
else:
    print("4. Multi-Doc Fusion usage tracking pattern not found.")

# 5. Single-Doc File API usage tracking
old_file_api_resp = """                        self.respond_json({
                            "reply": text,
                            "source_document": target_doc_name,
                            "source_page": target_start_page or 1,
                            "matched_sections": matched_section_titles,
                            "trace": rag_trace
                        })"""

new_file_api_resp = """                        try:
                            meta = getattr(resp, "usage_metadata", None) if "resp" in locals() else None
                            pt = getattr(meta, "prompt_token_count", 0) if meta else 0
                            ct = getattr(meta, "candidates_token_count", 0) if meta else 0
                            cached = getattr(meta, "cached_content_token_count", 0) if meta else 0
                            tracker = usage_cost_tracker.get_tracker()
                            u_info = tracker.record_usage(prompt_tokens=pt, candidate_tokens=ct, cached_tokens=cached, model=m_name, status="OK")
                        except Exception as ue:
                            print(f"[Usage Track Error]: {ue}")
                            u_info = None

                        self.respond_json({
                            "reply": text,
                            "source_document": target_doc_name,
                            "source_page": target_start_page or 1,
                            "matched_sections": matched_section_titles,
                            "trace": rag_trace,
                            "usage": u_info
                        })"""

if old_file_api_resp in content:
    content = content.replace(old_file_api_resp, new_file_api_resp, 1)
    print("5. Added usage tracking to Single-Doc File API route!")
else:
    print("5. Single-Doc File API usage tracking pattern not found.")

# 6. Single-Doc Inline / Fallback usage tracking
old_inline_resp = """                    resp_data = {
                        "reply": source_notice + text,
                        "source_document": target_doc_name,
                        "source_page": target_start_page,
                        "matched_sections": matched_section_titles,
                        "active_sections": matched_section_objs
                    }
                    self.respond_json(resp_data)"""

new_inline_resp = """                    try:
                        tracker = usage_cost_tracker.get_tracker()
                        if "resp" in locals() and hasattr(resp, "usage_metadata"):
                            meta = resp.usage_metadata
                            pt = getattr(meta, "prompt_token_count", 0)
                            ct = getattr(meta, "candidates_token_count", 0)
                            cached = getattr(meta, "cached_content_token_count", 0)
                            u_m_name = fb_m if "fb_m" in locals() else "gemini"
                        elif "resp_data" in locals() and isinstance(resp_data, dict):
                            meta = resp_data.get("usageMetadata", {})
                            pt = meta.get("promptTokenCount", 0)
                            ct = meta.get("candidatesTokenCount", 0)
                            cached = 0
                            u_m_name = model_name if "model_name" in locals() else "gemini"
                        else:
                            pt, ct, cached, u_m_name = 0, 0, 0, "gemini"
                        u_info = tracker.record_usage(prompt_tokens=pt, candidate_tokens=ct, cached_tokens=cached, model=u_m_name, status="OK")
                    except Exception as ue:
                        print(f"[Usage Track Error]: {ue}")
                        u_info = None

                    resp_data = {
                        "reply": source_notice + text,
                        "source_document": target_doc_name,
                        "source_page": target_start_page,
                        "matched_sections": matched_section_titles,
                        "active_sections": matched_section_objs,
                        "usage": u_info
                    }
                    self.respond_json(resp_data)"""

if old_inline_resp in content:
    content = content.replace(old_inline_resp, new_inline_resp, 1)
    print("6. Added usage tracking to Single-Doc Inline/Fallback route!")
else:
    print("6. Single-Doc Inline usage tracking pattern not found.")

# 7. Record 429 quota error if error occurs
old_err_block = """            except urllib.error.HTTPError as e:
                err_msg = e.read().decode("utf-8", errors="ignore")
                self.respond_json({"error": f"Google Gemini API 에러 ({e.code}): {err_msg}"}, 500)"""

new_err_block = """            except urllib.error.HTTPError as e:
                err_msg = e.read().decode("utf-8", errors="ignore")
                try:
                    if e.code == 429:
                        usage_cost_tracker.get_tracker().mark_quota_exceeded("gemini", err_msg)
                except Exception:
                    pass
                self.respond_json({"error": f"Google Gemini API 에러 ({e.code}): {err_msg}"}, 500)"""

if old_err_block in content:
    content = content.replace(old_err_block, new_err_block, 1)
    print("7. Added 429 quota marking to HTTPError handler!")
else:
    print("7. HTTPError pattern not found.")

server_path.write_text(content, encoding="utf-8")
print("Backend server.py usage tracking integration finished!")
