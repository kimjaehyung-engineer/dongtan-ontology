# -*- coding: utf-8 -*-
import sys
import os
import re
import py_compile
from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# ==============================================================================
# Part 1: Top definitions (DOCS_ROOT, scan_folder_tree, helpers)
# ==============================================================================
old_docs_def = 'DOCS_DIR = Path(__file__).parent / "documents"\nENV_FILE = Path(__file__).parent / ".env"'
new_docs_def = '''DOCS_DIR = Path(__file__).parent / "documents"
ENV_FILE = Path(__file__).parent / ".env"
RAG_CONFIG_FILE = Path(__file__).parent / "rag_config.json"
DEFAULT_SOURCE_DOCS = Path(r"C:\\Users\\sskjh\\antigravity\\01_전문업무_및_엔지니어링\\11_현장_프로젝트\\01_동탄트램\\Rag구축\\01_SOURCE_DOCUMENTS")

def get_configured_docs_root() -> Path:
    if RAG_CONFIG_FILE.exists():
        try:
            import json
            with open(RAG_CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                custom_root = cfg.get("docs_root_path")
                if custom_root and Path(custom_root).exists() and Path(custom_root).is_dir():
                    return Path(custom_root)
        except Exception:
            pass
    if DEFAULT_SOURCE_DOCS.exists() and DEFAULT_SOURCE_DOCS.is_dir():
        return DEFAULT_SOURCE_DOCS
    return DOCS_DIR

def set_configured_docs_root(path_str: str) -> bool:
    target = Path(path_str)
    if not target.exists() or not target.is_dir():
        return False
    cfg = {}
    import json
    if RAG_CONFIG_FILE.exists():
        try:
            with open(RAG_CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            pass
    cfg["docs_root_path"] = str(target.resolve())
    with open(RAG_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    return True

def scan_folder_tree(root_dir: Path):
    valid_exts = {".pdf", ".xlsx", ".xls", ".hwp", ".hwpx", ".docx", ".txt", ".csv"}
    all_files = []
    meta_map = {}
    if META_INDEX_FILE.exists():
        try:
            import json
            with open(META_INDEX_FILE, "r", encoding="utf-8") as f:
                meta_map = json.load(f)
        except Exception:
            pass

    for p in root_dir.rglob("*"):
        if not p.is_file():
            continue
        if p.name.startswith("~") or p.name.startswith("."):
            continue
        if p.suffix.lower() not in valid_exts:
            continue
            
        rel = p.relative_to(root_dir)
        size_mb = round(p.stat().st_size / (1024 * 1024), 2)
        folders = list(rel.parent.parts)
        rel_str = str(rel).replace("\\\\", "/")
        
        doc_info = {
            "name": p.name,
            "rel_path": rel_str,
            "folders": folders,
            "size_mb": size_mb,
            "ext": p.suffix.lower()
        }
        
        if p.name in meta_map:
            m = meta_map[p.name]
            doc_info["total_pages"] = m.get("total_pages", 0)
            doc_info["sections"] = [
                {"title": s["title"], "start_page": s["start_page"], "end_page": s["end_page"], "facility": s.get("facility", [])}
                for s in m.get("sections", [])
            ]
        all_files.append(doc_info)
        
    tree_root = {"name": root_dir.name, "type": "folder", "path": "", "children": {}}
    for item in all_files:
        curr = tree_root
        accum_path = []
        for folder in item["folders"]:
            accum_path.append(folder)
            subpath = "/".join(accum_path)
            if folder not in curr["children"]:
                curr["children"][folder] = {
                    "name": folder,
                    "type": "folder",
                    "path": subpath,
                    "children": {}
                }
            curr = curr["children"][folder]
            
        curr["children"][item["name"]] = {
            "name": item["name"],
            "type": "file",
            "rel_path": item["rel_path"],
            "size_mb": item["size_mb"],
            "ext": item["ext"],
            "total_pages": item.get("total_pages", 0)
        }
        
    def dict_to_list(node):
        if node["type"] == "folder":
            folders = []
            files = []
            for k, child in node["children"].items():
                processed = dict_to_list(child)
                if processed["type"] == "folder":
                    folders.append(processed)
                else:
                    files.append(processed)
            folders.sort(key=lambda x: x["name"])
            files.sort(key=lambda x: x["name"])
            node["children"] = folders + files
            node["total_files"] = sum(c.get("total_files", 1) if c["type"] == "folder" else 1 for c in node["children"])
        return node
        
    final_tree = dict_to_list(tree_root)
    return {
        "root_path": str(root_dir),
        "total_count": len(all_files),
        "docs": all_files,
        "tree": final_tree
    }'''

