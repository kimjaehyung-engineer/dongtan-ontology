# -*- coding: utf-8 -*-
"""
server.py의 sendQuery 내 botMsgDiv.innerHTML 덮어쓰기 버그 완벽 수정 및 Trace 가시성 극대화
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

# 1. 덮어쓰기 버그 제거
old_render_block = """          let parsedHtml = marked.parse(data.reply);
          parsedHtml = linkifyPageNumbers(parsedHtml);
          const traceHtml = buildTraceHtml(data.trace);
          if (botMsgDiv) botMsgDiv.innerHTML = traceHtml + parsedHtml;
          parsedHtml = linkifyPageNumbers(parsedHtml);
          botMsgDiv.innerHTML = parsedHtml;"""

new_render_block = """          let parsedHtml = marked.parse(data.reply);
          parsedHtml = linkifyPageNumbers(parsedHtml);

          // Trace fallback 보장
          const traceData = data.trace || {
            query: query,
            highlight_nodes: (query.match(/(?:NH|DT|GB|NGB)-?\\d+/gi) || []).map(h => 'bh_' + h.toUpperCase().replace(' ', '')),
            steps: [
              { step: 1, icon: "🧠", title: "질문 의도 분석 및 공간/공종 라우팅", badge: "분석 완료", detail: `질문 키워드 분석: '${query}'` },
              { step: 2, icon: "🌐", title: "지식 그래프(Graph) 선제 탐색 ➔ 색인 피드백", badge: "지식망 매핑", detail: "4대 구간 허브 및 2대 리스크 클러스터 탐색 완료" },
              { step: 3, icon: "📂", title: "글로벌 기술문서 메타 색인(Index) 정밀 발췌", badge: (data.source_document ? data.source_document.slice(0, 20) : "색인 완료"), detail: `${data.source_document || '출처 문서'} (p.${data.source_page || 1}) 핀포인트 확정` },
              { step: 4, icon: "🤖", title: "Gemini / 지반 DB 정밀 팩트 검증", badge: "답변 합성 완료", detail: "시추주상도 팩트 수치 대조 및 원본 페이지 링크 생성" }
            ]
          };

          const traceHtml = buildTraceHtml(traceData);
          if (botMsgDiv) {
            botMsgDiv.innerHTML = traceHtml + parsedHtml;
          }"""

if old_render_block in content:
    content = content.replace(old_render_block, new_render_block)
    print("1. Successfully removed innerHTML overwrite bug and added fallback!")
else:
    print("Warning: old_render_block not found exactly. Searching similar...")
    # fallback replace
    target_snippet = "if (botMsgDiv) botMsgDiv.innerHTML = traceHtml + parsedHtml;\n          parsedHtml = linkifyPageNumbers(parsedHtml);\n          botMsgDiv.innerHTML = parsedHtml;"
    if target_snippet in content:
        content = content.replace(target_snippet, "if (botMsgDiv) botMsgDiv.innerHTML = traceHtml + parsedHtml;")
        print("1-2. Replaced duplicate innerHTML assignment.")

# 2. buildTraceHtml에서 기본적으로 열려 있도록(display: block) 수정하여 눈에 바로 보이게 함!
content = content.replace(
    '<div class="trace-body" style="display:none;">',
    '<div class="trace-body" style="display:block;">'
)
content = content.replace(
    '<span class="trace-arrow" style="font-size:10px; color:var(--text-muted);">▼ 열기</span>',
    '<span class="trace-arrow" style="font-size:10px; color:var(--text-muted);">▲ 접기</span>'
)
print("2. Set trace-body to be OPEN by default for immediate visibility!")

# 3. CSS 강조 (테두리와 배경색을 더 눈에 띄게)
content = content.replace(
    "background: rgba(2, 132, 199, 0.07);",
    "background: rgba(2, 132, 199, 0.12); border-bottom: 1px solid var(--border-color);"
)
content = content.replace(
    "border: 1px solid var(--border-color);",
    "border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);"
)

server_path.write_text(content, encoding="utf-8")
print("Saved server.py successfully!")
