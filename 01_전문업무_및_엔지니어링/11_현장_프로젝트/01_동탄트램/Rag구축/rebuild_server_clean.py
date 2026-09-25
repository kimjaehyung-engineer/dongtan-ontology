# -*- coding: utf-8 -*-
import os, sys, re, subprocess

server_path = r'C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py'
bak_path = server_path + '.bak'

with open(bak_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Helper & Imports
helper_code = '''
META_INDEX_FILE = DOCS_DIR / "_metadata_index.json"

import io
try:
    import fitz
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

def slice_pdf_pages(file_path, page_indices):
    if HAS_FITZ:
        doc = fitz.open(file_path)
        new_doc = fitz.open()
        for idx in page_indices:
            if 0 <= idx < len(doc):
                new_doc.insert_pdf(doc, from_page=idx, to_page=idx)
        pdf_bytes = new_doc.tobytes()
        doc.close()
        new_doc.close()
        return pdf_bytes
    elif HAS_PYPDF:
        reader = pypdf.PdfReader(str(file_path))
        writer = pypdf.PdfWriter()
        for idx in page_indices:
            if 0 <= idx < len(reader.pages):
                writer.add_page(reader.pages[idx])
        out = io.BytesIO()
        writer.write(out)
        return out.getvalue()
    else:
        with open(file_path, "rb") as f:
            return f.read()

def get_smart_pdf_payload(file_path, query=""):
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    meta_map = {}
    if META_INDEX_FILE.exists():
        try:
            with open(META_INDEX_FILE, "r", encoding="utf-8") as f:
                meta_map = json.load(f)
        except Exception:
            pass

    doc_meta = meta_map.get(file_path.name)
    if not doc_meta and file_size_mb <= 15.0:
        with open(file_path, "rb") as f:
            return f.read(), "", False

    if not doc_meta and file_size_mb > 15.0:
        indices = list(range(15))
        return slice_pdf_pages(file_path, indices), f"[안내] 20MB 제한으로 전체 중 주요 15페이지만 로드되었습니다.", False

    sections = doc_meta.get("sections", [])
    query_lower = query.lower()
    is_overview = any(k in query_lower for k in ["목차", "구성", "전체", "어떻게 구성", "요약", "개요", "색인"])
    if is_overview and len(query.strip()) <= 35:
        overview_text = f"### [{doc_meta.get('document_name')}] 정밀 탐색 색인 정보\\n"
        overview_text += f"- 총 페이지: {doc_meta.get('total_pages')}p\\n"
        overview_text += f"- 개요: {doc_meta.get('description')}\\n\\n"
        overview_text += "| 섹션ID | 분류 | 제목 | 페이지 | 대상시설 |\\n"
        overview_text += "| :--- | :--- | :--- | :---: | :--- |\\n"
        for s in sections:
            fac = ", ".join(s.get("facility", []))
            overview_text += f"| {s['section_id']} | {s['task_id']} | {s['title']} | **p.{s['start_page']}~{s['end_page']}** | {fac} |\\n"
        return None, overview_text, True

    scored = []
    for s in sections:
        score = 0
        for fac in s.get("facility", []):
            if fac.lower() in query_lower:
                score += 5
        for kw in s.get("keywords", []):
            if kw.lower() in query_lower:
                score += 3
        if s.get("title", "").lower() in query_lower:
            score += 4
        if score > 0:
            scored.append((score, s))

    scored.sort(key=lambda x: x[0], reverse=True)
    target_pages = set()
    matched_sections = []
    if scored:
        for sc, s in scored[:2]:
            matched_sections.append(f"{s['title']} (p.{s['start_page']}~{s['end_page']})")
            for p in range(s["start_page"] - 1, s["end_page"]):
                target_pages.add(p)
    else:
        matched_sections.append("주요 대표 시작 페이지")
        rep_pages = [1, 7, 42, 93, 126, 129, 154, 170, 186, 192, 196, 198, 219]
        for rp in rep_pages:
            if rp - 1 < doc_meta.get("total_pages", 221):
                target_pages.add(rp - 1)

    sorted_pages = sorted(list(target_pages))
    if len(sorted_pages) > 30:
        sorted_pages = sorted_pages[:30]

    sliced_bytes = slice_pdf_pages(file_path, sorted_pages)
    info_str = f"[색인 라우팅] {', '.join(matched_sections)} 총 {len(sorted_pages)}페이지만 메모리에서 추출하여 분석합니다."
    return sliced_bytes, info_str, False
'''

anchor1 = 'DOCS_DIR.mkdir(exist_ok=True)'
text = text.replace(anchor1, anchor1 + '\n' + helper_code)

# 2. CSS for .doc-del-btn
del_css = '''
    .doc-del-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid #fecaca;
      background: #fff5f5;
      color: #ef4444;
      cursor: pointer;
      font-size: 11px;
      font-weight: 500;
      transition: all 0.2s;
      flex-shrink: 0;
      opacity: 0.7;
    }
    .doc-item:hover .doc-del-btn {
      opacity: 1.0;
    }
    .doc-del-btn:hover {
      background: #ef4444;
      color: #ffffff;
      border-color: #ef4444;
      transform: scale(1.05);
    }
'''
anchor_css = '.doc-item.active {'
text = text.replace(anchor_css, del_css + '\n    ' + anchor_css)

# 3. HTML file input multiple
text = text.replace(
    '<input type="file" id="fileInput" accept=".pdf" style="display:none;" onchange="uploadDoc()">',
    '<input type="file" id="fileInput" accept=".pdf" multiple style="display:none;" onchange="uploadDoc()">'
)

# 4. JS: fetchDocs rendering with [내리기] button
old_render = '''          item.innerHTML = `
            <div class="doc-icon">📄</div>
            <div class="doc-info">
              <div class="doc-name" title="${doc.name}">${doc.name}</div>
              <div class="doc-size">${doc.size_mb} MB</div>
            </div>
          `;'''

new_render = '''          item.innerHTML = `
            <div class="doc-icon">📄</div>
            <div class="doc-info">
              <div class="doc-name" title="${doc.name}">${doc.name}</div>
              <div class="doc-size">${doc.size_mb} MB</div>
            </div>
            <button class="doc-del-btn" title="보관함에서 내리기 (업로드본만 제거)" onclick="deleteDoc(event, '${doc.name}')">내리기</button>
          `;'''
text = text.replace(old_render, new_render)

# 5. JS: deleteDoc function + multiple uploadDoc function
old_select_doc = '    function selectDoc(name) {'
clean_js_funcs = '''    async function deleteDoc(event, name) {
      event.stopPropagation();
      const msg = `'${name}' 문서를 보관함에서 내리시겠습니까?\\n\\n※ 프로젝트 원본 파일은 안전하게 보존되며, 웹 화면(서버)에 업로드된 복사본 파일만 제거되어 디스크 용량이 확보됩니다.`;
      if (!confirm(msg)) {
        return;
      }
      try {
        const res = await fetch('/api/delete', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ document: name })
        });
        const data = await res.json();
        if (res.ok) {
          if (activeDoc === name) {
            activeDoc = null;
            const titleEl = document.getElementById('activeDocTitle');
            if (titleEl) titleEl.innerText = '문서를 선택하세요';
          }
          await fetchDocs();
        } else {
          alert('내리기 실패: ' + (data.error || '오류 발생'));
        }
      } catch(e) {
        alert('서버 요청 중 오류: ' + e);
      }
    }

    function selectDoc(name) {'''

text = text.replace(old_select_doc, clean_js_funcs)

old_upload_func = '''    async function uploadDoc() {
      const fileInput = document.getElementById('fileInput');
      if (!fileInput.files || fileInput.files.length === 0) return;
      const file = fileInput.files[0];
      const formData = new FormData();
      formData.append('file', file);
      try {
        const res = await fetch('/api/upload', {
          method: 'POST',
          body: formData
        });
        if (res.ok) {
          await fetchDocs();
          selectDoc(file.name);
        } else {
          alert('업로드 실패');
        }
      } catch (e) {
        alert('업로드 오류: ' + e);
      }
      fileInput.value = '';
    }'''

new_upload_func = '''    async function uploadDoc() {
      const fileInput = document.getElementById('fileInput');
      if (!fileInput.files || fileInput.files.length === 0) return;
      const files = Array.from(fileInput.files);
      const total = files.length;

      const uploadBtn = document.querySelector('.upload-btn');
      const originalText = uploadBtn ? uploadBtn.innerHTML : '➕ 새 시방서/보고서 PDF 추가';

      let successCount = 0;
      let lastUploadedName = '';

      for (let i = 0; i < total; i++) {
        const file = files[i];
        if (uploadBtn) {
          uploadBtn.innerHTML = `⏳ 업로드 중 (${i+1}/${total}): ${file.name.slice(0, 12)}...`;
          uploadBtn.style.opacity = '0.7';
          uploadBtn.style.pointerEvents = 'none';
        }

        const formData = new FormData();
        formData.append('file', file);
        try {
          const res = await fetch('/api/upload', {
            method: 'POST',
            body: formData
          });
          if (res.ok) {
            successCount++;
            lastUploadedName = file.name;
          }
        } catch (e) {
          console.error('업로드 실패:', file.name, e);
        }
      }

      if (uploadBtn) {
        uploadBtn.innerHTML = originalText;
        uploadBtn.style.opacity = '1.0';
        uploadBtn.style.pointerEvents = 'auto';
      }

      fileInput.value = '';
      await fetchDocs();
      if (lastUploadedName) {
        selectDoc(lastUploadedName);
      }
      if (total > 1) {
        alert(`선택한 ${total}개 파일 중 ${successCount}개 파일이 보관함에 추가되었습니다!`);
      }
    }'''

text = text.replace(old_upload_func, new_upload_func)

# 6. BE: Add /api/delete in do_POST
old_upload_be = '''                self.respond_json({"status": "uploaded"})
            else:
                self.send_response(400)
                self.end_headers()'''

new_upload_be = '''                self.respond_json({"status": "uploaded"})
            else:
                self.send_response(400)
                self.end_headers()

        elif self.path == "/api/delete":
            content_len = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(content_len).decode("utf-8"))
            doc_name = payload.get("document")
            if not doc_name:
                self.respond_json({"error": "문서명이 지정되지 않았습니다."}, 400)
                return

            file_path = DOCS_DIR / doc_name
            if file_path.exists():
                try:
                    file_path.unlink()
                    meta_file = DOCS_DIR / "_metadata_index.json"
                    if meta_file.exists():
                        try:
                            with open(meta_file, "r", encoding="utf-8") as f:
                                meta_data = json.load(f)
                            if doc_name in meta_data:
                                del meta_data[doc_name]
                                with open(meta_file, "w", encoding="utf-8") as f:
                                    json.dump(meta_data, f, ensure_ascii=False, indent=2)
                        except Exception:
                            pass
                    self.respond_json({"status": "deleted", "message": f"{doc_name} 삭제 완료"})
                except Exception as e:
                    self.respond_json({"error": f"파일 삭제 실패: {str(e)}"}, 500)
            else:
                self.respond_json({"error": "해당 문서가 존재하지 않습니다."}, 404)'''

text = text.replace(old_upload_be, new_upload_be)

# 7. BE: Patch chat and graph to use get_smart_pdf_payload
old_open_pdf = '''            try:
                with open(file_path, "rb") as f:
                    pdf_bytes = f.read()
                pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")'''

new_chat_pdf = '''            try:
                pdf_bytes, info_msg, is_meta_only = get_smart_pdf_payload(file_path, query)
                if is_meta_only:
                    self.respond_json({"reply": info_msg})
                    return
                pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")'''

new_graph_pdf = '''            try:
                pdf_bytes, info_msg, _ = get_smart_pdf_payload(file_path, "지반조사 시추공 지층 가시설 구조물 기초 계측")
                pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")'''

text = text.replace(old_open_pdf, new_chat_pdf, 1)
text = text.replace(old_open_pdf, new_graph_pdf, 1)

# Write clean server.py
with open(server_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS: Clean rebuild completed!")