if old_docs_def in code:
    code = code.replace(old_docs_def, new_docs_def, 1)
    print("[OK] Part 1: Top definitions replaced")
else:
    print("[Skip/Already applied] Part 1")

# ==============================================================================
# Part 2: Sidebar HTML Markup
# ==============================================================================
old_sidebar_pattern = r'<!-- 2-Way Tree Switcher \+ New Folder Button -->[\s\S]*?<!-- Document Tree Container -->\s*<div class="doc-list" id="docList"[\s\S]*?</div>\s*</div>\s*<div>\s*<input type="file" id="fileInput"[\s\S]*?➕ 새 시방서/보고서 PDF 추가\s*</button>\s*</div>'

new_sidebar_markup = '''<!-- Root Folder Info & Action Bar -->
        <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 8px; padding: 8px 10px; margin-bottom: 8px;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
            <span style="font-size: 11px; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 4px;">
              <span>📁</span> 참조 상위 폴더
            </span>
            <div style="display: flex; gap: 4px;">
              <button onclick="changeRootFolder()" style="font-size: 10px; padding: 3px 8px; border-radius: 5px; background: #2563eb; color: #fff; border: none; cursor: pointer; font-weight: 600;" title="참조할 PC 상위 폴더 경로 변경">경로 변경</button>
              <button onclick="fetchDocs()" title="하위 폴더/문서 즉시 재스캔 및 동기화" style="font-size: 10px; padding: 3px 6px; border-radius: 5px; background: #e2e8f0; color: #334155; border: none; cursor: pointer; font-weight: 600;">🔄</button>
            </div>
          </div>
          <div id="rootFolderPathDisplay" style="font-size: 10px; color: #475569; font-family: monospace; word-break: break-all; line-height: 1.35; max-height: 40px; overflow-y: auto; background: #ffffff; padding: 3px 6px; border-radius: 4px; border: 1px solid #e2e8f0;" title="현재 참조 중인 상위 폴더">
            불러오는 중...
          </div>
        </div>

        <!-- Document Tree Container -->
        <div class="doc-list" id="docList" style="max-height: calc(100vh - 350px); overflow-y: auto; margin-bottom: 8px; display: flex; flex-direction: column; gap: 4px; padding-right: 4px;">
          <div style="font-size: 11px; color: var(--text-muted); padding: 8px; text-align: center;">문서 목록 불러오는 중...</div>
        </div>
      </div>
      <div style="display: flex; gap: 4px;">
        <button class="upload-btn" onclick="openRootInExplorer()" style="flex: 1; padding: 8px; font-size: 11px; background: #f8fafc; color: #2563eb; border: 1.5px solid #bfdbfe; font-weight: 600; border-radius: 8px; cursor: pointer;" title="윈도우 탐색기로 상위 폴더 열기">
          📂 윈도우 탐색기 열기
        </button>
        <button onclick="fetchDocs()" style="padding: 8px 12px; font-size: 11px; background: #eff6ff; color: #1d4ed8; border: 1.5px solid #bfdbfe; border-radius: 8px; cursor: pointer; font-weight: 600;" title="폴더 변경사항 즉시 동기화">
          🔄 동기화
        </button>
      </div>'''

