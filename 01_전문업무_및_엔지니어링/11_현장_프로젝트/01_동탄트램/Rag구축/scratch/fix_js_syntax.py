from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

# 문제의 패턴 찾기
target_broken = "let descHtml = (nodeData.rawDesc || `ID: ${nodeData.id}`).replace(/\n/g, '<br>');"
target_fixed = "let descHtml = (nodeData.rawDesc || `ID: ${nodeData.id}`).replaceAll('\\n', '<br>');"

if target_broken in content:
    content = content.replace(target_broken, target_fixed)
    server_path.write_text(content, encoding="utf-8")
    print("Fixed broken regex using exact match!")
else:
    # Regex or replace check
    import re
    new_content = re.sub(
        r"let descHtml = \(nodeData\.rawDesc \|\| `ID: \$\{nodeData\.id\}`\)\.replace\(/[\r\n]+/g, '<br>'\);",
        target_fixed,
        content
    )
    if new_content != content:
        server_path.write_text(new_content, encoding="utf-8")
        print("Fixed broken regex using regex pattern!")
    else:
        # Check where descHtml is
        idx = content.find("descHtml =")
        print("descHtml context:")
        print(content[idx:idx+150])
        # Replace whatever is after descHtml =
        part1 = content[:idx]
        part2 = content[idx:]
        fixed_part2 = re.sub(r"descHtml = [^;]+;", "descHtml = (nodeData.rawDesc || `ID: ${nodeData.id}`).replaceAll('\\n', '<br>');", part2, count=1)
        server_path.write_text(part1 + fixed_part2, encoding="utf-8")
        print("Fixed descHtml line directly!")

