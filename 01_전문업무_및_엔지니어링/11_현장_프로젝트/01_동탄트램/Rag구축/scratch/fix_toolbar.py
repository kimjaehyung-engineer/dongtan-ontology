from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

pos = content.find('id="networkCanvas"')
print("Found networkCanvas at:", pos)
if pos != -1:
    print("Surrounding text:")
    print(content[pos-100:pos+100])

toolbar_html = """          <div class="graph-toolbar">
            <span style="font-size: 12px; font-weight: 600; color: var(--text-muted); margin-right: 4px;">구간 필터:</span>
            <button class="filter-chip active" onclick="applyGraphFilter('all', false, this)">전체 현장 (72공)</button>
            <button class="filter-chip" onclick="applyGraphFilter('depot', false, this)">차량기지 (GB)</button>
            <button class="filter-chip" onclick="applyGraphFilter('1', false, this)">1공구 본선 (NH)</button>
            <button class="filter-chip" onclick="applyGraphFilter('2', false, this)">2공구 본선 (DT)</button>
            <button class="filter-chip filter-chip-risk" onclick="applyGraphFilter('all', true, this)">⚠️ 연약층 위험구간 (25공)</button>
          </div>
          <div id="graphLoadingOverlay" class="graph-loading" style="display:none;">
            <div class="loading-spinner" style="width:28px; height:28px; border-width:3px;"></div>
            <div style="font-size: 13px; font-weight: 600; color: var(--text-main);">지반-공종 지식 그래프 로딩 중...</div>
          </div>
"""

if 'class="graph-toolbar"' not in content:
    target = '<div class="graph-canvas-area">\n          <div id="networkCanvas">'
    if target in content:
        content = content.replace(target, '<div class="graph-canvas-area">\n' + toolbar_html + '          <div id="networkCanvas">')
        server_path.write_text(content, encoding="utf-8")
        print("Toolbar successfully added!")
    else:
        # Regex or flexible match
        import re
        content = re.sub(
            r'(<div class="graph-canvas-area">\s*)<div id="networkCanvas">',
            r'\1' + toolbar_html + '<div id="networkCanvas">',
            content
        )
        server_path.write_text(content, encoding="utf-8")
        print("Toolbar added via regex!")
else:
    print("Toolbar already present.")