match_sidebar = re.search(old_sidebar_pattern, code)
if match_sidebar:
    code = code[:match_sidebar.start()] + new_sidebar_markup + code[match_sidebar.end():]
    print("[OK] Part 2: Sidebar markup replaced")
else:
    print("[Warning] Part 2: Sidebar pattern not matched directly")

# ==============================================================================
# Part 3: Tree JS & Document viewer logic
# ==============================================================================
old_js_pattern = r'function getCustomFolders\(\)\s*\{[\s\S]*?async function deleteDoc\([\s\S]*?window\.cachedDocs = \[\];\s*let currentViewingDoc = null;'

new_tree_js = '''  window.docsRootPath = '';
  window.cachedDocs = [];
  window.cachedTree = null;
  let currentViewingDoc = null;
  let currentViewingRelPath = null;

  async function changeRootFolder() {
    const currentPath = window.docsRootPath || '';
    const newPath = prompt('참조할 상위 폴더(루트 경로)를 입력하세요:\\n(해당 폴더 아래의 모든 하위 폴더와 파일이 계층 구조 그대로 자동 연동됩니다)', currentPath);
    if (!newPath || !newPath.trim() || newPath.trim() === currentPath) return;

    try {
      const res = await fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ docs_root_path: newPath.trim() })
      });
      const data = await res.json();
      if (data.status === 'ok') {
        alert(`상위 폴더가 설정되었습니다:\\n${data.docs_root_path}\\n\\n하위 모든 폴더 및 문서를 다시 스캔합니다.`);
        await fetchDocs();
      } else {
        alert(`폴더 설정 실패: ${data.error || '폴더가 존재하지 않거나 접근할 수 없습니다.'}`);
      }
    } catch(e) {
      alert(`오류 발생: ${e.message}`);
    }
  }

  async function openRootInExplorer() {
    try {
      const res = await fetch('/api/open_explorer', { method: 'POST' });
      const data = await res.json();
      if (!res.ok) {
        alert('탐색기 열기 실패: ' + (data.error || '오류'));
      }
    } catch(e) {
      alert('요청 실패: ' + e.message);
    }
  }

  async function fetchDocs() {
    try {
      const res = await fetch('/api/documents?tree=true');
      const data = await res.json();
      
      if (data.root_path) {
        window.docsRootPath = data.root_path;
        const rootDisplay = document.getElementById('rootFolderPathDisplay');
        if (rootDisplay) {
          rootDisplay.innerText = data.root_path;
          rootDisplay.title = data.root_path;
        }
      }
      
      window.cachedDocs = data.docs || (Array.isArray(data) ? data : []);
      window.cachedTree = data.tree || null;
      
      const badge = document.getElementById('docCountBadge');
      if (badge) {
        badge.innerText = `총 ${window.cachedDocs.length}개 파일 연동`;
      }
      
      renderDocTree();
    } catch(e) {
      console.error(e);
    }
  }

  function renderDocTree() {
    const listEl = document.getElementById('docList');
    if (!listEl) return;
    listEl.innerHTML = '';

    const tree = window.cachedTree;
    if (!tree || !tree.children || tree.children.length === 0) {
      listEl.innerHTML = '<div style="font-size:12px; color:var(--text-muted); padding:12px; text-align:center;">지정된 상위 폴더에 참조 가능한 문서가 없습니다.</div>';
      return;
    }

    // Render tree children (if root has single folder, unwrap or render direct)
    tree.children.forEach(child => {
      listEl.appendChild(createTreeNodeElement(child, 1));
    });
  }

  function createTreeNodeElement(node, depth) {
    if (node.type === 'folder') {
      const folderEl = document.createElement('div');
      // Top 2 levels open by default
      const defaultOpen = depth <= 2;
      folderEl.className = 'tree-folder' + (defaultOpen ? ' open' : '');
      folderEl.style.marginLeft = depth > 1 ? '6px' : '0px';
      folderEl.style.borderLeft = depth > 1 ? '2px solid #cbd5e1' : '';
      folderEl.style.paddingLeft = depth > 1 ? '6px' : '0px';

      const headerEl = document.createElement('div');
      headerEl.className = 'folder-header';
      headerEl.style.display = 'flex';
      headerEl.style.alignItems = 'center';
      headerEl.style.gap = '6px';
      headerEl.style.padding = '6px 8px';
      headerEl.style.cursor = 'pointer';
      headerEl.style.borderRadius = '6px';

      headerEl.innerHTML = `
        <span class="folder-arrow" style="font-size: 10px; color: #64748b; transition: transform 0.2s; display: inline-block;">${defaultOpen ? '▼' : '▶'}</span>
        <span class="folder-icon" style="font-size: 13px;">📁</span>
        <span class="folder-title" title="${node.name}" style="flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-weight:600; font-size:11.5px; color:var(--text-color, #1e293b);">${node.name}</span>
        <span class="folder-badge" style="font-size:10px; background:#e2e8f0; color:#475569; padding:1px 6px; border-radius:10px; font-weight:600;">${node.total_files || (node.children ? node.children.length : 0)}</span>
      `;

      const contentEl = document.createElement('div');
      contentEl.className = 'folder-content';
      contentEl.style.display = defaultOpen ? 'flex' : 'none';
      contentEl.style.flexDirection = 'column';
      contentEl.style.gap = '3px';
      contentEl.style.marginTop = '3px';

      headerEl.onclick = (e) => {
        e.stopPropagation();
        const isOpen = contentEl.style.display !== 'none';
        contentEl.style.display = isOpen ? 'none' : 'flex';
        headerEl.querySelector('.folder-arrow').textContent = isOpen ? '▶' : '▼';
        folderEl.classList.toggle('open', !isOpen);
      };

      if (node.children && node.children.length > 0) {
        node.children.forEach(sub => {
          contentEl.appendChild(createTreeNodeElement(sub, depth + 1));
        });
      } else {
        contentEl.innerHTML = '<div style="font-size:10.5px; color:var(--text-muted); padding:3px 8px;">(빈 폴더)</div>';
      }

      folderEl.appendChild(headerEl);
      folderEl.appendChild(contentEl);
      return folderEl;
    } else {
      // File node
      const doc = node;
      const item = document.createElement('div');
      const isAct = (typeof currentViewingDoc !== 'undefined' && (currentViewingDoc === doc.name || currentViewingDoc === doc.rel_path));
      item.className = 'tree-doc-item' + (isAct ? ' active' : '');
      item.style.marginLeft = depth > 1 ? '4px' : '0px';

      let icon = '📄';
      if (doc.ext === '.xlsx' || doc.ext === '.xls' || doc.ext === '.csv') icon = '📊';
      else if (doc.ext === '.hwp' || doc.ext === '.hwpx' || doc.ext === '.docx') icon = '📝';
      else if (doc.ext === '.txt') icon = '📃';

      item.onclick = (e) => {
        e.stopPropagation();
        viewDoc(doc.rel_path, doc.name);
        document.querySelectorAll('.tree-doc-item').forEach(el => el.classList.remove('active'));
        item.classList.add('active');
      };

      item.innerHTML = `
        <span class="tree-doc-icon">${icon}</span>
        <div class="tree-doc-info" style="flex:1; min-width:0;">
          <div class="tree-doc-name" title="${doc.name}" style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis; font-size:11.5px; font-weight:500;">${doc.name}</div>
          <div class="tree-doc-meta" style="font-size:10px; color:var(--text-muted);">${doc.size_mb} MB${doc.total_pages ? ' · ' + doc.total_pages + 'p' : ''}</div>
        </div>
        <div class="tree-doc-actions">
          <button class="tree-btn-view" title="웹 뷰어에서 문서 열람" onclick="event.stopPropagation(); viewDoc('${doc.rel_path}', '${doc.name}');">열람</button>
          <a href="/api/download?path=${encodeURIComponent(doc.rel_path)}" download="${doc.name}" class="tree-btn-view" style="text-decoration:none; background:#f1f5f9; color:#475569; border-color:#cbd5e1;" title="파일 다운로드" onclick="event.stopPropagation();">받기</a>
        </div>
      `;
      return item;
    }
  }

  function viewDoc(relPath, name) {
    const docName = name || relPath;
    currentViewingDoc = docName;
    currentViewingRelPath = relPath || docName;
    loadViewerDoc(currentViewingRelPath, 1);
    toggleViewerPanel(true);
    const topRef = document.getElementById('topSourceRef');
    if (topRef) {
      topRef.innerHTML = `📖 <b>직접 열람 중:</b> <span style="color:var(--text-color);">${docName}</span>`;
    }
    const topDlBtn = document.getElementById('topDownloadBtn');
    if (topDlBtn) {
      topDlBtn.style.display = 'inline-flex';
      topDlBtn.onclick = () => window.open(`/api/download?path=${encodeURIComponent(currentViewingRelPath)}`, '_blank');
    }
  }'''

