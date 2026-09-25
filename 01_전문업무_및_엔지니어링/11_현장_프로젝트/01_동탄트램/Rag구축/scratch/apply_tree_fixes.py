import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
content = server_path.read_text(encoding='utf-8')

# 1. Add #docList to sidebar HTML
old_sidebar_part = """            <button onclick="promptCreateNewFolder()" title="사용자 정의 새 폴더 생성" style="flex-shrink: 0; padding: 6px 9px; font-size: 11px; font-weight: 600; background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; border-radius: 8px; cursor: pointer; display: flex; align-items: center; gap: 3px; transition: all 0.15s;">
              <span>➕ 새 폴더</span>
            </button>
          </div>
      </div>
      <div>
        <input type="file" id="fileInput" accept=".pdf" multiple style="display:none;" onchange="uploadDoc()">"""

new_sidebar_part = """            <button onclick="promptCreateNewFolder()" title="사용자 정의 새 폴더 생성" style="flex-shrink: 0; padding: 6px 9px; font-size: 11px; font-weight: 600; background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; border-radius: 8px; cursor: pointer; display: flex; align-items: center; gap: 3px; transition: all 0.15s;">
              <span>➕ 새 폴더</span>
            </button>
          </div>

          <!-- Document Tree Container -->
          <div class="doc-list" id="docList" style="max-height: calc(100vh - 360px); overflow-y: auto; margin-bottom: 12px; display: flex; flex-direction: column; gap: 6px;">
            <div style="font-size: 11px; color: var(--text-muted); padding: 8px; text-align: center;">문서 목록 불러오는 중...</div>
          </div>
      </div>
      <div>
        <input type="file" id="fileInput" accept=".pdf" multiple style="display:none;" onchange="uploadDoc()">"""

if old_sidebar_part in content:
    content = content.replace(old_sidebar_part, new_sidebar_part, 1)
    print("Successfully added #docList container!")
else:
    print("WARNING: old_sidebar_part not found!")

# 2. Fix promptMoveDocFolder and deleteDoc
# Find promptMoveDocFolder definition
p_move = content.find("function promptMoveDocFolder(event, docName) {")
p_move_end = content.find("function classifyDoc(docName) {", p_move)

if p_move != -1 and p_move_end != -1:
    new_move_func = """function promptMoveDocFolder(event, docName) {
    event.stopPropagation();
    const builtInFolders = currentDocTreeViewMode === 'zone' 
      ? ['00. 총괄 및 입찰·계약', '01. 1공구 본선', '02. 2공구 본선', '03. 차량기지', '04. 기술제안 및 특화', '05. 기타 및 일반']
      : ['총괄 · 계약', '토목 · 지반', '궤도 · 철도', '건축 · 정거장', '시스템 (신호/전기/통신)', '기타 · 일반'];
    const allFolders = Array.from(new Set([...builtInFolders, ...getCustomFolders()]));
    
    const nl = String.fromCharCode(10);
    const folderListStr = allFolders.map((f, i) => `${i + 1}. ${f}`).join(nl);
    const msg = `'${docName}' 문서를 이동할 폴더 번호(또는 새 폴더명)를 입력하세요:` + nl + nl + folderListStr;
    const selected = prompt(msg, '1');
    if (!selected) return;

    let targetFolder = null;
    const idx = parseInt(selected.trim(), 10);
    if (!isNaN(idx) && idx >= 1 && idx <= allFolders.length) {
      targetFolder = allFolders[idx - 1];
    } else if (selected.trim()) {
      targetFolder = selected.trim();
      const cf = getCustomFolders();
      if (!cf.includes(targetFolder)) {
        cf.push(targetFolder);
        saveCustomFolders(cf);
      }
    }

    if (targetFolder) {
      const map = getCustomDocFolderMap();
      map[docName] = targetFolder;
      saveCustomDocFolderMap(map);
      renderDocTree();
    }
  }

  """
    content = content[:p_move] + new_move_func + content[p_move_end:]
    print("Successfully updated promptMoveDocFolder with String.fromCharCode(10)!")
else:
    print("WARNING: promptMoveDocFolder not found!")

# 3. Check deleteDoc string literals
p_del = content.find("async function deleteDoc(event, name) {")
p_del_sub = content.find("if (!confirm(msg))", p_del)
if p_del != -1 and p_del_sub != -1:
    new_del_intro = """async function deleteDoc(event, name) {
      event.stopPropagation();
      const nl = String.fromCharCode(10);
      const msg = `'` + name + `' 문서를 보관함에서 내리시겠습니까?` + nl + nl + `※ 프로젝트 원본 파일은 안전하게 보존되며, 웹 화면(서버)에 업로드된 복사본 파일만 제거되어 디스크 용량이 확보됩니다.`;
      """
    content = content[:p_del] + new_del_intro + content[p_del_sub:]
    print("Successfully updated deleteDoc with safe newline strings!")

server_path.write_text(content, encoding='utf-8')
print("Saved server.py!")
