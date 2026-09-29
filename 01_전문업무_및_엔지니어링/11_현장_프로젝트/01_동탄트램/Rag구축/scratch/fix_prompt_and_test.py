# -*- coding: utf-8 -*-
import sys
import os
import py_compile
import subprocess
from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# 1. Fix prompt newline issue
bad_prompt_start = "async function changeRootFolder() {"
bad_prompt_end = "async function fetchDocs() {"

idx1 = text.find(bad_prompt_start)
idx2 = text.find(bad_prompt_end)

if idx1 == -1 or idx2 == -1:
    print(f"Error: could not find boundary ({idx1}, {idx2})")
    sys.exit(1)

clean_js = '''async function changeRootFolder() {
    const currentPath = window.docsRootPath || '';
    const newPath = prompt("참조할 상위 폴더(루트 경로)를 입력하세요 (하위 모든 폴더/문서 자동 연동):", currentPath);
    if (!newPath || !newPath.trim() || newPath.trim() === currentPath) return;

    try {
      const res = await fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ docs_root_path: newPath.trim() })
      });
      const data = await res.json();
      if (data.status === 'ok') {
        alert("상위 폴더가 설정되었습니다:\\n" + data.docs_root_path);
        await fetchDocs();
      } else {
        alert("폴더 설정 실패: " + (data.error || '폴더가 존재하지 않거나 접근할 수 없습니다.'));
      }
    } catch(e) {
      alert("오류 발생: " + e.message);
    }
  }

  async function openRootInExplorer(event) {
    const btn = (event && event.currentTarget) ? event.currentTarget : document.querySelector('button[onclick*="openRootInExplorer"]');
    const oldHtml = btn ? btn.innerHTML : '';
    if (btn) btn.innerHTML = '📂 탐색기 여는 중...';
    try {
      const res = await fetch('/api/open_explorer', { method: 'POST' });
      const data = await res.json();
      if (!res.ok) {
        alert('탐색기 열기 실패: ' + (data.error || '오류 발생'));
      }
    } catch(e) {
      alert('요청 실패: ' + e.message);
    } finally {
      if (btn) setTimeout(() => { btn.innerHTML = oldHtml; }, 1000);
    }
  }

  '''

text = text[:idx1] + clean_js + text[idx2:]
print("[OK] Replaced changeRootFolder and openRootInExplorer cleanly")

# 2. Fix /api/open_explorer in python
open_exp_start = 'elif self.path == "/api/open_explorer":'
idx_exp = text.find(open_exp_start)
if idx_exp != -1:
    idx_exp_end = text.find('elif self.path == "/api/chat":', idx_exp)
    if idx_exp_end != -1:
        new_open_exp = '''elif self.path == "/api/open_explorer":
            root = get_configured_docs_root()
            try:
                import os
                os.startfile(str(root))
                self.respond_json({"status": "ok", "opened": str(root)})
            except Exception as e:
                self.respond_json({"error": str(e)}, 500)

        '''
        text = text[:idx_exp] + new_open_exp + text[idx_exp_end:]
        print("[OK] Replaced /api/open_explorer with os.startfile")

# 3. Check Python compile
with open("scratch/server_check.py", "w", encoding="utf-8") as f:
    f.write(text)

py_compile.compile("scratch/server_check.py", doraise=True)
print("[OK] Python compile succeeded!")

# 4. Check JS syntax with node
s_start = text.find('<script>')
s_end = text.rfind('</script>')
script_body = text[s_start+8:s_end]
with open("scratch/verified_script.js", "w", encoding="utf-8") as f:
    f.write(script_body)

r = subprocess.run(["node", "--check", "scratch/verified_script.js"], capture_output=True, text=True, encoding="utf-8")
if r.returncode != 0:
    print("[ERROR] Node syntax check failed:\n", r.stderr)
    sys.exit(1)
print("[SUCCESS] Node --check passed with ZERO ERRORS!")

# 5. Overwrite server.py
with open(server_path, "w", encoding="utf-8") as f:
    f.write(text)
print("[SUCCESS] server.py saved successfully!")
