# -*- coding: utf-8 -*-
import sys
import os
import re
import py_compile
import subprocess
from pathlib import Path

server_path = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py")
with open(server_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# 1. Fix /api/open_explorer in Python
open_explorer_re = r'elif self\.path == "/api/open_explorer":[\s\S]*?self\.respond_json\(\{"error": str\(e\)\}, 500\)'
new_explorer_block = '''elif self.path == "/api/open_explorer":
            root = get_configured_docs_root()
            try:
                import os
                os.startfile(str(root))
                self.respond_json({"status": "ok", "opened": str(root)})
            except Exception as e:
                self.respond_json({"error": str(e)}, 500)'''

code = re.sub(open_explorer_re, new_explorer_block, code)
print("[OK] Updated /api/open_explorer to use os.startfile")

# 2. Fix the JS prompt and openRootInExplorer using raw string to preserve literal \\n
old_js_block_re = r'async function changeRootFolder\(\)[\s\S]*?async function openRootInExplorer\([\s\S]*?alert\(\'요청 실패: \' \+ e\.message\);\s*\}\s*\}'

new_js_block = r'''async function changeRootFolder() {
    const currentPath = window.docsRootPath || '';
    const newPath = prompt("참조할 상위 폴더(루트 경로)를 입력하세요:\n(해당 폴더 아래의 모든 하위 폴더와 파일이 계층 구조 그대로 자동 연동됩니다)", currentPath);
    if (!newPath || !newPath.trim() || newPath.trim() === currentPath) return;

    try {
      const res = await fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ docs_root_path: newPath.trim() })
      });
      const data = await res.json();
      if (data.status === 'ok') {
        alert("상위 폴더가 설정되었습니다:\n" + data.docs_root_path + "\n\n하위 모든 폴더 및 문서를 다시 스캔합니다.");
        await fetchDocs();
      } else {
        alert("폴더 설정 실패: " + (data.error || '폴더가 존재하지 않거나 접근할 수 없습니다.'));
      }
    } catch(e) {
      alert("오류 발생: " + e.message);
    }
  }

  async function openRootInExplorer(event) {
    const btn = event && event.currentTarget ? event.currentTarget : null;
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
  }'''

code = re.sub(old_js_block_re, new_js_block, code)
print("[OK] Updated changeRootFolder and openRootInExplorer with raw string")

# 3. Update onclick="openRootInExplorer()" to onclick="openRootInExplorer(event)"
code = code.replace('onclick="openRootInExplorer()"', 'onclick="openRootInExplorer(event)"')

# Test Python compile
with open("scratch/server_fix_test.py", "w", encoding="utf-8") as f:
    f.write(code)

py_compile.compile("scratch/server_fix_test.py", doraise=True)
print("[OK] Python compile succeeded!")

# Extract and test JS with node
idx1 = code.find('<script>')
idx2 = code.rfind('</script>')
script_content = code[idx1+8:idx2]
with open("scratch/test_fixed_script.js", "w", encoding="utf-8") as f:
    f.write(script_content)

r = subprocess.run(["node", "--check", "scratch/test_fixed_script.js"], capture_output=True, text=True, encoding="utf-8")
if r.returncode != 0:
    print("[ERROR] Node check failed:", r.stderr)
    sys.exit(1)
print("[SUCCESS] Node --check on script passed with ZERO errors!")

# Overwrite server.py
with open(server_path, "w", encoding="utf-8") as f:
    f.write(code)
print("[SUCCESS] server.py overwritten successfully!")
