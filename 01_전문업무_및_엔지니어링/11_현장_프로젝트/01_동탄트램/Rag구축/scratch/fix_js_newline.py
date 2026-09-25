from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

# 문제의 라인 찾기
target_fragment = "let descHtml = (nodeData.rawDesc || `ID: ${nodeData.id}`)"
idx = content.find(target_fragment)
print("Found target fragment at:", idx)

if idx != -1:
    # 해당 줄부터 세미콜론까지 교체
    end_semicolon = content.find(";", idx)
    old_stmt = content[idx:end_semicolon+1]
    print("Old statement:")
    print(repr(old_stmt))
    
    # split('\\n').join('<br>') 은 정규식이 아니므로 어떤 환경에서도 100% 안전하게 동작함
    # 파이썬 원시 문자열 또는 확실한 이스케이프 사용
    new_stmt = r"let descHtml = (nodeData.rawDesc || `ID: ${nodeData.id}`).split('\\n').join('<br>');"
    # 실제 JS에는 .split('\n').join('<br>'); 형태로 들어가야 함:
    new_stmt = "let descHtml = (nodeData.rawDesc || `ID: ${nodeData.id}`).split('\\\\n').join('<br>');"
    
    content = content[:idx] + new_stmt + content[end_semicolon+1:]
    server_path.write_text(content, encoding="utf-8")
    print("Fixed statement with split/join!")
