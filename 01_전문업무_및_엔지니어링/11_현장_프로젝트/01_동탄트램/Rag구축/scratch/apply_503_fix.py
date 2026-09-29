import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

# 1. Update get_smart_pdf_payload threshold:
# Change 18MB to 3MB
old_threshold_1 = """    # 18MB 초과 시 페이지를 강제로 5장으로 줄이지 않고, Google File API 롱컨텍스트 모드로 직결 전환!
    if len(sliced_bytes) > 18 * 1024 * 1024:
        info_str = f"[Google File API 롱컨텍스트] {', '.join(matched_sections[:6])} 전체({len(sorted_pages)}p, 18MB 초과)를 자르지 않고 Google 멀티모달 통업로드로 분석합니다."
        return None, info_str, False"""

new_threshold_1 = """    # 3MB 초과 시 REST API 인라인 전송 시 503(High Demand/용량초과) 에러가 발생하므로 Google File API 모드로 직결 전환!
    if len(sliced_bytes) > 3 * 1024 * 1024:
        info_str = f"[Google File API 롱컨텍스트] {', '.join(matched_sections[:6])} 등 총 {len(sorted_pages)}p({round(len(sliced_bytes)/(1024*1024), 1)}MB) 전수 탐색 모드"
        return None, info_str, False"""

if old_threshold_1 in content:
    content = content.replace(old_threshold_1, new_threshold_1, 1)
    print("1. Successfully updated 18MB threshold to 3MB!")
else:
    print("1. Warning: old_threshold_1 not found!")

# 2. Update file_size_mb > 20.0 to 5.0
old_threshold_2 = """    if file_size_mb > 20.0 and not (doc_meta and doc_meta.get("sections")):
        # 20MB 초과 대형 스캔 문서는 15쪽으로 자르지 않고 Google File API 통업로드로 처리
        return None, f"[Google File API 롱컨텍스트] {file_path.name} 전체({round(file_size_mb, 1)}MB) 전수 탐색 모드", False"""

new_threshold_2 = """    if file_size_mb > 5.0 and not (doc_meta and doc_meta.get("sections")):
        # 5MB 초과 대형 스캔 문서는 15쪽으로 자르지 않고 Google File API 통업로드로 처리
        return None, f"[Google File API 롱컨텍스트] {file_path.name} 전체({round(file_size_mb, 1)}MB) 전수 탐색 모드", False"""

if old_threshold_2 in content:
    content = content.replace(old_threshold_2, new_threshold_2, 1)
    print("2. Successfully updated 20MB file threshold to 5MB!")
else:
    print("2. Warning: old_threshold_2 not found!")

# 3. Update models_to_try in multi-doc fusion
old_fusion_models = """                    models_to_try = [
                        "gemini-3.6-flash",
                        "gemini-flash-latest",
                        "gemini-3.5-flash-lite"
                    ]"""

new_fusion_models = """                    models_to_try = [
                        "gemini-3.6-flash",
                        "gemini-3.5-flash-lite",
                        "gemini-3.8-flash",
                        "gemini-flash-latest"
                    ]"""

if old_fusion_models in content:
    content = content.replace(old_fusion_models, new_fusion_models, 1)
    print("3. Successfully updated multi-doc fusion models_to_try!")
else:
    print("3. Warning: old_fusion_models not found!")

# 4. Update models_to_try and add File API Auto-Fallback in single-doc chat
old_single_models = """                models_to_try = [
                    "gemini-3.6-flash",
                    "gemini-3.5-flash-lite",
                    "gemini-flash-latest"
                ]"""

new_single_models = """                models_to_try = [
                    "gemini-3.6-flash",
                    "gemini-3.5-flash-lite",
                    "gemini-3.8-flash",
                    "gemini-flash-latest"
                ]"""

if old_single_models in content:
    content = content.replace(old_single_models, new_single_models, 1)
    print("4. Successfully updated single-doc chat models_to_try!")
else:
    print("4. Warning: old_single_models not found!")

# 5. Add Auto-Fallback to Google File API when text is empty after inline REST API calls
old_text_check = """                if text:
                    matched_section_objs = ["""

new_text_check = """                if not text:
                    # [Resilience Guard] 인라인 base64 전송 실패(503/용량초과 등) 시 즉시 100만 컨텍스트 Google File API로 자동 폴백
                    print(f" -> [Inline Base64 Fallback Triggered] Error was: {last_error}")
                    try:
                        from google import genai
                        import gemini_file_manager
                        client = genai.Client(api_key=api_key)
                        file_ref = gemini_file_manager.get_or_upload_file(client, target_file_path)
                        for fb_m in ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-flash-latest"]:
                            try:
                                resp = client.models.generate_content(
                                    model=fb_m,
                                    contents=[file_ref, query],
                                    config=genai.types.GenerateContentConfig(
                                        system_instruction=system_prompt,
                                        temperature=0.1
                                    )
                                )
                                if resp and resp.text:
                                    text = resp.text.strip()
                                    source_notice = (
                                        f"> 🚀 **[Google File API 무중단 전환]** API 일시 부하(503)를 자동 극복하고 Google File API 100만 컨텍스트 모드로 답변을 안전하게 합성했습니다.\\n\\n"
                                    )
                                    break
                            except Exception as fb_err:
                                last_error = f"[{fb_m}] {str(fb_err)}"
                    except Exception as fb_outer:
                        last_error = f"[File API Fallback Failed] {str(fb_outer)}"

                if text:
                    matched_section_objs = ["""

if old_text_check in content:
    content = content.replace(old_text_check, new_text_check, 1)
    print("5. Successfully added Google File API Auto-Fallback resilience guard!")
else:
    print("5. Warning: old_text_check not found!")

# Backup and save
backup_path = server_path.with_suffix(".py.bak_503_fix")
backup_path.write_text(server_path.read_text(encoding="utf-8"), encoding="utf-8")
server_path.write_text(content, encoding="utf-8")
print(f"server.py successfully updated and saved (backup at {backup_path.name})!")