match_js = re.search(old_js_pattern, code)
if match_js:
    code = code[:match_js.start()] + new_tree_js + "\n\n" + code[match_js.end():]
    print("[OK] Part 3: Tree JS replaced")
else:
    print("[Warning] Part 3: Old JS pattern not matched directly")

# ==============================================================================
# Part 4: loadViewerDoc update to support path and non-PDF preview
# ==============================================================================
old_load_viewer = '''      if (iframe) {
        // Enforce reliable reload with timestamp to guarantee browser jumps to #page
        iframe.src = `/api/view?document=${encodeURIComponent(name)}&t=${Date.now()}#page=${effectiveTargetPage}`;
        iframe.style.display = 'block';
      }
      if (placeholder) {
        placeholder.style.display = 'none';
      }'''

new_load_viewer = '''      const isPdf = name.toLowerCase().endsWith('.pdf');
      if (iframe && isPdf) {
        iframe.src = `/api/view?path=${encodeURIComponent(name)}&t=${Date.now()}#page=${effectiveTargetPage}`;
        iframe.style.display = 'block';
        if (placeholder) placeholder.style.display = 'none';
      } else if (!isPdf) {
        if (iframe) iframe.style.display = 'none';
        if (placeholder) {
          placeholder.style.display = 'flex';
          placeholder.innerHTML = `
            <div style="text-align: center; padding: 40px 20px;">
              <div style="font-size: 48px; margin-bottom: 12px;">📊</div>
              <h3 style="margin-bottom: 8px; color: var(--text-color);">${name}</h3>
              <p style="color: var(--text-muted); font-size: 13px; margin-bottom: 20px;">
                본 파일은 스프레드시트 또는 기술 보고서 데이터입니다.<br>
                AI 질의 시 본 파일의 내용 및 정수를 자동으로 분석·참조합니다.
              </p>
              <a href="/api/download?path=${encodeURIComponent(name)}" class="btn-primary" style="display: inline-flex; align-items: center; gap: 6px; padding: 10px 18px; border-radius: 8px; background: #2563eb; color: #fff; text-decoration: none; font-weight: 600;">
                ⬇️ 파일 다운로드 및 열기
              </a>
            </div>
          `;
        }
      }'''

