# -*- coding: utf-8 -*-
from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

replacements = [
    (
        "조사-설계 상충(DISCREPANCY) 경고",
        "표층 연약지반(N<6) 및 고지하수위 설계 위험 경고"
    ),
    (
        "<strong>DISCREPANCY</strong> (상충 / 위험경고 엣지)",
        "<strong>DISCREPANCY</strong> (설계 위험 / 취약구간 엣지)"
    ),
    (
        "<h4>🚨 조사 ↔ 설계 불일치/리스크 알림</h4>",
        "<h4>🚨 표층 연약지반(N<6) 및 고지하수위 설계 위험 알림</h4>"
    ),
    (
        '<div id="discrepancyContent">검출된 불일치 없음</div>',
        '<div id="discrepancyContent">검출된 설계 위험 요인 없음</div>'
    )
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"Replaced: {old[:30]}... -> {new[:30]}...")
    else:
        print(f"Warning: Not found: {old[:30]}...")

server_path.write_text(content, encoding="utf-8")
print("Updated server.py successfully!")
