import re
from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

# 1. Add self-healing guard right after import sys
old_sys_block = """import sys
sys.path.insert(0, str(Path(__file__).parent))"""

new_sys_block = """import sys
# [Self-Healing Guard] Google GenAI 및 PyMuPDF가 설치된 Python 3.14 인터프리터 자동 감지 및 인계
py314_exe = r"C:\\Users\\sskjh\\AppData\\Local\\Programs\\Python\\Python314\\python.exe"
if os.path.exists(py314_exe) and sys.executable.lower() != py314_exe.lower():
    try:
        from google import genai
    except ImportError:
        import subprocess
        print(f"[Self-Healing] Detected missing 'google.genai' in current interpreter ({sys.executable}).")
        print(f"[Self-Healing] Seamlessly switching to Python 3.14: {py314_exe}...")
        sys.exit(subprocess.call([py314_exe] + sys.argv))

sys.path.insert(0, str(Path(__file__).parent))"""

if old_sys_block in content:
    content = content.replace(old_sys_block, new_sys_block, 1)
    print("1. Added self-healing Python 3.14 guard!")
else:
    print("1. Warning: old_sys_block not found!")

# 2. Add '입찰안내서' and '기술제안' routing bonus
old_bonus_block = """                        if any(k in query_lower for k in ["보링", "시추", "주상도", "n치", "n<", "n<=", "n=", "연약", "spt", "관입"]):
                            if "주상도" in dn: doc_bonus += 40
                        if "본선" in query_lower and "본선" in dn: doc_bonus += 15"""

new_bonus_block = """                        if any(k in query_lower for k in ["보링", "시추", "주상도", "n치", "n<", "n<=", "n=", "연약", "spt", "관입"]):
                            if "주상도" in dn: doc_bonus += 40
                        if "입찰안내서" in query_lower and "입찰안내서" in dn: doc_bonus += 60
                        if ("기술제안" in query_lower or "4편" in query_lower) and "4편" in dn: doc_bonus += 30
                        if "본선" in query_lower and "본선" in dn: doc_bonus += 15"""

if old_bonus_block in content:
    content = content.replace(old_bonus_block, new_bonus_block, 1)
    print("2. Added 입찰안내서/기술제안 routing bonus!")
else:
    print("2. Warning: old_bonus_block not found!")

# 3. Update models_to_try in /api/chat
old_chat_models = """                        models_to_try = ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-flash-latest"]"""
new_chat_models = """                        models_to_try = [
                            "gemini-3.8-flash",
                            "gemini-3.6-flash",
                            "gemini-3.5-flash-lite",
                            "gemini-flash-latest"
                        ]"""

if old_chat_models in content:
    content = content.replace(old_chat_models, new_chat_models, 1)
    print("3. Updated /api/chat models_to_try with gemini-3.8-flash!")
else:
    print("3. Warning: old_chat_models not found!")

# 4. Fix target_file_path bug and update models in /api/extract-graph
old_extract_graph = """                        file_ref = gemini_file_manager.get_or_upload_file(client, target_file_path)
                        
                        system_prompt = (
                            "당신은 철도/토목/지반 엔지니어링 및 설계보고서, 시추주상도 분석 전문 AI입니다.\\n"
                            "제공된 대용량 PDF 문서 전체(수백 페이지)를 면밀히 분석하여 질문에 100% 팩트 기반으로 답변하세요.\\n\\n"
                            "[핵심 규칙]\\n"
                            "1. 반드시 해당 내용이 수록된 '정확한 원본 페이지 번호(예: p.87 등)'를 명시하세요.\\n"
                            "2. 지층, 심도, N치, 토질 특성 등 표(Table) 데이터는 마크다운 표로 깔끔하게 정리하세요.\\n"
                            "3. 제안설계 NGB 시추공, 기본설계 GB/NH/DT 시추공 등의 구분을 명확히 설명하세요.\\n"
                            "4. 추측하지 말고 문서에 명시된 사실만을 정확히 인용하세요."
                        )
                        
                        models_to_try = ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-flash-latest"]"""

new_extract_graph = """                        file_ref = gemini_file_manager.get_or_upload_file(client, file_path)
                        
                        system_prompt = (
                            "당신은 철도/토목/지반 엔지니어링 및 설계보고서, 시추주상도 분석 전문 AI입니다.\\n"
                            "제공된 대용량 PDF 문서 전체(수백 페이지)를 면밀히 분석하여 질문에 100% 팩트 기반으로 답변하세요.\\n\\n"
                            "[핵심 규칙]\\n"
                            "1. 반드시 해당 내용이 수록된 '정확한 원본 페이지 번호(예: p.87 등)'를 명시하세요.\\n"
                            "2. 지층, 심도, N치, 토질 특성 등 표(Table) 데이터는 마크다운 표로 깔끔하게 정리하세요.\\n"
                            "3. 제안설계 NGB 시추공, 기본설계 GB/NH/DT 시추공 등의 구분을 명확히 설명하세요.\\n"
                            "4. 추측하지 말고 문서에 명시된 사실만을 정확히 인용하세요."
                        )
                        
                        models_to_try = [
                            "gemini-3.8-flash",
                            "gemini-3.6-flash",
                            "gemini-3.5-flash-lite",
                            "gemini-flash-latest"
                        ]"""

if old_extract_graph in content:
    content = content.replace(old_extract_graph, new_extract_graph, 1)
    print("4. Fixed /api/extract-graph target_file_path bug and updated models!")
else:
    print("4. Warning: old_extract_graph not found!")

# Backup original and write updated
backup_path = server_path.with_suffix(".py.bak_before_fix")
backup_path.write_text(server_path.read_text(encoding="utf-8"), encoding="utf-8")
server_path.write_text(content, encoding="utf-8")
print(f"server.py successfully updated and backed up to {backup_path.name}!")