if old_load_viewer in code:
    code = code.replace(old_load_viewer, new_load_viewer, 1)
    print("[OK] Part 4: loadViewerDoc updated")
else:
    print("[Warning] Part 4: old_load_viewer not found")

# ==============================================================================
# Part 5: jumpToPage update for path
# ==============================================================================
old_jump = 'iframe.src = `/api/view?document=${encodeURIComponent(currentViewingDoc)}&t=${Date.now()}#page=${pageNum}`;'
new_jump = 'iframe.src = `/api/view?path=${encodeURIComponent(currentViewingRelPath || currentViewingDoc)}&t=${Date.now()}#page=${pageNum}`;'
if old_jump in code:
    code = code.replace(old_jump, new_jump)
    print("[OK] Part 5: jumpToPage updated")

# ==============================================================================
# Part 6: do_GET routes (/api/documents, /api/view, /api/download, /api/config)
# ==============================================================================
old_routes_pattern = r'elif self\.path == "/api/documents":[\s\S]*?elif self\.path == "/api/config":[\s\S]*?self\.respond_json\({\s*"server_ip": ip,\s*"port": PORT,\s*"api_key": masked_key\s*}\)'

new_routes = '''elif self.path.startswith("/api/documents"):
            root = get_configured_docs_root()
            tree_data = scan_folder_tree(root)
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            if params.get("tree", ["false"])[0].lower() in ("true", "1") or params.get("format", [""])[0].lower() == "tree":
                self.respond_json(tree_data)
            else:
                self.respond_json(tree_data["docs"])

        elif self.path.startswith("/api/graph/master"):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            section = params.get("section", [None])[0]
            risk_only = params.get("risk_only", ["false"])[0].lower() in ("true", "1")
            try:
                import graph_engine
                data = graph_engine.build_master_graph(section=section, risk_only=risk_only)
                self.respond_json(data)
            except Exception as e:
                self.respond_json({"error": str(e)}, 500)

        elif self.path.startswith("/api/download") or self.path.startswith("/api/view"):
            is_download = self.path.startswith("/api/download")
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            doc_param = params.get("path", [None])[0] or params.get("document", [None])[0]
            if not doc_param:
                self.send_response(400)
                self.end_headers()
                return

            root = get_configured_docs_root()
            file_path = (root / doc_param).resolve()
            if not file_path.exists():
                matches = list(root.rglob(Path(doc_param).name))
                if matches:
                    file_path = matches[0]
                elif (DOCS_DIR / Path(doc_param).name).exists():
                    file_path = DOCS_DIR / Path(doc_param).name

            if not file_path.exists():
                self.send_response(404)
                self.end_headers()
                return

            try:
                file_size = file_path.stat().st_size
                ext = file_path.suffix.lower()
                content_type = "application/octet-stream"
                if ext == ".pdf":
                    content_type = "application/pdf"
                elif ext == ".xlsx":
                    content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                elif ext == ".xls":
                    content_type = "application/vnd.ms-excel"
                elif ext in (".hwp", ".hwpx"):
                    content_type = "application/x-hwp"
                elif ext == ".txt":
                    content_type = "text/plain; charset=utf-8"

                self.send_response(200)
                self.send_header("Content-Type", content_type)
                quoted_name = urllib.parse.quote(file_path.name)
                disposition = "attachment" if (is_download or ext != ".pdf") else "inline"
                self.send_header("Content-Disposition", f"{disposition}; filename*=UTF-8''{quoted_name}")
                self.send_header("Content-Length", str(file_size))
                self.send_header("Accept-Ranges", "bytes")
                self.end_headers()
                with open(file_path, "rb") as f:
                    while chunk := f.read(1024 * 1024):
                        self.wfile.write(chunk)
            except Exception:
                pass

        elif self.path == "/api/config":
            key = load_env_api_key()
            masked_key = key if key else ""
            ip = get_server_ip()
            self.respond_json({
                "server_ip": ip,
                "port": PORT,
                "api_key": masked_key,
                "docs_root_path": str(get_configured_docs_root())
            })'''

