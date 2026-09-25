from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding="utf-8")

old_toolbar = """          <div class="graph-toolbar">
            <span style="font-size: 12px; font-weight: 600; color: var(--text-muted); margin-right: 4px;">구간 필터:</span>
            <button class="filter-chip active" onclick="applyGraphFilter('all', false, this)">전체 현장 (72공)</button>
            <button class="filter-chip" onclick="applyGraphFilter('depot', false, this)">차량기지 (GB)</button>
            <button class="filter-chip" onclick="applyGraphFilter('1', false, this)">1공구 본선 (NH)</button>
            <button class="filter-chip" onclick="applyGraphFilter('2', false, this)">2공구 본선 (DT)</button>
            <button class="filter-chip filter-chip-risk" onclick="applyGraphFilter('all', true, this)">⚠️ 연약층 위험구간 (25공)</button>
          </div>"""

new_toolbar = """          <div class="graph-toolbar">
            <span style="font-size: 12px; font-weight: 600; color: var(--text-muted); margin-right: 4px;">구간 필터:</span>
            <button class="filter-chip active" onclick="applyGraphFilter('all', false, this)">전체 현장 (77공)</button>
            <button class="filter-chip" onclick="applyGraphFilter('depot', false, this)">차량기지 전체 (GB+NGB)</button>
            <button class="filter-chip" onclick="applyGraphFilter('prop', false, this)">제안설계 기지 (NGB)</button>
            <button class="filter-chip" onclick="applyGraphFilter('1', false, this)">1공구 본선 (NH)</button>
            <button class="filter-chip" onclick="applyGraphFilter('2', false, this)">2공구 본선 (DT)</button>
            <button class="filter-chip filter-chip-risk" onclick="applyGraphFilter('all', true, this)">⚠️ 연약층 위험구간 (28공)</button>
          </div>"""

if old_toolbar in content:
    content = content.replace(old_toolbar, new_toolbar)
    server_path.write_text(content, encoding="utf-8")
    print("Toolbar updated with NGB filter chip!")
else:
    import re
    content = re.sub(r'<div class="graph-toolbar">.*?</div>', new_toolbar, content, flags=re.DOTALL)
    server_path.write_text(content, encoding="utf-8")
    print("Toolbar updated via regex!")