match_routes = re.search(old_routes_pattern, code)
if match_routes:
    code = code[:match_routes.start()] + new_routes + code[match_routes.end():]
    print("[OK] Part 6: do_GET routes replaced")
else:
    print("[Warning] Part 6: old_routes_pattern not matched directly")

# ==============================================================================
# Part 7: do_POST routes (/api/config with docs_root_path, /api/open_explorer)
# ==============================================================================
old_post_config = '''        if self.path == "/api/config":
            content_len = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_len).decode("utf-8"))
            if "api_key" in body and body["api_key"].strip():
                save_env_api_key(body["api_key"].strip())
            self.respond_json({"status": "ok"})'''

new_post_config = '''        if self.path == "/api/config":
            content_len = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_len).decode("utf-8"))
            if "api_key" in body and body["api_key"].strip():
                save_env_api_key(body["api_key"].strip())
            if "docs_root_path" in body and body["docs_root_path"].strip():
                success = set_configured_docs_root(body["docs_root_path"].strip())
                if not success:
                    self.respond_json({"error": "유효하지 않거나 존재하지 않는 디렉토리입니다."}, 400)
                    return
            self.respond_json({"status": "ok", "docs_root_path": str(get_configured_docs_root())})

        elif self.path == "/api/open_explorer":
            root = get_configured_docs_root()
            try:
                import subprocess
                subprocess.Popen(f'explorer "{str(root)}"', shell=True)
                self.respond_json({"status": "ok", "opened": str(root)})
            except Exception as e:
                self.respond_json({"error": str(e)}, 500)'''

if old_post_config in code:
    code = code.replace(old_post_config, new_post_config, 1)
    print("[OK] Part 7: do_POST config & open_explorer added")
else:
    print("[Warning] Part 7: old_post_config not found directly")

# ==============================================================================
# Part 8: /api/chat target_file_path resolution
# ==============================================================================
old_fp_line = 'fp = DOCS_DIR / dn'
new_fp_line = '''root = get_configured_docs_root()
                        fp = root / dn
                        if not fp.exists():
                            matches = list(root.rglob(dn))
                            fp = matches[0] if matches else (DOCS_DIR / dn)'''
if old_fp_line in code:
    code = code.replace(old_fp_line, new_fp_line, 1)
    print("[OK] Part 8: /api/chat fp resolution replaced")

old_primary_block = '''                # Fallback: #3편 증빙자료 or first available
                primary_doc = DOCS_DIR / "#3편 증빙자료_토질 및 기초.pdf"
                if primary_doc.exists():
                    target_file_path = primary_doc
                    target_doc_name = primary_doc.name
                else:
                    pdf_files = list(DOCS_DIR.glob("*.pdf"))
                    if pdf_files:
                        target_file_path = pdf_files[0]
                        target_doc_name = target_file_path.name
                    else:
                        self.respond_json({"error": "보관소에 분석할 PDF 문서가 없습니다."}, 404)
                        return'''

new_primary_block = '''                # Fallback: #3편 증빙자료 or first available in root
                root = get_configured_docs_root()
                primary_doc = root / "#3편 증빙자료_토질 및 기초.pdf"
                if not primary_doc.exists():
                    matches = list(root.rglob("#3편 증빙자료*"))
                    if matches:
                        primary_doc = matches[0]
                    else:
                        primary_doc = DOCS_DIR / "#3편 증빙자료_토질 및 기초.pdf"

                if primary_doc.exists():
                    target_file_path = primary_doc
                    target_doc_name = primary_doc.name
                else:
                    pdf_files = list(root.rglob("*.pdf"))
                    if not pdf_files:
                        pdf_files = list(DOCS_DIR.glob("*.pdf"))
                    if pdf_files:
                        target_file_path = pdf_files[0]
                        target_doc_name = target_file_path.name
                    else:
                        self.respond_json({"error": "지정된 상위 폴더에 분석할 PDF 문서가 없습니다."}, 404)
                        return'''

if old_primary_block in code:
    code = code.replace(old_primary_block, new_primary_block, 1)
    print("[OK] Part 8b: /api/chat primary_doc fallback replaced")

# Save and verify
test_output_path = Path("scratch/server_patched.py")
with open(test_output_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Compiling patched code...")
try:
    py_compile.compile(str(test_output_path), doraise=True)
    print("SUCCESS: Code compiled with NO syntax errors!")
    
    # Overwrite server.py with the verified patched code
    with open(server_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("Wrote patched server.py successfully!")
except Exception as e:
    print(f"COMPILE ERROR: {e}")
    sys.exit(1)
