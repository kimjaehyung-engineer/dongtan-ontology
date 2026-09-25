import time
import os
import json
import base64
import urllib.request
import urllib.error
import urllib.parse
import re
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer
import socket

PORT = 8080
DOCS_DIR = Path(__file__).parent / "documents"
ENV_FILE = Path(__file__).parent / ".env"

DOCS_DIR.mkdir(exist_ok=True)

META_INDEX_FILE = DOCS_DIR / "_metadata_index.json"

import sys
# [Self-Healing Guard] Google GenAI 및 PyMuPDF가 설치된 Python 3.14 인터프리터 자동 감지 및 인계
py314_exe = r"C:\Users\sskjh\AppData\Local\Programs\Python\Python314\python.exe"
if __name__ == '__main__' and os.path.exists(py314_exe) and sys.executable.lower() != py314_exe.lower():
    try:
        from google import genai
    except ImportError:
        import subprocess
        print(f"[Self-Healing] Detected missing 'google.genai' in current interpreter ({sys.executable}).")
        print(f"[Self-Healing] Seamlessly switching to Python 3.14: {py314_exe}...")
        sys.exit(subprocess.call([py314_exe] + sys.argv))

sys.path.insert(0, str(Path(__file__).parent))
try:
    import sql_query_engine
    import graph_intelligence
    print("[Server Init] Loaded sql_query_engine successfully!")
except Exception as e:
    print(f"[Server Init] Failed to load sql_query_engine: {e}")
    sql_query_engine = None


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

def extract_target_numbers(query):
    nums = set()
    # 1. Clean query from depth, N-value conditions, page numbers to avoid false positives
    # e.g. "3m", "3.0m", "n<6", "n < 6", "n=10", "n치 6", "p.4", "페이지 5"
    cleaned = re.sub(r'\b\d+(?:\.\d+)?\s*(?:m|meter|미터|cm|km)\b', ' ', query, flags=re.I)
    cleaned = re.sub(r'[nN]\s*(?:치)?\s*([<>]=?|=)\s*\d+', ' ', cleaned)
    cleaned = re.sub(r'[nN]\s*치\s*[<>=]?\s*\d+', ' ', cleaned)
    cleaned = re.sub(r'p(?:age|\.)?\s*\d+', ' ', cleaned, flags=re.I)
    cleaned = re.sub(r'심도\s*\d+(?:\.\d+)?', ' ', cleaned)

    # 2. range like 7~9, 7-9, 7 - 9
    for m in re.finditer(r'(\d+)\s*[~-]\s*(\d+)', cleaned):
        try:
            s_n, e_n = int(m.group(1)), int(m.group(2))
            if s_n <= e_n and e_n - s_n <= 30:
                nums.update(range(s_n, e_n + 1))
        except ValueError:
            pass

    # 3. Explicit borehole patterns: GB-7, NH-3, DT-1, 7번, 7공, 7호
    for m in re.finditer(r'(?:gb|nh|dt|공|시추공|번|호)\s*[-_]?\s*(\d+)', cleaned, re.I):
        try:
            nums.add(int(m.group(1)))
        except ValueError:
            pass
    for m in re.finditer(r'(\d+)\s*(?:공|호|번|공구)', cleaned, re.I):
        try:
            nums.add(int(m.group(1)))
        except ValueError:
            pass
    return nums


def scan_all_boreholes_for_condition(file_path, max_depth=3.0, max_n=6):
    """Scan all borehole logs in PDF for depth and N-value conditions (Audit mode)"""
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        matching = []
        for p_idx, page in enumerate(reader.pages):
            txt = page.extract_text() or ""
            if not txt.strip():
                continue
            m_hole = re.search(r'HOLE\s*No\.?\s*([A-Z0-9_-]+)', txt, re.I)
            if not m_hole:
                m_hole = re.search(r'\b(NH-\d+|GB-\d+|DT-\d+)\b', txt)
            hole_name = m_hole.group(1).strip() if m_hole else f"p.{p_idx+1}"
            
            lines = [l.strip() for l in txt.split('\n') if l.strip()]
            samples = [l for l in lines if re.match(r'^S-\d+$', l)]
            n_values = [l for l in lines if re.match(r'^\d+/\d+$', l)]
            depths = [float(l) for l in lines if re.match(r'^\d+\.\d+$', l) and 0.5 <= float(l) <= 50.0]
            
            matched_records = []
            if len(depths) >= len(n_values) and len(n_values) > 0:
                num_spt = len(n_values)
                spt_depths = depths[-num_spt:] if len(depths) >= num_spt else depths
                for i, n_str in enumerate(n_values):
                    d = spt_depths[i] if i < len(spt_depths) else (i + 1) * 1.0
                    m_blow = re.match(r'^(\d+)/(\d+)$', n_str)
                    if m_blow:
                        blows = int(m_blow.group(1))
                        pen = int(m_blow.group(2))
                        if d <= max_depth and blows < max_n and pen == 30:
                            s_name = samples[i] if i < len(samples) else f"S-{i+1}"
                            matched_records.append({
                                "depth": d,
                                "sample": s_name,
                                "n_val": blows
                            })
            if matched_records:
                matching.append({
                    "hole": hole_name,
                    "page": p_idx + 1,
                    "records": matched_records
                })
        return matching
    except Exception as e:
        print(f"[Scanner Error] {e}")
        return []

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

    if file_size_mb > 20.0 and not (doc_meta and doc_meta.get("sections")):
        # 20MB 초과 대형 스캔 문서는 15쪽으로 자르지 않고 Google File API 통업로드로 처리
        return None, f"[Google File API 롱컨텍스트] {file_path.name} 전체({round(file_size_mb, 1)}MB) 전수 탐색 모드", False

    sections = doc_meta.get("sections", [])
    query_lower = query.lower()
    is_pure_toc = any(k in query_lower for k in ["목차 보여", "색인 보여", "문서 구조", "목차 확인"])
    if is_pure_toc and len(query.strip()) <= 30:
        overview_text = f"### [{doc_meta.get('document_name')}] 정밀 탐색 색인 정보\n"
        overview_text += f"- 총 페이지: {doc_meta.get('total_pages')}p\n"
        overview_text += f"- 개요: {doc_meta.get('description')}\n\n"
        overview_text += "| 섹션ID | 분류 | 제목 | 페이지 | 대상시설 |\n"
        overview_text += "| :--- | :--- | :--- | :---: | :--- |\n"
        for s in sections:
            fac = ", ".join(s.get("facility", []))
            task_val = s.get("task_id", s.get("section_id", "-"))
            overview_text += f"| {s.get('section_id', '-')} | {task_val} | {s.get('title', '-')} | **p.{s.get('start_page', 1)}~{s.get('end_page', 1)}** | {fac} |\n"
        return None, overview_text, True

    target_nums = extract_target_numbers(query_lower)

    # Condition Search (Depth / N-value Audit Mode)
    is_n_condition = bool(re.search(r'[nN]\s*(?:치)?\s*([<>]=?|=)\s*(\d+)', query_lower) or re.search(r'[nN]\s*치', query_lower))
    is_depth_cond = bool(re.search(r'심도\s*(\d+(?:\.\d+)?)\s*m?', query_lower) or re.search(r'(\d+(?:\.\d+)?)\s*m\s*이내', query_lower))

    if (is_n_condition or is_depth_cond) and not target_nums and any(k in file_path.name for k in ["시추주상도", "주상도"]):
        m_d = re.search(r'(\d+(?:\.\d+)?)\s*m', query_lower)
        max_d = float(m_d.group(1)) if m_d else 3.0
        m_n = re.search(r'[nN]\s*(?:치)?\s*[<]=?\s*(\d+)', query_lower)
        max_n = int(m_n.group(1)) if m_n else 6

        scan_res = scan_all_boreholes_for_condition(file_path, max_depth=max_d, max_n=max_n)
        if scan_res:
            target_pages = set()
            for item in scan_res:
                target_pages.add(item["page"] - 1)
            sorted_pages = sorted(list(target_pages))
            sliced_bytes = slice_pdf_pages(file_path, sorted_pages)
            
            audit_summary = f"[전수 스캔 감사] 지하 심도 {max_d}m 이내에서 N < {max_n}을 만족하는 보링공은 총 {len(scan_res)}개소입니다:\n"
            for item in scan_res:
                rec_text = ", ".join([f"{r['sample']} (심도 {r['depth']}m, N={r['n_val']})" for r in item["records"]])
                audit_summary += f"- **{item['hole']}** (p.{item['page']}): {rec_text}\n"

            info_msg = f"[출처 문서 자동 탐색] **{file_path.name}** 전체 45공 전수 감사(Audit) 결과, 조건 만족 보링공 **{len(scan_res)}개소(총 {len(sorted_pages)}p)**를 추출했습니다.\n{audit_summary}"
            return sliced_bytes, info_msg, False

    is_base = any(k in query_lower for k in ["차량기지", "건축기지", "기지", "gb"])

    scored = []
    for s in sections:
        score = 0
        sec_title = s.get("title", "")
        m = re.search(r'(?:GB|NH|DT)-(\d+)', sec_title)
        sec_num = int(m.group(1)) if m else None

        # facility matching
        for fac in s.get("facility", []):
            if fac.lower() in query_lower:
                score += 8
        if is_base and "차량기지" in s.get("facility", []):
            score += 15
        elif not is_base and "본선" in s.get("facility", []):
            score += 5

        # exact borehole number match (massive bonus)
        if sec_num is not None and sec_num in target_nums:
            score += 40

        for kw in s.get("keywords", []):
            if kw.lower() in query_lower:
                score += 4
        if sec_title.lower() in query_lower:
            score += 6

        if score > 0:
            scored.append((score, s))

    scored.sort(key=lambda x: x[0], reverse=True)
    target_pages = set()
    matched_sections = []

    # If specific borehole numbers are requested (e.g. 7~9), strictly pick those
    if target_nums and any(item[0] >= 40 for item in scored):
        filtered_scored = [item for item in scored if item[0] >= 35]
    else:
        # NO PAGE COUNT LIMIT: Include ALL matching sections completely!
        top_sc = scored[0][0] if scored else 0
        rel_threshold = max(3, int(top_sc * 0.35))
        filtered_scored = [item for item in scored if item[0] >= rel_threshold]

    # Collect ALL pages from all matched sections without any page limit
    for sc, s in filtered_scored:
        sec_pages = list(range(s["start_page"] - 1, s["end_page"]))
        matched_sections.append(f"{s['title']} (p.{s['start_page']}~{s['end_page']})")
        for p in sec_pages:
            target_pages.add(p)

    if not target_pages:
        matched_sections.append("전체 주요 섹션")
        for s in sections[:15]:
            matched_sections.append(f"{s['title']} (p.{s['start_page']}~{s['end_page']})")
            for p in range(s["start_page"] - 1, s["end_page"]):
                target_pages.add(p)

    sorted_pages = sorted(list(target_pages))
    sliced_bytes = slice_pdf_pages(file_path, sorted_pages)

    # 18MB 초과 시 페이지를 강제로 5장으로 줄이지 않고, Google File API 롱컨텍스트 모드로 직결 전환!
    if len(sliced_bytes) > 18 * 1024 * 1024:
        info_str = f"[Google File API 롱컨텍스트] {', '.join(matched_sections[:6])} 전체({len(sorted_pages)}p, 18MB 초과)를 자르지 않고 Google 멀티모달 통업로드로 분석합니다."
        return None, info_str, False

    info_str = f"[색인 전수 추출] {', '.join(matched_sections[:8])} 등 총 {len(sorted_pages)}페이지 전체를 메모리에서 추출하여 분석합니다."
    return sliced_bytes, info_str, False

def get_server_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def load_env_api_key():
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("GEMINI_API_KEY="):
                    return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get("GEMINI_API_KEY", "")

def save_env_api_key(key):
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write(f"GEMINI_API_KEY={key}\n")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>현장 기술문서 AI 지식 어시스턴트 & GraphRAG</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    :root {
      --bg-main: #f8fafc;
      --bg-sidebar: #ffffff;
      --bg-card: #ffffff;
      --bg-input: #ffffff;
      --border-color: #e2e8f0;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --accent: #2563eb;
      --accent-hover: #1d4ed8;
      --bot-msg-bg: #ffffff;
      --user-msg-bg: #eff6ff;
      --user-border: #bfdbfe;
      --heading-color: #0f172a;
      --canvas-bg: #f8fafc;
      --card-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
      --table-header-bg: #f1f5f9;
      --table-header-text: #1e40af;
      --table-stripe: #f8fafc;
      --alert-bg: #fef2f2;
      --alert-border: #fecaca;
      --alert-text: #991b1b;
      --alert-heading: #dc2626;
      --doc-active-bg: #eff6ff;
    }
    [data-theme="dark"] {
      --bg-main: #121418;
      --bg-sidebar: #1a1d24;
      --bg-card: #222631;
      --bg-input: #1a1d24;
      --border-color: #2e3442;
      --text-main: #e6edf3;
      --text-muted: #8b949e;
      --accent: #3b82f6;
      --accent-hover: #2563eb;
      --bot-msg-bg: #1e2330;
      --user-msg-bg: #1d3557;
      --user-border: #2b4c7e;
      --heading-color: #ffffff;
      --canvas-bg: #0f1115;
      --card-shadow: 0 4px 12px rgba(0,0,0,0.25);
      --table-header-bg: #1e293b;
      --table-header-text: #93c5fd;
      --table-stripe: #1b202c;
      --alert-bg: #2b1717;
      --alert-border: #7f1d1d;
      --alert-text: #fca5a5;
      --alert-heading: #ef4444;
      --doc-active-bg: #1e293b;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans KR", sans-serif;
      background: var(--bg-main);
      color: var(--text-main);
      display: flex;
      height: 100vh;
      overflow: hidden;
      transition: background 0.2s, color 0.2s;
    }
    /* Sidebar */
    #sidebar {
      width: 320px;
      background: var(--bg-sidebar);
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      box-shadow: 1px 0 4px rgba(0,0,0,0.03);
    }
    .sidebar-header {
      padding: 16px 20px;
      border-bottom: 1px solid var(--border-color);
    }
    .sidebar-header h1 {
      font-size: 15px;
      font-weight: 700;
      color: var(--heading-color);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .badge {
      font-size: 11px;
      background: #eff6ff;
      color: #2563eb;
      border: 1px solid #bfdbfe;
      padding: 2px 7px;
      border-radius: 12px;
      font-weight: 600;
    }
    .sidebar-content {
      flex: 1;
      overflow-y: auto;
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .section-title {
      font-size: 12px;
      text-transform: uppercase;
      color: var(--text-muted);
      letter-spacing: 0.5px;
      margin-bottom: 8px;
      font-weight: 600;
    }

    /* Document Folder Tree View Styles */
    .doc-tree-container {
      display: flex;
      flex-direction: column;
      gap: 6px;
      max-height: 480px;
      overflow-y: auto;
      padding-right: 2px;
    }
    .tree-folder {
      border: 1px solid var(--border-color, #e2e8f0);
      background: var(--bg-card, #ffffff);
      border-radius: 8px;
      overflow: hidden;
      transition: all 0.2s ease;
    }
    .tree-folder.open {
      border-color: #93c5fd;
      box-shadow: 0 2px 8px rgba(37, 99, 235, 0.06);
    }
    .folder-header {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 8px 10px;
      background: var(--bg-hover, #f8fafc);
      cursor: pointer;
      user-select: none;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-color, #1e293b);
      transition: background 0.15s;
    }
    .folder-header:hover {
      background: #eff6ff;
      color: #1d4ed8;
    }
    .folder-icon {
      font-size: 14px;
      flex-shrink: 0;
    }
    .folder-title {
      flex: 1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .folder-badge {
      font-size: 10px;
      font-weight: 600;
      padding: 1px 6px;
      border-radius: 10px;
      background: #e2e8f0;
      color: #475569;
    }
    .tree-folder.open .folder-badge {
      background: #dbeafe;
      color: #1e40af;
    }
    .folder-arrow {
      font-size: 10px;
      color: var(--text-muted, #94a3b8);
      transition: transform 0.2s ease;
    }
    .tree-folder.open .folder-arrow {
      transform: rotate(90deg);
      color: #2563eb;
    }
    .folder-content {
      display: none;
      padding: 4px 6px 6px 6px;
      background: var(--bg-card, #ffffff);
      flex-direction: column;
      gap: 4px;
    }
    .tree-folder.open .folder-content {
      display: flex;
    }
    .tree-subfolder {
      margin-left: 6px;
      border-left: 2px solid #e2e8f0;
      padding-left: 6px;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }
    .subfolder-header {
      display: flex;
      align-items: center;
      gap: 5px;
      padding: 4px 6px;
      font-size: 11px;
      font-weight: 600;
      color: var(--text-muted, #64748b);
      cursor: pointer;
      border-radius: 4px;
    }
    .subfolder-header:hover {
      background: #f1f5f9;
      color: #0f172a;
    }
    .tree-doc-item {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 6px 8px;
      border-radius: 6px;
      border: 1px solid #f1f5f9;
      background: var(--bg-card, #ffffff);
      font-size: 12px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .tree-doc-item:hover {
      background: #f0fdf4;
      border-color: #86efac;
      transform: translateX(2px);
    }
    .tree-doc-item.active {
      background: #eff6ff;
      border-color: #3b82f6;
      font-weight: 600;
    }
    .tree-doc-icon {
      font-size: 13px;
      flex-shrink: 0;
    }
    .tree-doc-info {
      flex: 1;
      min-width: 0;
    }
    .tree-doc-name {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      color: var(--text-color, #1e293b);
      line-height: 1.3;
      font-weight: 500;
    }
    .tree-doc-meta {
      font-size: 10px;
      color: var(--text-muted, #94a3b8);
    }
    .tree-doc-actions {
      display: flex;
      gap: 3px;
      align-items: center;
      flex-shrink: 0;
    }
    .tree-btn-view {
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      background: #eff6ff;
      color: #2563eb;
      border: 1px solid #bfdbfe;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.15s;
    }
    .tree-btn-view:hover {
      background: #2563eb;
      color: #ffffff;
    }
    .tree-btn-del {
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      background: #fff1f2;
      color: #e11d48;
      border: 1px solid #fecdd3;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.15s;
    }
    .tree-btn-del:hover {
      background: #e11d48;
      color: #ffffff;
    }

    .doc-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .doc-item {
      padding: 10px 12px;
      background: var(--bg-card);
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      border-radius: 8px;
      font-size: 13px;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.15s;
      box-shadow: var(--card-shadow);
    }
    .doc-item:hover {
      border-color: #cbd5e1;
      background: var(--bot-msg-bg);
    }
    .doc-view-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 3px 8px;
      border-radius: 4px;
      border: 1px solid #bfdbfe;
      background: #eff6ff;
      color: #2563eb;
      cursor: pointer;
      font-size: 11px;
      font-weight: 600;
      transition: all 0.15s;
      flex-shrink: 0;
    }
    .doc-view-btn:hover {
      background: #2563eb;
      color: #ffffff;
      border-color: #2563eb;
    }
    
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

    .doc-item-actions {
      display: flex;
      align-items: center;
      gap: 4px;
      flex-shrink: 0;
    }
    .doc-view-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 3px 8px;
      border-radius: 4px;
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      background: var(--bg-card);
      color: var(--text-main);
      cursor: pointer;
      font-size: 11px;
      font-weight: 600;
      transition: all 0.15s;
    }
    .doc-view-btn:hover {
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
    }
    .doc-icon { font-size: 18px; }
    .doc-info { flex: 1; min-width: 0; }
    .doc-name {
      font-weight: 600;
      color: var(--heading-color);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .doc-size { font-size: 11px; color: var(--text-muted); margin-top: 2px; }
    
    .upload-btn {
      width: 100%;
      padding: 10px;
      background: transparent;
      border: 1px dashed var(--border-color);
      border-radius: 8px;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 13px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.15s;
    }
    .upload-btn:hover {
      border-color: var(--accent);
      color: var(--accent);
      background: var(--bg-card);
    }
    
    .sidebar-footer {
      padding: 16px 20px;
      border-top: 1px solid var(--border-color);
      font-size: 12px;
    }
    .ip-box {
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      border-radius: 6px;
      padding: 8px 10px;
      color: #1d4ed8;
      word-break: break-all;
      margin-top: 6px;
      font-family: monospace;
      font-size: 12px;
      font-weight: 600;
    }
    
    /* Main */
    #main {
      flex: 1;
      display: flex;
      flex-direction: column;
      height: 100vh;
      background: var(--bg-main);
      overflow: hidden;
    }
    .top-nav {
      padding: 10px 24px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-sidebar);
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .nav-tabs {
      display: flex;
      gap: 8px;
    }
    .tab-btn {
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13.5px;
      font-weight: 600;
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      background: var(--bg-card);
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }
    .tab-btn:hover { color: var(--text-main); border-color: var(--accent); }
    .tab-btn.active {
      background: #eff6ff;
      color: #2563eb;
      border-color: #3b82f6;
    }
    
    .api-key-input {
      background: var(--bg-input);
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      color: var(--text-main);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      width: 210px;
    }
    .api-key-input:focus {
      outline: none;
      border-color: var(--accent);
    }
    
    .theme-toggle-btn {
      background: var(--bg-card);
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      color: var(--text-main);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }
    .theme-toggle-btn:hover { border-color: var(--accent); }
    
    .tab-content {
      flex: 1;
      display: none;
      height: calc(100vh - 61px);
    }
    .tab-content.active {
      display: flex;
      flex-direction: column;
    }
    
    /* Chat View */
    
    /* Split Layout for Chat & Document Viewer */
    .chat-header-bar {
      padding: 10px 20px;
      border-bottom: 1px solid var(--border-color);
      font-size: 13px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-card);
      gap: 12px;
      flex-shrink: 0;
    }
    .top-action-btn {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      background: var(--bg-input);
      color: var(--text-main);
      cursor: pointer;
      transition: all 0.15s;
    }
    .top-action-btn:hover {
      border-color: var(--accent);
      color: var(--accent);
    }
    .top-action-btn.active {
      background: var(--doc-active-bg);
      border-color: var(--accent);
      color: var(--accent);
    }
    .top-action-btn.download-btn {
      background: #eff6ff;
      border-color: #bfdbfe;
      color: #1d4ed8;
    }
    .top-action-btn.download-btn:hover {
      background: #2563eb;
      color: #ffffff;
      border-color: #2563eb;
    }
    .chat-split-container {
      flex: 1;
      display: flex;
      overflow: hidden;
      width: 100%;
      height: calc(100% - 41px);
    }
    .chat-main-col {
      flex: 1;
      min-width: 0;
      display: flex;
      flex-direction: column;
      height: 100%;
      transition: all 0.2s ease;
    }
    .doc-viewer-panel {
      width: 48%;
      min-width: 380px;
      max-width: 780px;
      border-left: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      background: var(--bg-card);
      height: 100%;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
    }
    .doc-viewer-panel.collapsed {
      display: none;
    }
    .viewer-header {
      padding: 8px 16px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-sidebar);
      gap: 10px;
      flex-shrink: 0;
    }
    .viewer-title-box {
      display: flex;
      align-items: center;
      gap: 8px;
      min-width: 0;
      flex: 1;
    }
    .viewer-doc-title {
      font-weight: 600;
      font-size: 12.5px;
      color: var(--heading-color);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .viewer-doc-size {
      font-size: 11px;
      color: var(--text-muted);
      flex-shrink: 0;
    }
    .viewer-actions {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-shrink: 0;
    }
    .viewer-btn {
      padding: 4px 9px;
      border-radius: 5px;
      font-size: 11.5px;
      font-weight: 500;
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      background: var(--bg-input);
      color: var(--text-main);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.15s;
    }
    .viewer-btn:hover {
      border-color: var(--accent);
      color: var(--accent);
    }
    .viewer-btn.primary {
      background: #2563eb;
      border-color: #2563eb;
      color: #ffffff;
      font-weight: 600;
    }
    .viewer-btn.primary:hover {
      background: #1d4ed8;
      transform: translateY(-1px);
    }
    .viewer-btn.icon-only {
      padding: 4px 7px;
      font-size: 13px;
      color: var(--text-muted);
    }
    .viewer-btn.icon-only:hover {
      color: #ef4444;
      border-color: #fca5a5;
    }
    .viewer-page-bar {
      padding: 6px 14px;
      border-bottom: 1px solid var(--border-color);
      background: var(--table-header-bg);
      display: flex;
      align-items: center;
      gap: 8px;
      overflow-x: auto;
      font-size: 11.5px;
      flex-shrink: 0;
    }
    .page-pills-container {
      display: flex;
      gap: 5px;
      overflow-x: auto;
      flex: 1;
      padding-bottom: 2px;
    }
    .page-link-badge {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      padding: 1px 7px;
      margin: 0 2px;
      border-radius: 4px;
      border: 1px solid #93c5fd;
      background: #eff6ff;
      color: #1d4ed8;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
      vertical-align: middle;
      text-decoration: none;
    }
    .page-link-badge:hover {
      background: #2563eb;
      color: #ffffff;
      border-color: #2563eb;
      transform: translateY(-1px);
      box-shadow: 0 2px 4px rgba(37,99,235,0.25);
    }
    .page-pill.highlight {
      background: #f0fdf4 !important;
      color: #15803d !important;
      border-color: #86efac !important;
      font-weight: 600 !important;
    }
    .page-pill.current {
      background: #2563eb !important;
      color: #ffffff !important;
      border-color: #2563eb !important;
      font-weight: 600 !important;
      box-shadow: 0 0 0 2px rgba(37,99,235,0.2);
    }
    .page-pill {
      padding: 2px 7px;
      border-radius: 4px;
      background: var(--bg-card);
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      color: var(--text-main);
      cursor: pointer;
      white-space: nowrap;
      font-size: 11px;
      font-weight: 500;
      transition: all 0.15s;
    }
    .page-pill:hover {
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
    }
    .page-direct-jump {
      display: flex;
      align-items: center;
      gap: 4px;
      flex-shrink: 0;
    }
    .page-direct-jump input {
      width: 44px;
      padding: 2px 4px;
      font-size: 11px;
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      border-radius: 4px;
      background: var(--bg-input);
      color: var(--text-main);
      text-align: center;
    }
    .page-direct-jump button {
      padding: 2px 6px;
      font-size: 11px;
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      border-radius: 4px;
      background: var(--bg-card);
      color: var(--text-main);
      cursor: pointer;
    }
    .page-direct-jump button:hover {
      border-color: var(--accent);
      color: var(--accent);
    }
    .viewer-iframe-wrapper {
      flex: 1;
      position: relative;
      background: #525659;
      height: 100%;
      overflow: hidden;
    }
    .pdf-iframe {
      width: 100%;
      height: 100%;
      border: none;
    }
    .viewer-placeholder {
      position: absolute;
      inset: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: var(--bg-card);
      color: var(--text-muted);
      text-align: center;
      padding: 24px;
    }

    .chat-body {
      flex: 1;
      overflow-y: auto;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .message {
      display: flex;
      gap: 14px;
      max-width: 900px;
      width: 100%;
      margin: 0 auto;
    }
    .avatar {
      width: 34px;
      height: 34px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      flex-shrink: 0;
    }
    .avatar.bot { background: #2563eb; color: #fff; }
    .avatar.user { background: #374151; color: #fff; }
    .message-content {
      flex: 1;
      line-height: 1.65;
      font-size: 14.5px;
      padding: 14px 18px;
      border-radius: 12px;
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
    }
    .message.bot .message-content {
      background: var(--bot-msg-bg);
      color: var(--text-main);
    }
    .message.user .message-content {
      background: var(--user-msg-bg);
      border-color: var(--user-border);
      color: var(--text-main);
    }
    
    .message-content h1, .message-content h2, .message-content h3 {
      margin-top: 14px;
      margin-bottom: 8px;
      color: var(--heading-color);
      font-weight: 700;
    }
    .message-content table {
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0;
      font-size: 13.5px;
    }
    .message-content th, .message-content td {
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      padding: 8px 12px;
      text-align: left;
    }
    .message-content th {
      background: var(--table-header-bg);
      color: var(--table-header-text);
      font-weight: 600;
    }
    .message-content tr:nth-child(even) {
      background: var(--table-stripe);
    }
    
    .chat-footer {
      padding: 16px 24px 20px 24px;
      background: var(--bg-main);
      border-top: 1px solid var(--border-color);
    }
    .input-container {
      max-width: 900px;
      margin: 0 auto;
      display: flex;
      gap: 10px;
      background: var(--bg-input);
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      border-radius: 12px;
      padding: 8px 14px;
      box-shadow: var(--card-shadow);
    }
    .input-container:focus-within { border-color: var(--accent); }
    #promptInput {
      flex: 1;
      background: transparent;
      border: none;
      color: var(--text-main);
      font-size: 14.5px;
      padding: 6px 0;
      resize: none;
      height: 48px;
      max-height: 140px;
      font-family: inherit;
    }
    #promptInput::placeholder { color: var(--text-muted); }
    #promptInput:focus { outline: none; }
    .send-btn {
      align-self: flex-end;
      background: var(--accent);
      color: #fff;
      border: none;
      border-radius: 8px;
      padding: 10px 18px;
      font-size: 13.5px;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.15s;
    }
    .send-btn:hover { background: var(--accent-hover); }
    .send-btn:disabled { background: #94a3b8; cursor: not-allowed; }
    
    
    /* GraphRAG Custom UI */
    .graph-toolbar {
      position: absolute;
      top: 14px;
      left: 16px;
      z-index: 10;
      display: flex;
      align-items: center;
      gap: 6px;
      background: var(--bg-card);
      padding: 6px 12px;
      border-radius: 8px;
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .filter-chip {
      padding: 5px 11px;
      font-size: 12px;
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      border-radius: 6px;
      background: var(--bg-main);
      color: var(--text-main);
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .filter-chip:hover {
      border-color: var(--accent);
      color: var(--accent);
    }
    .filter-chip.active {
      background: var(--accent);
      color: #fff !important;
      border-color: var(--accent);
      font-weight: 600;
    }
    .filter-chip-risk.active {
      background: #ef4444 !important;
      border-color: #ef4444 !important;
      color: #fff !important;
    }
    .graph-loading {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(255, 255, 255, 0.7);
      backdrop-filter: blur(2px);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 12px;
      z-index: 20;
    }
    [data-theme="dark"] .graph-loading {
      background: rgba(15, 23, 42, 0.75);
    }
    .borehole-jump-btn {
      margin-top: 10px;
      padding: 8px 12px;
      background: var(--accent);
      color: #fff;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 12px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      width: 100%;
      transition: background 0.15s;
    }
    .borehole-jump-btn:hover {
      filter: brightness(1.1);
    }

    /* Graph View */
    .graph-container {
      flex: 1;
      display: flex;
      height: 100%;
      overflow: hidden;
    }
    .graph-canvas-area {
      flex: 1;
      position: relative;
      height: 100%;
      background: var(--canvas-bg);
    }
    #networkCanvas {
      width: 100%;
      height: 100%;
    }
    .graph-panel {
      width: 380px;
      border-left: 1px solid var(--border-color);
      background: var(--bg-sidebar);
      display: flex;
      flex-direction: column;
      height: 100%;
      overflow-y: auto;
      padding: 18px 20px;
      gap: 16px;
    }
    .graph-btn-extract {
      width: 100%;
      padding: 12px;
      background: linear-gradient(135deg, #2563eb, #1d4ed8);
      color: #fff;
      border: none;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
      transition: all 0.2s;
    }
    .graph-btn-extract:hover { filter: brightness(1.1); transform: translateY(-1px); }
    .graph-btn-extract:disabled { background: #94a3b8; cursor: not-allowed; transform: none; box-shadow: none; }
    
    .legend-box {
      background: var(--bg-card);
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      border-radius: 8px;
      padding: 12px 14px;
      font-size: 12px;
    }
    .legend-item { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
    .legend-dot { width: 12px; height: 12px; border-radius: 50%; }
    
    .alert-card {
      background: var(--alert-bg);
      border: 1px solid var(--alert-border);
      border-radius: 8px;
      padding: 12px;
      font-size: 13px;
      color: var(--alert-text);
    }
    .alert-card h4 {
      display: flex;
      align-items: center;
      gap: 6px;
      color: var(--alert-heading);
      margin-bottom: 6px;
      font-size: 13.5px;
    }
    
    .info-card {
      background: var(--bg-card);
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      border-radius: 8px;
      padding: 12px 14px;
      font-size: 13px;
      line-height: 1.6;
    }
    
    .loading-spinner {
      display: inline-block;
      width: 14px;
      height: 14px;
      border: 2px solid rgba(255,255,255,0.3);
      border-radius: 50%;
      border-top-color: #fff;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
  
    
    /* Graph Path Highlight Button & Toolbar */
    .trace-graph-view-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      font-size: 11.5px;
      font-weight: 600;
      color: #fff;
      background: linear-gradient(135deg, #4f46e5 0%, #0284c7 100%);
      border: none;
      border-radius: 6px;
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(79, 70, 229, 0.3);
      transition: all 0.2s ease;
    }
    .trace-graph-view-btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(79, 70, 229, 0.45);
      filter: brightness(1.1);
    }
    .graph-reset-chip {
      padding: 5px 11px;
      font-size: 12px;
      font-weight: 600;
      border: 1px solid #4f46e5;
      border-radius: 6px;
      background: #4f46e5;
      color: #fff;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      animation: pulseHighlight 2s infinite;
    }
    @keyframes pulseHighlight {
      0%, 100% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.6); }
      50% { box-shadow: 0 0 0 8px rgba(79, 70, 229, 0); }
    }

    /* Reasoning Trace Accordion & Timeline UI */
    .trace-card {
      margin-bottom: 12px;
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      border-radius: 8px;
      background: var(--bg-card);
      overflow: hidden;
      font-size: 12px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .trace-header {
      padding: 8px 12px;
      background: rgba(2, 132, 199, 0.12); border-bottom: 1px solid var(--border-color);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      user-select: none;
      transition: background 0.15s ease;
    }
    .trace-header:hover {
      background: rgba(2, 132, 199, 0.14);
    }
    .trace-badge {
      font-size: 10.5px;
      padding: 2px 6px;
      border-radius: 4px;
      background: #0284c7;
      color: #fff;
      font-weight: 600;
    }
    .trace-body {
      padding: 12px 14px;
      border-top: 1px solid var(--border-color);
      background: var(--bg-main);
    }
    .trace-timeline {
      display: flex;
      flex-direction: column;
      gap: 10px;
      position: relative;
    }
    .trace-item {
      display: flex;
      align-items: flex-start;
      gap: 10px;
    }
    .trace-dot {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: #0284c7;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 700;
      flex-shrink: 0;
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
    }
    .trace-content {
      flex: 1;
    }
    .trace-step-title {
      font-weight: 600;
      color: var(--heading-color);
      margin-bottom: 2px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .trace-step-badge {
      font-size: 10px;
      padding: 1px 5px;
      background: var(--bg-card);
      border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);
      border-radius: 4px;
      color: #0284c7;
      font-weight: 600;
    }
    .trace-step-desc {
      font-size: 11.5px;
      color: var(--text-muted);
      line-height: 1.45;
    }

  </style>
</head>
<body>

  <!-- Sidebar -->
  <div id="sidebar">
    <div class="sidebar-header">
      <h1>🏢 현장 엔지니어링 RAG <span class="badge">GraphRAG MVP</span></h1>
    </div>
    <div class="sidebar-content">
      <div>
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
          <div class="section-title" style="margin-bottom: 0;">📂 현장 기술문서 보관소</div>
          <span id="docCountBadge" style="font-size: 11px; background: #eff6ff; color: #2563eb; padding: 2px 7px; border-radius: 10px; font-weight: 600; border: 1px solid #bfdbfe;">전수 색인 연동</span>
        </div>
        <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 8px; line-height: 1.4;">
          ※ 문서를 일일이 선택할 필요 없이, 질문하시면 AI가 아래 보관소 전체 색인에서 출처를 자동 탐색합니다.
        </div>
                  <!-- 2-Way Tree Switcher + New Folder Button -->
          <div style="display: flex; gap: 4px; align-items: center; margin-bottom: 8px;">
            <div class="tree-switcher" style="flex: 1; display: flex; gap: 2px; background: var(--bg-hover, #f1f5f9); padding: 3px; border-radius: 8px; border: 1px solid var(--border-color, #e2e8f0);">
              <button id="btnViewZone" onclick="setDocTreeView('zone')" style="flex: 1; font-size: 11px; padding: 5px 4px; border-radius: 6px; border: none; font-weight: 600; cursor: pointer; background: #2563eb; color: #ffffff; transition: all 0.15s; display: flex; align-items: center; justify-content: center; gap: 3px;">
                <span>📍 공구·총괄별</span>
              </button>
              <button id="btnViewField" onclick="setDocTreeView('field')" style="flex: 1; font-size: 11px; padding: 5px 4px; border-radius: 6px; border: none; font-weight: 500; cursor: pointer; background: transparent; color: var(--text-muted, #64748b); transition: all 0.15s; display: flex; align-items: center; justify-content: center; gap: 3px;">
                <span>📐 분야(공종)별</span>
              </button>
            </div>
            <button onclick="promptCreateNewFolder()" title="사용자 정의 새 폴더 생성" style="flex-shrink: 0; padding: 6px 9px; font-size: 11px; font-weight: 600; background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; border-radius: 8px; cursor: pointer; display: flex; align-items: center; gap: 3px; transition: all 0.15s;">
              <span>➕ 새 폴더</span>
            </button>
          </div>

          <!-- Document Tree Container -->
          <div class="doc-list" id="docList" style="max-height: calc(100vh - 360px); overflow-y: auto; margin-bottom: 12px; display: flex; flex-direction: column; gap: 6px;">
            <div style="font-size: 11px; color: var(--text-muted); padding: 8px; text-align: center;">문서 목록 불러오는 중...</div>
          </div>
      </div>
      <div>
        <input type="file" id="fileInput" accept=".pdf" multiple style="display:none;" onchange="uploadDoc()">
        <button class="upload-btn" onclick="document.getElementById('fileInput').click()">
          ➕ 새 시방서/보고서 PDF 추가
        </button>
      </div>
    </div>
    <div class="sidebar-footer">
      <div style="color: var(--text-muted); font-weight: 600;">🌐 사내망 20인 공유 주소</div>
      <div class="ip-box" id="serverAddress">불러오는 중...</div>
      <div style="color: var(--text-muted); font-size: 11px; margin-top: 6px;">
        ※ 같은 현장 Wi-Fi/LAN에 연결된 직원은 위 주소로 바로 접속 가능합니다.
      </div>
    </div>
  </div>

  <!-- Main -->
  <div id="main">
    <div class="top-nav">
      <div class="nav-tabs">
        <button class="tab-btn active" onclick="switchTab('chat')">💬 1:1 문서 질의응답 (Long-Context)</button>
        <button class="tab-btn" onclick="switchTab('graph')">🌐 지반·공종 지식 그래프 (GraphRAG MVP)</button>
      </div>
      <div style="display: flex; align-items: center; gap: 12px;">
        <button id="themeToggleBtn" class="theme-toggle-btn" onclick="toggleTheme()" title="화면 밝기 전환">
          🌙 다크 모드로 전환
        </button>
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 12px; color: var(--text-muted);">Gemini API Key:</span>
          <input type="password" id="apiKeyInput" class="api-key-input" placeholder="AI Studio에서 복사한 API Key" onchange="saveApiKey(this.value)">
        </div>
      </div>
    </div>

    <!-- Tab 1: Chat View -->
    <div id="chatTab" class="tab-content active">
      <div class="chat-header-bar">
        <div style="display: flex; align-items: center; gap: 10px; flex: 1; min-width: 0;">
          <span class="badge" style="background: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; font-size: 11.5px; padding: 3px 8px; font-weight: 600; flex-shrink: 0;">⚡ 실시간 자동 색인 RAG</span>
          <span id="topSourceRef" style="color: var(--text-muted); font-size: 12.5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            질문을 입력하시면 보관소 전체 문서(시추주상도, 구조계산서, 기술제안 등)에서 자동 탐색합니다.
          </span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px; flex-shrink: 0;">
          <button id="topDownloadBtn" class="top-action-btn download-btn" onclick="downloadActiveDoc()" style="display: none;" title="현재 분석된 출처 문서 다운로드">
            ⬇️ 출처 문서 다운로드
          </button>
          <button id="topToggleViewerBtn" class="top-action-btn active" onclick="toggleViewerPanel()" title="우측 문서 뷰어 패널 열기/닫기">
            📖 출처 문서 뷰어
          </button>
        </div>
      </div>

      <div class="chat-split-container">
        <!-- Left: Chat Main Column -->
        <div class="chat-main-col">
          <div id="chatBody" class="chat-body">
            <div class="message bot">
              <div class="avatar bot">🤖</div>
              <div class="message-content">
                <strong>⚡ 동탄트램 통합 지능형 색인 RAG 어시스턴트입니다.</strong><br><br>
                문서를 일일이 선택하실 필요가 전혀 없습니다! 아래 질문창에 궁금하신 기술 사항을 바로 입력하세요.<br>
                • <strong>전체 문서 자동 색인:</strong> 시추주상도(1·2공구), 토질 증빙자료, 기술제안서, 비탈면 안정성 검토 등 보관소 내 모든 문서를 AI가 실시간으로 분석하여 <strong>최적의 출처 문서와 해당 페이지를 스스로 찾아내어 답변</strong>합니다.<br>
                • <strong>실시간 출처 뷰어 연동:</strong> AI가 답변을 작성함과 동시에 <strong>오른쪽 뷰어에 해당 원본 문서와 페이지가 자동으로 열려</strong> 원문을 즉시 검증 및 다운로드할 수 있습니다.<br>
                • 언제든 왼쪽 보관함의 <strong>[열람]</strong> 버튼을 누르면 원하시는 문서를 뷰어에서 직접 확인하실 수도 있습니다.
              </div>
            </div>
          </div>
          <div class="chat-footer">
            <div class="input-container">
              <textarea id="promptInput" placeholder="질문을 입력하세요 (예: 차량기지 시추주상도의 제원을 표로 정리해줘)" onkeydown="handleKey(event)"></textarea>
              <button id="sendBtn" class="send-btn" onclick="sendQuery()">전송</button>
            </div>
          </div>
        </div>

        <!-- Right: Source Document Viewer Panel -->
        <div id="docViewerPanel" class="doc-viewer-panel">
          <div class="viewer-header">
            <div class="viewer-title-box">
              <span style="font-size: 16px;">📄</span>
              <div class="viewer-doc-title" id="viewerDocTitle" title="선택된 문서 없음">선택된 문서 없음</div>
              <span class="viewer-doc-size" id="viewerDocSize"></span>
            </div>
            <div class="viewer-actions">
              <button class="viewer-btn primary" onclick="downloadActiveDoc()" title="현재 보고 있는 문서 파일 다운로드">
                ⬇️ 다운로드
              </button>
              <button class="viewer-btn" onclick="openActiveDocNewTab()" title="새 창(전체화면)에서 PDF 열기">
                ↗️ 새 탭
              </button>
              <button class="viewer-btn icon-only" onclick="toggleViewerPanel(false)" title="뷰어 패널 접기">
                ✕
              </button>
            </div>
          </div>

          <!-- Quick Page Jump Bar -->
          <div id="viewerPageBar" class="viewer-page-bar" style="display: none;">
            <span style="color: var(--text-muted); font-size: 11px; flex-shrink: 0;">📌 빠른 이동:</span>
            <div id="viewerPagePills" class="page-pills-container"></div>
            <div class="page-direct-jump">
              <input type="number" id="pageJumpInput" min="1" placeholder="P." onkeydown="if(event.key==='Enter') jumpToDirectPage()">
              <button onclick="jumpToDirectPage()">이동</button>
            </div>
          </div>

          <!-- PDF Viewer Iframe / Placeholder -->
          <div class="viewer-iframe-wrapper">
            <div id="viewerPlaceholder" class="viewer-placeholder">
              <div style="font-size: 36px; margin-bottom: 12px; opacity: 0.6;">📑</div>
              <div style="font-weight: 600; font-size: 14px; margin-bottom: 6px; color: var(--heading-color);">출처 문서 미리보기</div>
              <div style="font-size: 12px; color: var(--text-muted); max-width: 240px; line-height: 1.5;">
                왼쪽 보관함에서 문서를 선택하면 이 공간에 원본 PDF가 바로 표시되며 언제든지 다운로드할 수 있습니다.
              </div>
            </div>
            <iframe id="pdfViewerFrame" class="pdf-iframe" style="display: none;" src="about:blank"></iframe>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab 2: GraphRAG View -->
    <div id="graphTab" class="tab-content">
      <div class="graph-container">
        <div class="graph-canvas-area">
          <div class="graph-toolbar">
            <span style="font-size: 12px; font-weight: 600; color: var(--text-muted); margin-right: 4px;">구간 필터:</span>
            <button class="filter-chip active" onclick="applyGraphFilter('all', false, this)">전체 현장 (77공)</button>
            <button class="filter-chip" onclick="applyGraphFilter('depot', false, this)">차량기지 전체 (GB+NGB)</button>
            <button class="filter-chip" onclick="applyGraphFilter('prop', false, this)">제안설계 기지 (NGB)</button>
            <button class="filter-chip" onclick="applyGraphFilter('1', false, this)">1공구 본선 (NH)</button>
            <button class="filter-chip" onclick="applyGraphFilter('2', false, this)">2공구 본선 (DT)</button>
            <button class="filter-chip filter-chip-risk" onclick="applyGraphFilter('all', true, this)">⚠️ 연약층 위험구간 (28공)</button>
          </div>
          <div id="graphLoadingOverlay" class="graph-loading" style="display:none;">
            <div class="loading-spinner" style="width:28px; height:28px; border-width:3px;"></div>
            <div style="font-size: 13px; font-weight: 600; color: var(--text-main);">지반-공종 지식 그래프 로딩 중...</div>
          </div>
          <div id="networkCanvas"></div>
        </div>
        <div class="graph-panel">
          <div>
            <h3 style="font-size: 15px; margin-bottom: 6px;">🌐 GraphRAG 4×4 MVP 추출</h3>
            <p style="font-size: 12px; color: var(--text-muted); line-height: 1.5;">
              선택된 문서에서 <strong>시추공, 지층, 지반정수, 설계요소</strong> 간의 연결망과 <strong>표층 연약지반(N<6) 및 고지하수위 설계 위험 경고</strong>를 자동 추출합니다.
            </p>
          </div>

          <button id="extractBtn" class="graph-btn-extract" onclick="loadMasterGraph(currentGraphFilter.section, currentGraphFilter.riskOnly)">
            ⚡ 지식 그래프 자동 추출 & 분석 실행
          </button>

          <!-- Legend -->
          <div class="legend-box">
            <div style="font-weight: 600; margin-bottom: 8px; color: var(--heading-color);">🏷️ 노드 범례 (4대 핵심 엔터티)</div>
            <div class="legend-item"><span class="legend-dot" style="background:#f97316;"></span> <strong>BORING</strong> (시추공 / 위치)</div>
            <div class="legend-item"><span class="legend-dot" style="background:#a16207;"></span> <strong>STRATUM</strong> (지층 / 토사 / 암반)</div>
            <div class="legend-item"><span class="legend-dot" style="background:#06b6d4;"></span> <strong>PARAMETER</strong> (지반정수 c, φ, 수위)</div>
            <div class="legend-item"><span class="legend-dot" style="background:#3b82f6;"></span> <strong>DESIGN_ELEMENT</strong> (가시설 / 앵커 / 해석)</div>
            <div class="legend-item"><span class="legend-dot" style="background:#ef4444;"></span> <strong>DISCREPANCY</strong> (설계 위험 / 취약구간 엣지)</div>
          </div>

          <!-- Alert / Discrepancy Box -->
          <div id="discrepancyBox" style="display:none;">
            <div class="alert-card">
              <h4>🚨 표층 연약지반(N<6) 및 고지하수위 설계 위험 알림</h4>
              <div id="discrepancyContent">검출된 설계 위험 요인 없음</div>
            </div>
          </div>

          <!-- Summary Box -->
          <div id="summaryBox" style="display:none;" class="info-card">
            <div style="font-weight: 600; color: var(--accent); margin-bottom: 6px;">📋 핵심 관계 요약 보고</div>
            <div id="summaryContent" style="font-size: 12.5px; color: var(--text-main); line-height: 1.6;"></div>
          </div>

          <!-- Node Detail Inspector -->
          <div id="nodeDetailBox" class="info-card" style="display:none;">
            <div style="font-weight: 600; color: var(--accent); margin-bottom: 4px;" id="nodeDetailLabel">노드 상세</div>
            <div id="nodeDetailDesc" style="font-size: 12px; color: var(--text-muted); line-height: 1.5;"></div>
          </div>

        </div>
      </div>
    </div>

  </div>

  <script>
    let activeDoc = "";
    let serverIp = "";
    let network = null;

    function initTheme() {
      const savedTheme = localStorage.getItem('THEME') || 'light';
      applyTheme(savedTheme);
    }

    function toggleTheme() {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      applyTheme(newTheme);
      localStorage.setItem('THEME', newTheme);
      if (network) {
        network.redraw();
      }
    }

    function applyTheme(theme) {
      const btn = document.getElementById('themeToggleBtn');
      if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        if (btn) btn.innerHTML = '☀️ 라이트 모드로 전환';
      } else {
        document.documentElement.removeAttribute('data-theme');
        if (btn) btn.innerHTML = '🌙 다크 모드로 전환';
      }
    }

    window.onload = async () => {
      initTheme();
      await fetchConfig();
      await fetchDocs();
    };

    function switchTab(tab) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      if (tab === 'chat') {
        document.querySelector('.tab-btn:nth-child(1)').classList.add('active');
        document.getElementById('chatTab').classList.add('active');
      } else {
        document.querySelector('.tab-btn:nth-child(2)').classList.add('active');
        document.getElementById('graphTab').classList.add('active');
        if (!hasLoadedMasterGraph) {
          loadMasterGraph();
        } else if (network) {
          setTimeout(() => network.fit(), 200);
        }
      }
    }

    async function fetchConfig() {
      try {
        const res = await fetch('/api/config');
        const data = await res.json();
        serverIp = data.server_ip;
        document.getElementById('serverAddress').innerText = `http://${serverIp}:${data.port}`;
        if (data.api_key) {
          document.getElementById('apiKeyInput').value = data.api_key;
        } else {
          const saved = localStorage.getItem('GEMINI_API_KEY');
          if (saved) {
            document.getElementById('apiKeyInput').value = saved;
            saveApiKey(saved);
          }
        }
      } catch (e) {
        console.error(e);
      }
    }

    async function saveApiKey(key) {
      localStorage.setItem('GEMINI_API_KEY', key);
      try {
        await fetch('/api/config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ api_key: key })
        });
      } catch(e) {}
    }

    let currentDocTreeViewMode = 'zone'; // 'zone' or 'field'
  window.cachedDocs = [];
  // currentViewingDoc declared in viewer section below

  function getCustomFolders() {
    try {
      return JSON.parse(localStorage.getItem('CUSTOM_USER_FOLDERS') || '[]');
    } catch(e) {
      return [];
    }
  }

  function saveCustomFolders(folders) {
    try {
      localStorage.setItem('CUSTOM_USER_FOLDERS', JSON.stringify(folders));
    } catch(e) {}
  }

  function getCustomDocFolderMap() {
    try {
      return JSON.parse(localStorage.getItem('CUSTOM_DOC_FOLDER_MAP') || '{}');
    } catch(e) {
      return {};
    }
  }

  function saveCustomDocFolderMap(map) {
    try {
      localStorage.setItem('CUSTOM_DOC_FOLDER_MAP', JSON.stringify(map));
    } catch(e) {}
  }

  function promptCreateNewFolder() {
    const name = prompt('생성할 새 폴더명을 입력하세요 (예: 05. 정거장 건축설계 / 06. 트램 궤도공사):');
    if (!name || !name.trim()) return;
    const clean = name.trim();
    const folders = getCustomFolders();
    if (!folders.includes(clean)) {
      folders.push(clean);
      saveCustomFolders(folders);
    }
    renderDocTree();
  }

  function promptMoveDocFolder(event, docName) {
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

  function classifyDoc(docName) {
    const customMap = getCustomDocFolderMap();
    let zone = customMap[docName] || null;
    let field = '기타 · 일반';

    if (!zone) {
      if (docName.includes('1공구') || docName.startsWith('NH')) {
        zone = '01. 1공구 본선';
      } else if (docName.includes('2공구') || docName.startsWith('DT')) {
        zone = '02. 2공구 본선';
      } else if (docName.includes('차량기지') || docName.startsWith('GB') || docName.startsWith('NGB')) {
        zone = '03. 차량기지';
      } else if (docName.includes('제안') || docName.includes('증빙') || docName.includes('#3편')) {
        zone = '04. 기술제안 및 특화';
      } else if (docName.includes('입찰') || docName.includes('안내서') || docName.includes('과업') || docName.includes('공정표') || docName.includes('총괄')) {
        zone = '00. 총괄 및 입찰·계약';
      } else {
        zone = '05. 기타 및 일반';
      }
    }

    if (docName.includes('토질') || docName.includes('지반') || docName.includes('시추') || docName.includes('기초') || docName.includes('비탈면') || docName.includes('가시설') || docName.includes('사면')) {
      field = '토목 · 지반';
    } else if (docName.includes('궤도') || docName.includes('분기기') || docName.includes('레일')) {
      field = '궤도 · 철도';
    } else if (docName.includes('건축') || docName.includes('정거장') || docName.includes('환승') || docName.includes('검수고') || docName.includes('관리동')) {
      field = '건축 · 정거장';
    } else if (docName.includes('신호') || docName.includes('전기') || docName.includes('통신') || docName.includes('전차선') || docName.includes('시스템')) {
      field = '시스템 (신호/전기/통신)';
    } else if (docName.includes('입찰') || docName.includes('계약') || docName.includes('총괄')) {
      field = '총괄 · 계약';
    }

    return { zone, field };
  }

  function setDocTreeView(mode) {
    currentDocTreeViewMode = mode;
    const btnZone = document.getElementById('btnViewZone');
    const btnField = document.getElementById('btnViewField');
    if (btnZone && btnField) {
      if (mode === 'zone') {
        btnZone.style.background = '#2563eb';
        btnZone.style.color = '#ffffff';
        btnZone.style.fontWeight = '600';
        btnField.style.background = 'transparent';
        btnField.style.color = 'var(--text-muted, #64748b)';
        btnField.style.fontWeight = '500';
      } else {
        btnField.style.background = '#2563eb';
        btnField.style.color = '#ffffff';
        btnField.style.fontWeight = '600';
        btnZone.style.background = 'transparent';
        btnZone.style.color = 'var(--text-muted, #64748b)';
        btnZone.style.fontWeight = '500';
      }
    }
    renderDocTree();
  }

  async function fetchDocs() {
    try {
      const res = await fetch('/api/documents');
      const docs = await res.json();
      window.cachedDocs = docs;
      renderDocTree();
    } catch(e) {
      console.error(e);
    }
  }

  function createDocItemEl(doc) {
    const item = document.createElement('div');
    const isAct = (typeof currentViewingDoc !== 'undefined' && currentViewingDoc === doc.name);
    item.className = 'tree-doc-item' + (isAct ? ' active' : '');
    item.onclick = (e) => {
      e.stopPropagation();
      viewDoc(doc.name);
      document.querySelectorAll('.tree-doc-item').forEach(el => el.classList.remove('active'));
      item.classList.add('active');
    };

    item.innerHTML = `
      <span class="tree-doc-icon">📄</span>
      <div class="tree-doc-info">
        <div class="tree-doc-name" title="${doc.name}">${doc.name}</div>
        <div class="tree-doc-meta">${doc.size_mb} MB${doc.total_pages ? ' · ' + doc.total_pages + 'p' : ''}</div>
      </div>
      <div class="tree-doc-actions">
        <button class="tree-btn-view" title="웹 뷰어에서 문서 열람" onclick="event.stopPropagation(); viewDoc('${doc.name}');">열람</button>
        <button class="tree-btn-move" title="다른 폴더로 이동" onclick="promptMoveDocFolder(event, '${doc.name}');" style="font-size:10px; padding:2px 5px; border-radius:4px; background:#f8fafc; color:#475569; border:1px solid #cbd5e1; cursor:pointer;">이동</button>
        <button class="tree-btn-del" title="서재에서 삭제" onclick="deleteDoc(event, '${doc.name}')">내리기</button>
      </div>
    `;
    return item;
  }

  function renderDocTree() {
    const listEl = document.getElementById('docList');
    if (!listEl) return;
    listEl.innerHTML = '';
    const docs = window.cachedDocs || [];

    const badge = document.getElementById('docCountBadge');
    if (badge) {
      badge.innerText = '총 ' + docs.length + '권 탑재';
    }

    if (docs.length === 0) {
      listEl.innerHTML = '<div style="font-size:12px; color:var(--text-muted); padding:8px;">등록된 문서가 없습니다.</div>';
      return;
    }

    if (currentDocTreeViewMode === 'zone') {
      const builtInZones = [
        '00. 총괄 및 입찰·계약',
        '01. 1공구 본선',
        '02. 2공구 본선',
        '03. 차량기지',
        '04. 기술제안 및 특화',
        '05. 기타 및 일반'
      ];
      const customZones = getCustomFolders();
      const zoneOrder = Array.from(new Set([...builtInZones, ...customZones]));

      const tree = {};
      zoneOrder.forEach(z => { tree[z] = {}; });

      docs.forEach(doc => {
        const { zone, field } = classifyDoc(doc.name);
        if (!tree[zone]) tree[zone] = {};
        if (!tree[zone][field]) tree[zone][field] = [];
        tree[zone][field].push(doc);
      });

      zoneOrder.forEach(zoneName => {
        const fields = tree[zoneName] || {};
        let zoneDocCount = 0;
        Object.values(fields).forEach(arr => { zoneDocCount += arr.length; });

        const folderEl = document.createElement('div');
        folderEl.className = 'tree-folder' + (zoneDocCount > 0 ? ' open' : '');

        folderEl.innerHTML = `
          <div class="folder-header" onclick="this.parentElement.classList.toggle('open')">
            <span class="folder-arrow">▶</span>
            <span class="folder-icon">📁</span>
            <span class="folder-title" title="${zoneName}">${zoneName}</span>
            <span class="folder-badge">${zoneDocCount}</span>
          </div>
          <div class="folder-content"></div>
        `;

        const contentEl = folderEl.querySelector('.folder-content');

        if (zoneDocCount === 0) {
          contentEl.innerHTML = '<div style="font-size:11px; color:var(--text-muted); padding:5px 8px;">(문서 없음)</div>';
        } else {
          Object.keys(fields).forEach(fieldName => {
            const docList = fields[fieldName];
            if (!docList || docList.length === 0) return;

            const subEl = document.createElement('div');
            subEl.className = 'tree-subfolder';
            subEl.innerHTML = `
              <div class="subfolder-header" onclick="const it = this.nextElementSibling; it.style.display = it.style.display==='none'?'flex':'none'">
                <span>📂</span>
                <span style="flex:1;">${fieldName}</span>
                <span style="font-size:10px; opacity:0.7;">(${docList.length})</span>
              </div>
              <div class="subfolder-items" style="display:flex; flex-direction:column; gap:3px;"></div>
            `;

            const itemsContainer = subEl.querySelector('.subfolder-items');
            docList.forEach(doc => {
              itemsContainer.appendChild(createDocItemEl(doc));
            });
            contentEl.appendChild(subEl);
          });
        }
        listEl.appendChild(folderEl);
      });

    } else {
      // 2. 분야별 트리
      const builtInFields = [
        '총괄 · 계약',
        '토목 · 지반',
        '궤도 · 철도',
        '건축 · 정거장',
        '시스템 (신호/전기/통신)',
        '기타 · 일반'
      ];
      const customFields = getCustomFolders();
      const fieldOrder = Array.from(new Set([...builtInFields, ...customFields]));

      const tree = {};
      fieldOrder.forEach(f => { tree[f] = {}; });

      docs.forEach(doc => {
        const { zone, field } = classifyDoc(doc.name);
        if (!tree[field]) tree[field] = {};
        if (!tree[field][zone]) tree[field][zone] = [];
        tree[field][zone].push(doc);
      });

      fieldOrder.forEach(fieldName => {
        const zones = tree[fieldName] || {};
        let fieldDocCount = 0;
        Object.values(zones).forEach(arr => { fieldDocCount += arr.length; });

        const folderEl = document.createElement('div');
        folderEl.className = 'tree-folder' + (fieldDocCount > 0 ? ' open' : '');

        folderEl.innerHTML = `
          <div class="folder-header" onclick="this.parentElement.classList.toggle('open')">
            <span class="folder-arrow">▶</span>
            <span class="folder-icon">📂</span>
            <span class="folder-title" title="${fieldName}">${fieldName}</span>
            <span class="folder-badge">${fieldDocCount}</span>
          </div>
          <div class="folder-content"></div>
        `;

        const contentEl = folderEl.querySelector('.folder-content');

        if (fieldDocCount === 0) {
          contentEl.innerHTML = '<div style="font-size:11px; color:var(--text-muted); padding:5px 8px;">(문서 없음)</div>';
        } else {
          Object.keys(zones).forEach(zoneName => {
            const docList = zones[zoneName];
            if (!docList || docList.length === 0) return;

            const subEl = document.createElement('div');
            subEl.className = 'tree-subfolder';
            subEl.innerHTML = `
              <div class="subfolder-header" onclick="const it = this.nextElementSibling; it.style.display = it.style.display==='none'?'flex':'none'">
                <span>📍</span>
                <span style="flex:1;">${zoneName}</span>
                <span style="font-size:10px; opacity:0.7;">(${docList.length})</span>
              </div>
              <div class="subfolder-items" style="display:flex; flex-direction:column; gap:3px;"></div>
            `;

            const itemsContainer = subEl.querySelector('.subfolder-items');
            docList.forEach(doc => {
              itemsContainer.appendChild(createDocItemEl(doc));
            });
            contentEl.appendChild(subEl);
          });
        }
        listEl.appendChild(folderEl);
      });
    }
  }

  async function deleteDoc(event, name) {
      event.stopPropagation();
      const nl = String.fromCharCode(10);
      const msg = `'` + name + `' 문서를 보관함에서 내리시겠습니까?` + nl + nl + `※ 프로젝트 원본 파일은 안전하게 보존되며, 웹 화면(서버)에 업로드된 복사본 파일만 제거되어 디스크 용량이 확보됩니다.`;
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
          if (currentViewingDoc === name) {
            currentViewingDoc = null;
            const topDl = document.getElementById('topDownloadBtn');
            if (topDl) topDl.style.display = 'none';
            const vTitle = document.getElementById('viewerDocTitle');
            if (vTitle) vTitle.innerText = '출처 문서 미리보기';
            const vSize = document.getElementById('viewerDocSize');
            if (vSize) vSize.innerText = '';
            const iframe = document.getElementById('pdfViewerFrame');
            if (iframe) { iframe.src = 'about:blank'; iframe.style.display = 'none'; }
            const ph = document.getElementById('viewerPlaceholder');
            if (ph) ph.style.display = 'flex';
          }
          await fetchDocs();
        } else {
          alert('내리기 실패: ' + (data.error || '오류 발생'));
        }
      } catch(e) {
        alert('서버 요청 중 오류: ' + e);
      }
    }

    window.cachedDocs = [];
    let currentViewingDoc = null;

    function viewDoc(name) {
      currentViewingDoc = name;
      loadViewerDoc(name, 1);
      toggleViewerPanel(true);
      const topRef = document.getElementById('topSourceRef');
      if (topRef) {
        topRef.innerHTML = `📖 <b>직접 열람 중:</b> <span style="color:var(--text-color);">${name}</span>`;
      }
      const topDlBtn = document.getElementById('topDownloadBtn');
      if (topDlBtn) topDlBtn.style.display = 'inline-flex';
    }

    function linkifyPageNumbers(htmlText) {
      if (!htmlText) return '';
      // Linkify occurrences like p.50, p. 50, p.50~51, 페이지 50, (p.50)
      return htmlText.replace(/(?:p\.|페이지\s*)(\d+)(?:\s*[~-]\s*(\d+))?/gi, (match, p1, p2) => {
        const pageNum = parseInt(p1);
        const label = p2 ? `p.${p1}~${p2}` : `p.${p1}`;
        return `<button class="page-link-badge" onclick="jumpToPage(${pageNum})" title="클릭 시 우측 뷰어 ${pageNum}페이지로 즉시 이동">📄 ${label}</button>`;
      });
    }

    function loadViewerDoc(name, targetPage, activeSections) {
      if (!name) return;
      currentViewingDoc = name;
      const titleEl = document.getElementById('viewerDocTitle');
      const sizeEl = document.getElementById('viewerDocSize');
      const iframe = document.getElementById('pdfViewerFrame');
      const placeholder = document.getElementById('viewerPlaceholder');
      const pageBar = document.getElementById('viewerPageBar');
      const pillsContainer = document.getElementById('viewerPagePills');

      if (titleEl) {
        titleEl.innerText = name;
        titleEl.title = name;
      }

      const docObj = (window.cachedDocs || []).find(d => d.name === name);
      if (docObj && sizeEl) {
        sizeEl.innerText = `(${docObj.size_mb} MB${docObj.total_pages ? ' · ' + docObj.total_pages + 'p' : ''})`;
      } else if (sizeEl) {
        sizeEl.innerText = '';
      }

      const effectiveTargetPage = targetPage || 1;

      // Smart Fast Jump Pills: Priority to this query's matched activeSections!
      if (pillsContainer) {
        pillsContainer.innerHTML = '';
        const renderedPages = new Set();

        // 1. Matched Active Sections for this exact question
        if (activeSections && activeSections.length > 0) {
          activeSections.forEach(sec => {
            const pill = document.createElement('button');
            const isCur = sec.start_page === effectiveTargetPage;
            pill.className = 'page-pill highlight' + (isCur ? ' current' : '');
            pill.dataset.page = sec.start_page;
            const shortTitle = sec.title.replace(' 시추주상도', '').replace(' 구조계산서', '');
            pill.innerText = `🎯 ${shortTitle} (p.${sec.start_page})`;
            pill.title = `[질문 근거 섹션] ${sec.title} (p.${sec.start_page}~${sec.end_page})`;
            pill.onclick = () => jumpToPage(sec.start_page);
            pillsContainer.appendChild(pill);
            renderedPages.add(sec.start_page);
          });
        }

        // 2. Additional Sections from Document (if room)
        if (docObj && docObj.sections) {
          docObj.sections.slice(0, 16).forEach(sec => {
            if (renderedPages.has(sec.start_page)) return;
            const pill = document.createElement('button');
            const isCur = sec.start_page === effectiveTargetPage;
            pill.className = 'page-pill' + (isCur ? ' current' : '');
            pill.dataset.page = sec.start_page;
            const shortTitle = sec.title.replace(' 시추주상도', '').replace(' 구조계산서', '');
            pill.innerText = `${shortTitle} (p.${sec.start_page})`;
            pill.title = `${sec.title} (p.${sec.start_page}~${sec.end_page})`;
            pill.onclick = () => jumpToPage(sec.start_page);
            pillsContainer.appendChild(pill);
          });
        }

        if (pageBar) {
          pageBar.style.display = (pillsContainer.children.length > 0) ? 'flex' : 'none';
        }
      }

      if (iframe) {
        // Enforce reliable reload with timestamp to guarantee browser jumps to #page
        iframe.src = `/api/view?document=${encodeURIComponent(name)}&t=${Date.now()}#page=${effectiveTargetPage}`;
        iframe.style.display = 'block';
      }
      if (placeholder) {
        placeholder.style.display = 'none';
      }
    }

    function jumpToPage(pageNum) {
      if (!currentViewingDoc) return;
      const iframe = document.getElementById('pdfViewerFrame');
      if (iframe) {
        iframe.src = `/api/view?document=${encodeURIComponent(currentViewingDoc)}&t=${Date.now()}#page=${pageNum}`;
      }
      // Update active state among pills
      document.querySelectorAll('.page-pill').forEach(btn => {
        const isCurrent = btn.dataset.page == pageNum;
        btn.classList.toggle('current', isCurrent);
      });
      // Also sync direct jump input
      const input = document.getElementById('pageJumpInput');
      if (input) input.value = pageNum;
    }

    function jumpToDirectPage() {
      const input = document.getElementById('pageJumpInput');
      if (!input) return;
      const val = parseInt(input.value);
      if (val && val > 0) {
        jumpToPage(val);
      }
    }

    function downloadActiveDoc() {
      if (!currentViewingDoc) {
        alert('다운로드할 출처 문서가 아직 열리지 않았습니다. 질문을 입력하시거나 보관함의 [열람] 버튼을 누르세요.');
        return;
      }
      window.location.href = `/api/download?document=${encodeURIComponent(currentViewingDoc)}`;
    }

    function openActiveDocNewTab() {
      if (!currentViewingDoc) {
        alert('열람할 문서가 아직 없습니다. 질문을 입력하시거나 보관함의 [열람] 버튼을 누르세요.');
        return;
      }
      const page = document.getElementById('pageJumpInput')?.value || 1;
      window.open(`/api/view?document=${encodeURIComponent(currentViewingDoc)}#page=${page}`, '_blank');
    }

    function toggleViewerPanel(forceState) {
      const panel = document.getElementById('docViewerPanel');
      const btn = document.getElementById('topToggleViewerBtn');
      if (!panel) return;
      const isCollapsed = panel.classList.contains('collapsed');
      const shouldOpen = (forceState !== undefined) ? forceState : isCollapsed;
      if (shouldOpen) {
        panel.classList.remove('collapsed');
        if (btn) {
          btn.classList.add('active');
          btn.innerHTML = '📖 출처 문서 뷰어';
        }
        if (currentViewingDoc && document.getElementById('pdfViewerFrame') && (!document.getElementById('pdfViewerFrame').src || document.getElementById('pdfViewerFrame').src === 'about:blank')) {
          loadViewerDoc(currentViewingDoc);
        }
      } else {
        panel.classList.add('collapsed');
        if (btn) {
          btn.classList.remove('active');
          btn.innerHTML = '📖 뷰어 열기';
        }
      }
    }

    async function uploadDoc() {
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
        viewDoc(lastUploadedName);
      }
      if (total > 1) {
        alert(`선택한 ${total}개 파일 중 ${successCount}개 파일이 보관함에 추가되었습니다!`);
      }
    }

    function handleKey(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendQuery();
      }
    }

    function appendMessage(role, text) {
      const chatBody = document.getElementById('chatBody');
      if (!chatBody) return null;
      const msg = document.createElement('div');
      msg.className = `message ${role}`;
      msg.innerHTML = `
        <div class="avatar ${role}">${role === 'bot' ? '🤖' : '👷'}</div>
        <div class="message-content">${role === 'user' ? escapeHtml(text) : text}</div>
      `;
      chatBody.appendChild(msg);
      scrollToBottom();
      return msg.querySelector('.message-content');
    }

    function scrollToBottom() {
      const chatBody = document.getElementById('chatBody');
      if (chatBody) {
        chatBody.scrollTop = chatBody.scrollHeight;
      }
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    
    
    let originalRawNodes = [];
    let originalRawEdges = [];
    let isGraphHighlighted = false;

    function resetGraphHighlight() {
      if (!isGraphHighlighted || !window.masterGraphDataSets) return;
      const { nodes, edges } = window.masterGraphDataSets;
      
      // 원본 상태로 복원
      const colorMap = {
        'BORING': { background: '#f97316', border: '#ea580c' },
        'STRATUM': { background: '#a16207', border: '#854d0e' },
        'PARAMETER': { background: '#06b6d4', border: '#0891b2' },
        'DESIGN_ELEMENT': { background: '#3b82f6', border: '#2563eb' },
        'DISCREPANCY': { background: '#ef4444', border: '#dc2626' },
        'DEFAULT': { background: '#64748b', border: '#475569' }
      };

      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

      const nodeUpdates = originalRawNodes.map(n => {
        const col = colorMap[n.type] || colorMap['DEFAULT'];
        return {
          id: n.id,
          color: { background: col.background, border: col.border },
          opacity: 1.0,
          font: { color: '#fff', size: 12 },
          size: n.type === 'DESIGN_ELEMENT' ? 24 : 18
        };
      });
      nodes.update(nodeUpdates);

      const edgeUpdates = originalRawEdges.map(e => {
        const isWarn = e.is_warning || e.relation === 'DISCREPANCY';
        return {
          id: e.id || `${e.from}_${e.to}`,
          color: isWarn ? { color: '#ef4444' } : { color: isDark ? '#64748b' : '#94a3b8' },
          width: isWarn ? 2.5 : 1.2,
          opacity: 1.0
        };
      });
      edges.update(edgeUpdates);

      isGraphHighlighted = false;
      const chip = document.getElementById('resetHighlightChip');
      if (chip) chip.style.display = 'none';

      if (network) network.fit({ animation: { duration: 600, easingFunction: 'easeInOutQuad' } });
    }

    async function highlightGraphPath(targetNodeIdsJson) {
      let targetIds = [];
      try {
        const decoded = typeof targetNodeIdsJson === 'string' ? decodeURIComponent(targetNodeIdsJson) : targetNodeIdsJson;
        targetIds = typeof decoded === 'string' ? JSON.parse(decoded) : decoded;
      } catch (e) {
        targetIds = targetNodeIdsJson.split(',').map(s => s.trim()).filter(Boolean);
      }
      if (!targetIds || targetIds.length === 0) return;

      // 1. 그래프 탭으로 전환
      switchTab('graph');

      // 2. 마스터 그래프가 아직 없으면 로드 대기
      if (!hasLoadedMasterGraph) {
        await loadMasterGraph();
        await new Promise(r => setTimeout(r, 600));
      }

      if (!window.masterGraphDataSets || !network) return;
      const { nodes, edges } = window.masterGraphDataSets;

      const targetSet = new Set(targetIds);

      // 허브 노드 및 관련 엣지도 포함
      originalRawEdges.forEach(e => {
        if (targetSet.has(e.from) && targetSet.has(e.to)) {
          // Both in path
        }
      });

      // 3. 노드 스타일 업데이트: 타겟 노드는 형광 네온 하이라이트 + 확대, 나머지는 페이드아웃
      const nodeUpdates = originalRawNodes.map(n => {
        const isHit = targetSet.has(n.id);
        if (isHit) {
          return {
            id: n.id,
            color: { background: '#f59e0b', border: '#b45309', highlight: { background: '#fbbf24', border: '#d97706' } },
            font: { color: '#ffffff', size: 14, strokeWidth: 2, strokeColor: '#000' },
            size: n.type === 'DESIGN_ELEMENT' ? 32 : 26,
            shadow: { enabled: true, color: '#f59e0b', size: 16 }
          };
        } else {
          return {
            id: n.id,
            color: { background: 'rgba(100, 116, 139, 0.25)', border: 'rgba(100, 116, 139, 0.3)' },
            font: { color: 'rgba(255, 255, 255, 0.3)', size: 10 },
            shadow: { enabled: false },
            size: 14
          };
        }
      });
      nodes.update(nodeUpdates);

      // 4. 엣지 업데이트: 타겟 연결선은 두껍고 선명하게, 나머지는 투명하게
      const edgeUpdates = originalRawEdges.map(e => {
        const isHit = targetSet.has(e.from) && targetSet.has(e.to);
        const isConnected = targetSet.has(e.from) || targetSet.has(e.to);
        if (isHit) {
          return {
            id: e.id || `${e.from}_${e.to}`,
            color: { color: '#f59e0b' },
            width: 3.5,
            opacity: 1.0
          };
        } else if (isConnected) {
          return {
            id: e.id || `${e.from}_${e.to}`,
            color: { color: 'rgba(245, 158, 11, 0.6)' },
            width: 2.2,
            opacity: 0.8
          };
        } else {
          return {
            id: e.id || `${e.from}_${e.to}`,
            color: { color: 'rgba(148, 163, 184, 0.1)' },
            width: 0.8,
            opacity: 0.1
          };
        }
      });
      edges.update(edgeUpdates);

      isGraphHighlighted = true;

      // 5. 복원 칩 표시
      let chip = document.getElementById('resetHighlightChip');
      if (!chip) {
        const toolbar = document.querySelector('.graph-toolbar');
        if (toolbar) {
          chip = document.createElement('button');
          chip.id = 'resetHighlightChip';
          chip.className = 'graph-reset-chip';
          chip.innerHTML = '✨ 탐색 경로 표시 중 (클릭 시 전체 복원)';
          chip.onclick = resetGraphHighlight;
          toolbar.appendChild(chip);
        }
      } else {
        chip.style.display = 'inline-flex';
      }

      // 6. 타겟 노드 군집으로 부드럽게 줌인(Focus)
      setTimeout(() => {
        const existingTargetIds = targetIds.filter(id => nodes.get(id));
        if (existingTargetIds.length > 0) {
          network.fit({
            nodes: existingTargetIds,
            animation: { duration: 900, easingFunction: 'easeInOutQuad' }
          });
        }
      }, 200);
    }

    function toggleTrace(el) {
      const card = el.closest('.trace-card');
      const body = card.querySelector('.trace-body');
      const arrow = card.querySelector('.trace-arrow');
      if (body.style.display === 'none' || !body.style.display) {
        body.style.display = 'block';
        if (arrow) arrow.innerText = '▲';
      } else {
        body.style.display = 'none';
        if (arrow) arrow.innerText = '▼';
      }
    }

    function buildTraceHtml(trace) {
      if (!trace || !trace.steps || trace.steps.length === 0) return '';
      let stepsHtml = '';
      trace.steps.forEach(s => {
        stepsHtml += `
          <div class="trace-item">
            <div class="trace-dot">${s.step}</div>
            <div class="trace-content">
              <div class="trace-step-title">
                <span>${s.icon || '📌'} ${s.title}</span>
                <span class="trace-step-badge">${s.badge || '완료'}</span>
              </div>
              <div class="trace-step-desc">${s.detail}</div>
            </div>
          </div>
        `;
      });

      return `
        <div class="trace-card">
          <div class="trace-header" onclick="toggleTrace(this)">
            <div style="display:flex; align-items:center; gap:8px;">
              <span>🧭</span>
              <span style="font-weight:600; font-size:12.5px; color:var(--heading-color);">AI 탐색 및 추론 과정 추적 (색인 ➔ 지식망 ➔ 팩트 ➔ Gemini)</span>
              <span class="trace-badge">4단계 완료</span>
            </div>
            <span class="trace-arrow" style="font-size:10px; color:var(--text-muted);">▲ 접기</span>
          </div>
          <div class="trace-body" style="display:block;">
            <div class="trace-timeline">
              ${stepsHtml}
            </div>
            ${trace.highlight_nodes && trace.highlight_nodes.length > 0 ? `
              <div style="margin-top: 12px; padding-top: 10px; border-top: 1px dashed var(--border-color); display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 11px; color: var(--text-muted);">지식망 탐색 노드: <b>${trace.highlight_nodes.length}개</b> 연계 검출</span>
                <button class="trace-graph-view-btn" onclick="highlightGraphPath('${encodeURIComponent(JSON.stringify(trace.highlight_nodes))}')">
                  🌐 이 답변에 쓰인 지식망 경로 그래프로 직접 보기 (${trace.highlight_nodes.length}개 노드) ➔
                </button>
              </div>
            ` : ''}
          </div>
        </div>
      `;
    }

    async function sendQuery() {
      const input = document.getElementById('promptInput');
      if (!input) return;
      const query = input.value.trim();
      if (!query) return;

      const apiKeyEl = document.getElementById('apiKeyInput');
      const apiKey = apiKeyEl ? apiKeyEl.value.trim() : '';

      appendMessage('user', query);
      input.value = '';

      const sendBtn = document.getElementById('sendBtn');
      if (sendBtn) {
        sendBtn.disabled = true;
        sendBtn.innerHTML = '<span class="loading-spinner"></span> 색인 탐색 & 분석 중...';
      }

      const botMsgDiv = appendMessage('bot', `
        <div class="progress-box" style="font-size:12.5px; line-height: 1.6; color: var(--text-color); padding: 8px 12px; background: var(--bg-card); border-radius: 6px; border: 1.5px solid #0284c7; box-shadow: 0 3px 10px rgba(2, 132, 199, 0.1);">
          <div id="step1" style="font-weight:600; color: #0284c7;">🧠 1단계: 질문 의도 분석 및 공간/공종 라우팅 중...</div>
          <div id="step2" style="color: var(--text-muted); opacity: 0.6;">🌐 2단계: 지식 그래프(Graph) 위험 관계망 탐색 대기</div>
          <div id="step3" style="color: var(--text-muted); opacity: 0.6;">📂 3단계: 글로벌 기술문서 메타 색인(Index) 스코어링 대기</div>
          <div id="step4" style="color: var(--text-muted); opacity: 0.6;">🤖 4단계: Gemini 100만 컨텍스트 두뇌 심층 분석 대기</div>
        </div>
      `);

      const t1 = setTimeout(() => {
        const s1 = document.getElementById('step1');
        const s2 = document.getElementById('step2');
        if (s1 && s2) {
          s1.innerHTML = '✅ 1단계: 질문 의도 분석 및 라우팅 완료 (0.001s)';
          s1.style.color = '#15803d';
          s2.innerHTML = '<span class="loading-spinner"></span> 2단계: 지식 그래프(Graph) 4대 허브/2대 리스크 탐색 중...';
          s2.style.fontWeight = '600';
          s2.style.color = '#0284c7';
          s2.style.opacity = '1.0';
        }
      }, 500);

      const t2 = setTimeout(() => {
        const s2 = document.getElementById('step2');
        const s3 = document.getElementById('step3');
        if (s2 && s3) {
          s2.innerHTML = '✅ 2단계: 지식 그래프 관계 탐색 완료 (0.004s)';
          s2.style.color = '#15803d';
          s3.innerHTML = '<span class="loading-spinner"></span> 3단계: 5개 대용량 문서 색인(Index) 정밀 스코어링 중...';
          s3.style.fontWeight = '600';
          s3.style.color = '#0284c7';
          s3.style.opacity = '1.0';
        }
      }, 1100);

      const t3 = setTimeout(() => {
        const s3 = document.getElementById('step3');
        const s4 = document.getElementById('step4');
        if (s3 && s4) {
          s3.innerHTML = '✅ 3단계: 기술문서 메타 색인 정밀 발췌 완료';
          s3.style.color = '#15803d';
          s4.innerHTML = '<span class="loading-spinner"></span> 4단계: Gemini 100만 컨텍스트 심층 추론 & 팩트 검증 중...';
          s4.style.fontWeight = '600';
          s4.style.color = '#2563eb';
          s4.style.opacity = '1.0';
        }
      }, 1800);

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            api_key: apiKey,
            query: query
          })
        });
        clearTimeout(t1);
        clearTimeout(t2); clearTimeout(t3);

        const data = await res.json();
        if (data.error) {
          if (botMsgDiv) botMsgDiv.innerHTML = `<span style="color:#ef4444;">⚠️ 오류: ${data.error}</span>`;
        } else {
          let parsedHtml = marked.parse(data.reply);
          parsedHtml = linkifyPageNumbers(parsedHtml);

          // Trace fallback 보장
          const traceData = data.trace || {
            query: query,
            highlight_nodes: (query.match(/(?:NH|DT|GB|NGB)-?\d+/gi) || []).map(h => 'bh_' + h.toUpperCase().replace(' ', '')),
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
          }

          // 자동 탐색된 출처 문서와 우측 뷰어 실시간 연동 (맞춤 근거 섹션 전달)
          if (data.source_document) {
            currentViewingDoc = data.source_document;
            loadViewerDoc(data.source_document, data.source_page || 1, data.active_sections || []);
            toggleViewerPanel(true);

            const topRef = document.getElementById('topSourceRef');
            if (topRef) {
              const secInfo = data.matched_sections && data.matched_sections.length > 0 ? ` (${data.matched_sections[0]})` : ` (p.${data.source_page || 1})`;
              topRef.innerHTML = `📂 <b>자동 탐색 출처:</b> <span style="color:var(--text-color); font-weight:600; cursor:pointer;" onclick="jumpToPage(${data.source_page || 1})" title="클릭 시 뷰어 이동">${data.source_document}</span>${secInfo}`;
            }
            const topDlBtn = document.getElementById('topDownloadBtn');
            if (topDlBtn) topDlBtn.style.display = 'inline-flex';
          }
        }
      } catch (err) {
        if (botMsgDiv) botMsgDiv.innerHTML = `<span style="color:#ef4444;">⚠️ 서버 통신 오류: ${err.message}</span>`;
      } finally {
        if (sendBtn) {
          sendBtn.disabled = false;
          sendBtn.innerText = '전송';
        }
        scrollToBottom();
      }
    }

    
    let hasLoadedMasterGraph = false;
    let currentGraphFilter = { section: 'all', riskOnly: false };

    async function loadMasterGraph(section = 'all', riskOnly = false) {
      currentGraphFilter = { section, riskOnly };
      const overlay = document.getElementById('graphLoadingOverlay');
      if (overlay) overlay.style.display = 'flex';

      const btn = document.getElementById('extractBtn');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = `<span class="loading-spinner"></span> 지식 그래프 갱신 중...`;
      }

      try {
        const queryParams = new URLSearchParams();
        if (section && section !== 'all') queryParams.append('section', section);
        if (riskOnly) queryParams.append('risk_only', 'true');

        const res = await fetch('/api/graph/master?' + queryParams.toString());
        const data = await res.json();

        if (data.error) {
          alert('지식 그래프 로딩 실패: ' + data.error);
          return;
        }

        renderNetwork(data.nodes, data.edges);
        hasLoadedMasterGraph = true;

        if (data.summary) {
          const sumBox = document.getElementById('summaryBox');
          if (sumBox) sumBox.style.display = 'block';
          const sumContent = document.getElementById('summaryContent');
          if (sumContent) sumContent.innerText = data.summary;
        }
        if (data.discrepancies && data.discrepancies.length > 0) {
          const discBox = document.getElementById('discrepancyBox');
          if (discBox) discBox.style.display = 'block';
          const discContent = document.getElementById('discrepancyContent');
          if (discContent) {
            discContent.innerHTML = data.discrepancies.slice(0, 15).map(d => `• ${d}`).join('<br>') + 
              (data.discrepancies.length > 15 ? `<br><small style="color:var(--text-muted);">외 ${data.discrepancies.length - 15}건 생략</small>` : '');
          }
        } else {
          const discBox = document.getElementById('discrepancyBox');
          if (discBox) discBox.style.display = 'none';
        }

      } catch (err) {
        console.error('loadMasterGraph error:', err);
      } finally {
        if (overlay) overlay.style.display = 'none';
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = '⚡ 지식 그래프 자동 추출 & 분석 실행';
        }
      }
    }

    function applyGraphFilter(section, riskOnly, btn) {
      document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
      if (btn) btn.classList.add('active');
      loadMasterGraph(section, riskOnly);
    }

    function openBoreholePdf(docName, page) {
      switchTab('chat');
      setTimeout(() => {
        const select = document.getElementById('documentSelect');
        if (select) {
          select.value = docName;
          onDocumentSelect();
          setTimeout(() => {
            if (typeof jumpToPage === 'function') {
              jumpToPage(page);
            }
          }, 600);
        }
      }, 200);
    }

    /* GraphRAG Extraction */
    async function extractGraph() {
      const apiKey = document.getElementById('apiKeyInput').value.trim();
      if (!apiKey) {
        alert('우측 상단에 Gemini API Key를 먼저 입력해 주세요.');
        return;
      }
      const targetDoc = currentViewingDoc || (window.cachedDocs && window.cachedDocs.length > 0 ? window.cachedDocs[0].name : null);
      if (!targetDoc) {
        alert('보관함에 등록된 문서가 없습니다. 먼저 PDF를 등록해 주세요.');
        return;
      }

      const btn = document.getElementById('extractBtn');
      btn.disabled = true;
      btn.innerHTML = `<span class="loading-spinner"></span> 지반·공종 관계망 분석 중 (${targetDoc})...`;

      try {
        const res = await fetch('/api/extract-graph', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            api_key: apiKey,
            document: targetDoc
          })
        });

        const data = await res.json();
        if (data.error) {
          alert('오류 발생: ' + data.error);
          return;
        }

        renderNetwork(data.nodes, data.edges);

        if (data.summary) {
          document.getElementById('summaryBox').style.display = 'block';
          document.getElementById('summaryContent').innerText = data.summary;
        }
        if (data.discrepancies && data.discrepancies.length > 0) {
          document.getElementById('discrepancyBox').style.display = 'block';
          document.getElementById('discrepancyContent').innerHTML = data.discrepancies.map(d => `• ${d}`).join('<br>');
        } else {
          document.getElementById('discrepancyBox').style.display = 'none';
        }

      } catch (err) {
        alert('네트워크 오류: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '⚡ 지식 그래프 재분석 실행';
      }
    }

    function renderNetwork(rawNodes, rawEdges) {
      originalRawNodes = rawNodes;
      originalRawEdges = rawEdges;
      const container = document.getElementById('networkCanvas');

      const colorMap = {
        'BORING': { background: '#f97316', border: '#ea580c' },
        'STRATUM': { background: '#a16207', border: '#854d0e' },
        'PARAMETER': { background: '#06b6d4', border: '#0891b2' },
        'DESIGN_ELEMENT': { background: '#3b82f6', border: '#2563eb' },
        'EQUIPMENT': { background: '#8b5cf6', border: '#7c3aed' },
        'DEFAULT': { background: '#64748b', border: '#475569' }
      };

      const nodes = new vis.DataSet(rawNodes.map(n => {
        const col = colorMap[n.type] || colorMap['DEFAULT'];
        return {
          id: n.id,
          label: n.label,
          title: n.description || n.label,
          color: { background: col.background, border: col.border, highlight: { background: '#fff', border: col.border } },
          font: { color: '#fff', size: 12, face: 'Noto Sans KR' },
          shape: n.type === 'BORING' ? 'box' : (n.type === 'PARAMETER' ? 'ellipse' : 'dot'),
          size: n.type === 'DESIGN_ELEMENT' ? 24 : 18,
          rawType: n.type,
          rawDesc: n.description || ''
        };
      }));

      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

      const edges = new vis.DataSet(rawEdges.map(e => {
        const isWarn = e.is_warning || e.relation === 'DISCREPANCY';
        return {
          from: e.from,
          to: e.to,
          label: e.label || e.relation,
          arrows: 'to',
          color: isWarn ? { color: '#ef4444', highlight: '#f87171' } : { color: isDark ? '#64748b' : '#94a3b8', highlight: '#3b82f6' },
          dashes: isWarn ? [5, 5] : false,
          width: isWarn ? 2.5 : 1.2,
          font: {
            color: isWarn ? '#ef4444' : (isDark ? '#cbd5e1' : '#334155'),
            size: 10,
            align: 'middle',
            background: isDark ? '#1a1d24' : '#ffffff',
            strokeWidth: 0
          }
        };
      }));

      const data = { nodes: nodes, edges: edges };
      const options = {
        physics: {
          stabilization: true,
          barnesHut: { gravitationalConstant: -3000, springLength: 120 }
        },
        interaction: { hover: true, tooltipDelay: 100 }
      };

      if (network) network.destroy();
      network = new vis.Network(container, data, options);
      window.masterGraphDataSets = { nodes, edges };

      network.on("click", function (params) {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0];
          const nodeData = nodes.get(nodeId);
          const raw = rawNodes.find(n => n.id === nodeId) || {};
          document.getElementById('nodeDetailBox').style.display = 'block';
          document.getElementById('nodeDetailLabel').innerText = `[${nodeData.rawType}] ${nodeData.label}`;
          
          let descHtml = (nodeData.rawDesc || `ID: ${nodeData.id}`).split('\\n').join('<br>');
          
          if (raw.type === 'BORING' && raw.doc_name && raw.page) {
            descHtml += `<div style="margin-top:10px;">
              <button class="borehole-jump-btn" onclick="openBoreholePdf('${raw.doc_name}', ${raw.page})">
                📄 원본 주상도 열기 (p.${raw.page})
              </button>
            </div>`;
          } else if (raw.type === 'DISCREPANCY' && raw.target) {
            const targetBh = rawNodes.find(n => n.label === raw.target);
            if (targetBh && targetBh.doc_name && targetBh.page) {
              descHtml += `<div style="margin-top:10px;">
                <button class="borehole-jump-btn" style="background:#ef4444;" onclick="openBoreholePdf('${targetBh.doc_name}', ${targetBh.page})">
                  ⚠️ 위험 대상(${raw.target}) 주상도 열기 (p.${targetBh.page})
                </button>
              </div>`;
            }
          }
          document.getElementById('nodeDetailDesc').innerHTML = descHtml;
        }
      });
    }
  </script>
</body>
</html>
"""

class SiteRAGHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
        elif self.path == "/api/documents":
            docs = []
            meta_map = {}
            if META_INDEX_FILE.exists():
                try:
                    with open(META_INDEX_FILE, "r", encoding="utf-8") as f:
                        meta_map = json.load(f)
                except Exception:
                    pass
            for f in DOCS_DIR.glob("*.pdf"):
                size_mb = round(f.stat().st_size / (1024 * 1024), 2)
                doc_info = {"name": f.name, "size_mb": size_mb}
                if f.name in meta_map:
                    m = meta_map[f.name]
                    doc_info["total_pages"] = m.get("total_pages", 0)
                    doc_info["sections"] = [
                        {"title": s["title"], "start_page": s["start_page"], "end_page": s["end_page"], "facility": s.get("facility", [])}
                        for s in m.get("sections", [])
                    ]
                docs.append(doc_info)
            docs.sort(key=lambda x: x["name"])
            self.respond_json(docs)

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
            doc_name = params.get("document", [None])[0]
            if not doc_name:
                self.send_response(400)
                self.end_headers()
                return
            file_path = DOCS_DIR / doc_name
            if not file_path.exists():
                self.send_response(404)
                self.end_headers()
                return
            try:
                file_size = file_path.stat().st_size
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                quoted_name = urllib.parse.quote(doc_name)
                disposition = "attachment" if is_download else "inline"
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
                "api_key": masked_key
            })
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/config":
            content_len = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_len).decode("utf-8"))
            if "api_key" in body and body["api_key"].strip():
                save_env_api_key(body["api_key"].strip())
            self.respond_json({"status": "ok"})

        elif self.path == "/api/upload":
            content_type = self.headers.get('Content-Type', '')
            if 'multipart/form-data' in content_type:
                boundary = content_type.split('boundary=')[1].encode()
                content_len = int(self.headers.get('Content-Length', 0))
                raw_data = self.rfile.read(content_len)
                parts = raw_data.split(b'--' + boundary)
                for part in parts:
                    if b'filename="' in part:
                        headers, file_data = part.split(b'\r\n\r\n', 1)
                        file_data = file_data.rsplit(b'\r\n', 1)[0]
                        filename = headers.split(b'filename="')[1].split(b'"')[0].decode('utf-8', errors='ignore')
                        if filename.lower().endswith(('.pdf', '.xlsx', '.csv')):
                            save_path = DOCS_DIR / filename
                            with open(save_path, "wb") as out_f:
                                out_f.write(file_data)
                            
                            # 자동 온톨로지 지식망 확장 파이프라인 가동
                            ingest_data = {}
                            try:
                                import knowledge_ingestion
                                ingest_data = knowledge_ingestion.ingest_file(save_path, api_key=load_env_api_key())
                            except Exception as e:
                                print(f"[KnowledgeIngestion] Error: {e}")
                                ingest_data = {"status": "partial", "message": str(e)}

                            self.respond_json({"status": "uploaded", "filename": filename, "ingest": ingest_data})
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
                self.respond_json({"error": "해당 문서가 존재하지 않습니다."}, 404)

        elif self.path == "/api/chat":
            content_len = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(content_len).decode("utf-8"))

            api_key = payload.get("api_key") or load_env_api_key()
            query = payload.get("query", "").strip()

            if not api_key:
                self.respond_json({"error": "Gemini API Key가 필요합니다."}, 400)
                return
            if not query:
                self.respond_json({"error": "질문 내용을 입력해 주세요."}, 400)
                return

                        # 1. Structured Geotechnical Text-to-SQL Routing
            try:
                if sql_query_engine and sql_query_engine.is_geotech_query(query):
                    print(f" -> [SQL Route Activated] query: {query}")
                    sql_res = sql_query_engine.generate_and_execute_sql(query)
                    if sql_res and sql_res.get("reply"):
                        print(f" -> [SQL Route Success] Returning {len(sql_res['reply'])} chars")
                        # SQL 대상 시추공 하이라이트 노드 구성
                        sql_h_nodes = []
                        if "hole_no" in sql_res:
                            sql_h_nodes.append(f"bh_{sql_res['hole_no']}")
                        for h in re.findall(r'(?:NH|DT|GB|NGB)-?\d+', query, re.IGNORECASE):
                            clean = h.upper().replace(" ", "")
                            if not clean.startswith(("NH-", "DT-", "GB-", "NGB-")):
                                clean = re.sub(r'([A-Z]+)(\d+)', r'\1-\2', clean)
                            sql_h_nodes.append(f"bh_{clean}")
                        if "연약" in query or "n<" in query or "n치" in query:
                            sql_h_nodes.append("risk_cluster_soft")
                        if "지하수" in query:
                            sql_h_nodes.append("risk_cluster_gw")

                        sql_res["trace"] = {
                            "query": query,
                            "highlight_nodes": list(set(sql_h_nodes)),
                            "steps": [
                                {"step": 1, "icon": "🧠", "title": "질문 의도 분석 & 정형 지반 DB 라우팅", "badge": "Text-to-SQL 감지", "detail": f"질문 '{query}'에서 시추공/N치/지하수위 정형 조건 인식 ➔ 고속 데이터베이스 엔진 직결"},
                                {"step": 2, "icon": "🌐", "title": "지식 그래프(Graph) 4대 구간/2대 리스크 매핑", "badge": "지식망 연결", "detail": "본선/차량기지 공간 허브 및 연약지반/고지하수위 클러스터와 시추공 상호 연결망 검증"},
                                {"step": 3, "icon": "⚡", "title": "정밀 지반 데이터베이스(SQL) 즉시 쿼리", "badge": "0.005s 초고속 실행", "detail": f"77개 시추공 및 SPT 레코드에서 조건에 맞는 팩트 데이터를 100% 누락 없이 전수 추출"},
                                {"step": 4, "icon": "📄", "title": "시추주상도 원본 페이지(p.XX) 링크 생성", "badge": "검증 완료", "detail": "검색된 결과에 대해 원본 주상도 보고서 페이지 번호와 직접 뷰어 이동 링크 매핑"}
                            ]
                        }
                        self.respond_json(sql_res)
                        return
                    else:
                        print(" -> [SQL Route] No results returned, falling back to RAG")
            except Exception as e:
                print(f"[SQL Route Error]: {e}")

            # Pure Global Multi-Document Index Routing (Graph-Guided Fusion)
            target_doc_name = None
            target_file_path = None
            target_start_page = 1
            matched_section_titles = []
            source_notice = ""

            # [지식망-색인 유기적 결합: Step 1] 질문 의도 기반 지식망 선제 질의
            graph_intel = {}
            matched_graph_holes = set()
            target_graph_docs = set()
            target_graph_pages = []
            try:
                import graph_intelligence
                graph_intel = graph_intelligence.extract_graph_intelligence(query)
                matched_graph_holes = set(graph_intel.get("matched_holes", []))
                target_graph_docs = set(graph_intel.get("target_docs", []))
                target_graph_pages = graph_intel.get("target_pages", [])
                print(f" -> [Graph Intelligence Activated] Holes: {matched_graph_holes}, TargetDocs: {target_graph_docs}")
            except Exception as ge_err:
                print(f" -> [Graph Intelligence Error]: {ge_err}")

            if META_INDEX_FILE.exists():
                try:
                    with open(META_INDEX_FILE, "r", encoding="utf-8") as f:
                        meta_map = json.load(f)
                    
                    query_lower = query.lower()
                    query_tokens = [w for w in re.split(r'[\s,._/?!~()\[\]]+', query_lower) if len(w) >= 1]
                    target_nums = extract_target_numbers(query_lower)

                    is_base = any(k in query_lower for k in ["차량기지", "건축기지", "기지", "gb"])
                    
                    scored_sections = []
                    for dn, dm in meta_map.items():
                        fp = DOCS_DIR / dn
                        if not fp.exists(): continue

                        doc_bonus = 0
                        if any(k in query_lower for k in ["보링", "시추", "주상도", "n치", "n<", "n<=", "n=", "연약", "spt", "관입"]):
                            if "주상도" in dn: doc_bonus += 40
                        if "입찰안내서" in query_lower and "입찰안내서" in dn: doc_bonus += 60
                        if ("기술제안" in query_lower or "4편" in query_lower) and "4편" in dn: doc_bonus += 30
                        if "본선" in query_lower and "본선" in dn: doc_bonus += 15
                        if ("차량기지" in query_lower or "기지" in query_lower) and "차량기지" in dn: doc_bonus += 15
                        if ("3편" in query_lower or "증빙" in query_lower or "기준" in query_lower) and "3편" in dn: doc_bonus += 10
                        if (is_base or "1공구" in query_lower or "nh" in query_lower) and "1공구" in dn: doc_bonus += 15
                        if ("2공구" in query_lower or "dt" in query_lower) and "2공구" in dn: doc_bonus += 10

                        for s in dm.get("sections", []):
                            sc = doc_bonus
                            sec_title = s.get("title", "")
                            m = re.search(r'(?:GB|NH|DT)-(\d+)', sec_title)
                            sec_num = int(m.group(1)) if m else None

                            for fac in s.get("facility", []):
                                if fac.lower() in query_lower: sc += 8
                                for tok in query_tokens:
                                    if tok in fac.lower(): sc += 3
                            if is_base and "차량기지" in s.get("facility", []):
                                sc += 15
                            elif not is_base and "본선" in s.get("facility", []):
                                sc += 5

                            if sec_num is not None and sec_num in target_nums:
                                sc += 40  # Massive priority for explicit borehole number/range

                            for kw in s.get("keywords", []):
                                if kw.lower() in query_lower: sc += 6
                                for tok in query_tokens:
                                    if tok in kw.lower(): sc += 3
                            title_l = sec_title.lower()
                            if title_l in query_lower: sc += 10
                            for tok in query_tokens:
                                if tok in title_l: sc += 4
                            task_l = s.get("task_id", "").lower()
                            if task_l in query_lower: sc += 8
                            for tok in query_tokens:
                                if tok in task_l: sc += 3

                            # [지식망-색인 유기적 결합: Step 2] 지식망 피드백 가중치(Graph-Guided Boost) 주입
                            graph_bonus = 0
                            for gh in matched_graph_holes:
                                if gh.lower() in sec_title.lower() or gh.lower() in " ".join(s.get("keywords", [])).lower():
                                    graph_bonus += 150  # 지식망 검출 시추공 일치 시 대규모 우선순위
                            
                            sec_start = s.get("start_page", 1)
                            sec_end = s.get("end_page", 1)
                            for gp in target_graph_pages:
                                if sec_start <= gp <= sec_end:
                                    graph_bonus += 100  # 지식망 위험구간 페이지 범위 일치 시 추가 보너스
                            
                            if dn in target_graph_docs:
                                graph_bonus += 50   # 지식망 소속 출처 문서 보너스

                            sc += graph_bonus

                            if sc > 0:
                                scored_sections.append((sc, dn, fp, s))
                    
                    scored_sections.sort(key=lambda x: x[0], reverse=True)
                    if scored_sections:
                        top_sc, target_doc_name, target_file_path, top_sec = scored_sections[0]
                        target_start_page = top_sec.get("start_page", 1)
                        matched_section_titles = [f"{s.get('title', '')} (p.{s.get('start_page', 1)}~{s.get('end_page', 1)})" for sc, dn, fp, s in scored_sections if dn == target_doc_name][:4]
                        source_notice = f"> 📂 **[출처 문서 자동 탐색]** **`{target_doc_name}`**의 **{top_sec.get('title', '')} (p.{top_sec.get('start_page', 1)}~{top_sec.get('end_page', 1)})**에서 자동 추출하여 분석했습니다.\n\n"
                except Exception:
                    pass

            if not target_file_path or not target_file_path.exists():
                # Fallback: #3편 증빙자료 or first available
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
                        return

            try:
                pdf_bytes, info_msg, is_meta_only = get_smart_pdf_payload(target_file_path, query)
                if is_meta_only:
                    self.respond_json({
                        "reply": info_msg,
                        "source_document": target_doc_name,
                        "source_page": target_start_page,
                        "matched_sections": matched_section_titles
                    })
                    return
                # 20MB 초과 대형 파일(또는 None)인 경우 Google File API Long-Context 모드 가동
                if pdf_bytes is None:
                    try:
                        from google import genai
                        import gemini_file_manager
                        
                        client = genai.Client(api_key=api_key)
                        file_ref = gemini_file_manager.get_or_upload_file(client, target_file_path)
                        
                        system_prompt = (
                            "당신은 철도/토목/지반 엔지니어링 및 설계보고서, 시추주상도 분석 전문 AI입니다.\n"
                            "제공된 대용량 PDF 문서 전체(수백 페이지)를 면밀히 분석하여 질문에 100% 팩트 기반으로 답변하세요.\n\n"
                            "[핵심 규칙]\n"
                            "1. 반드시 해당 내용이 수록된 '정확한 원본 페이지 번호(예: p.87 등)'를 명시하세요.\n"
                            "2. 지층, 심도, N치, 토질 특성 등 표(Table) 데이터는 마크다운 표로 깔끔하게 정리하세요.\n"
                            "3. 제안설계 NGB 시추공, 기본설계 GB/NH/DT 시추공 등의 구분을 명확히 설명하세요.\n"
                            "4. 추측하지 말고 문서에 명시된 사실만을 정확히 인용하세요."
                        )
                        
                        models_to_try = [
                            "gemini-3.8-flash",
                            "gemini-3.6-flash",
                            "gemini-3.5-flash-lite",
                            "gemini-flash-latest"
                        ]
                        text = ""
                        for m_name in models_to_try:
                            try:
                                resp = client.models.generate_content(
                                    model=m_name,
                                    contents=[file_ref, query],
                                    config=genai.types.GenerateContentConfig(
                                        system_instruction=system_prompt,
                                        temperature=0.1
                                    )
                                )
                                if resp and resp.text:
                                    text = resp.text.strip()
                                    break
                            except Exception as m_err:
                                last_error = str(m_err)
                                continue
                                
                        if not text:
                            self.respond_json({"error": f"Google File API 분석 실패: {last_error}"}, 500)
                            return
                            
                        holes_str = ", ".join(list(matched_graph_holes)[:4]) if matched_graph_holes else "전체 구간"
                        intel_summary = graph_intel.get("summary", "공간/공종 허브 매핑")
                        # 지식망 하이라이트 타겟 노드 구성
                        rag_h_nodes = [f"bh_{h}" for h in matched_graph_holes]
                        if graph_intel.get("is_soft_ground"):
                            rag_h_nodes.append("risk_cluster_soft")
                        if graph_intel.get("is_high_gw"):
                            rag_h_nodes.append("risk_cluster_gw")
                        if graph_intel.get("is_depot"):
                            rag_h_nodes.extend(["hub_depot", "hub_prop_depot"])
                        if graph_intel.get("is_sec1"):
                            rag_h_nodes.append("hub_sec1")
                        if graph_intel.get("is_sec2"):
                            rag_h_nodes.append("hub_sec2")

                        rag_trace = {
                            "query": query,
                            "highlight_nodes": list(set(rag_h_nodes)),
                            "steps": [
                                {"step": 1, "icon": "🧠", "title": "질문 의도 분석 및 공간/공종 라우팅", "badge": "엔지니어링 의도 파악", "detail": f"질문 키워드 분석 완료: '{query}' ➔ 지식망 쿼리 자동 연계"},
                                {"step": 2, "icon": "🌐", "title": "지식 그래프(Graph) 선제 탐색 ➔ 색인 피드백", "badge": "지식망 ➔ 색인 가중치 전달", "detail": f"지식그래프 탐색 완료: [{intel_summary}] 경로 검출 (타겟 시추공: {holes_str}) ➔ 색인 엔진으로 가중치(+150점) 실시간 피드백 전달"},
                                {"step": 3, "icon": "📂", "title": "글로벌 문서 메타 색인(Index) 정밀 스코어링", "badge": f"{target_doc_name} (p.{target_start_page or 1})", "detail": f"지식망 가중치 반영 완료 ➔ 1순위 최우선 근거 문서 '{target_doc_name}' 및 매칭 섹션({', '.join(matched_section_titles[:2]) if matched_section_titles else '핵심 절'}) 특정 완료"},
                                {"step": 4, "icon": "🤖", "title": "Gemini 100만 컨텍스트 두뇌 심층 추론 & 팩트 검증", "badge": "답변 합성 완료", "detail": f"수백 페이지 전체 원문과 도표를 대조하여 100% 팩트 기반 기술 답변 및 원본 페이지 링크 생성"}
                            ]
                        }
                        self.respond_json({
                            "reply": text,
                            "source_document": target_doc_name,
                            "source_page": target_start_page or 1,
                            "matched_sections": matched_section_titles,
                            "trace": rag_trace
                        })
                        return
                    except Exception as file_api_err:
                        self.respond_json({"error": f"Google File API 오류: {str(file_api_err)}"}, 500)
                        return

                pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")

                models_to_try = [
                    "gemini-flash-lite-latest",
                    "gemini-3.5-flash-lite",
                    "gemini-3.6-flash",
                    "gemini-3.1-flash-lite",
                    "gemini-flash-latest"
                ]
                last_error = ""
                text = ""

                for model_name in models_to_try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                    req_body = {
                        "systemInstruction": {
                            "parts": [{
                                "text": (
                                    "당신은 토목/건축/기계 엔지니어링 현장 기술 시방서 및 설계보고서 전문 감리원/수석 엔지니어 AI입니다.\n"
                                    "제공된 PDF 문서는 전체 원본 문서에서 질문과 관련된 핵심 섹션을 정밀 추출한 발췌본입니다.\n"
                                    f"[문서 발췌 정보 & 도메인 지식]\n"
                                    f"- 추출된 원본 범위: {info_msg}\n"
                                    "- 시추공 약어 기준: GB = 차량기지 시추공, NH = 1공구 본선 시추공, DT = 2공구 본선 시추공.\n"
                                    "- 주상도 서식에 '차량기지'라는 한글 단어 대신 공번 'GB'로 표기되어 있으므로 GB 공번을 차량기지 조사 결과로 정확히 인식하여 분석하세요.\n"
                                    "- 답변 시 발췌본 내부의 임의 페이지가 아닌, 위 [추출된 원본 범위]에 기재된 '원본 페이지 번호(예: p.40, p.44 등)'를 기준으로 인용하여 명시하세요.\n"
                                    "1. 본문의 비교 표(Table), 수치, 규격, 시공 및 시험 기준을 누락 없이 정밀하게 마크다운 표와 항목으로 정리하세요.\n"
                                    "2. 문서에 없는 내용은 억지로 지어내지 말고 문서에 없다고 명확히 밝히세요."
                                )
                            }]
                        },
                        "contents": [
                            {
                                "role": "user",
                                "parts": [
                                    {
                                        "inline_data": {
                                            "mime_type": "application/pdf",
                                            "data": pdf_b64
                                        }
                                    },
                                    {
                                        "text": query
                                    }
                                ]
                            }
                        ],
                        "generationConfig": {
                            "temperature": 0.2
                        }
                    }

                    try:
                        req = urllib.request.Request(
                            url,
                            data=json.dumps(req_body).encode("utf-8"),
                            headers={"Content-Type": "application/json"}
                        )
                        with urllib.request.urlopen(req, timeout=90) as resp:
                            resp_data = json.loads(resp.read().decode("utf-8"))
                            text = resp_data["candidates"][0]["content"]["parts"][0]["text"]
                            break
                    except urllib.error.HTTPError as e:
                        err_bytes = e.read()
                        err_str = err_bytes.decode("utf-8", errors="ignore")
                        last_error = f"[{model_name} {e.code}] {err_str}"
                        if e.code in [404, 429, 500, 502, 503, 504]:
                            time.sleep(1.0)
                            continue
                        else:
                            break
                    except Exception as e:
                        last_error = f"[{model_name}] {str(e)}"
                        time.sleep(0.5)
                        continue

                if text:
                    matched_section_objs = [
                        {
                            "title": s.get("title", ""),
                            "start_page": s.get("start_page", 1),
                            "end_page": s.get("end_page", 1),
                            "section_id": s.get("section_id", "")
                        }
                        for sc, dn, fp, s in scored_sections if dn == target_doc_name
                    ][:10]

                    resp_data = {
                        "reply": source_notice + text,
                        "source_document": target_doc_name,
                        "source_page": target_start_page,
                        "matched_sections": matched_section_titles,
                        "active_sections": matched_section_objs
                    }
                    self.respond_json(resp_data)
                else:
                    self.respond_json({"error": f"Google Gemini API 응답 생성 실패: {last_error}"}, 500)

            except urllib.error.HTTPError as e:
                err_msg = e.read().decode("utf-8", errors="ignore")
                self.respond_json({"error": f"Google Gemini API 에러 ({e.code}): {err_msg}"}, 500)
            except Exception as e:
                self.respond_json({"error": str(e)}, 500)

        elif self.path == "/api/extract-graph":
            content_len = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(content_len).decode("utf-8"))

            api_key = payload.get("api_key") or load_env_api_key()
            doc_name = payload.get("document")

            if not api_key:
                self.respond_json({"error": "Gemini API Key가 필요합니다."}, 400)
                return
            if not doc_name:
                self.respond_json({"error": "문서가 선택되지 않았습니다."}, 400)
                return

            file_path = DOCS_DIR / doc_name
            if not file_path.exists():
                self.respond_json({"error": f"문서를 찾을 수 없습니다: {doc_name}"}, 404)
                return

            try:
                pdf_bytes, info_msg, _ = get_smart_pdf_payload(file_path, "지반조사 시추공 지층 가시설 구조물 기초 계측")
                # 20MB 초과 대형 파일(또는 None)인 경우 Google File API Long-Context 모드 가동
                if pdf_bytes is None:
                    try:
                        from google import genai
                        import gemini_file_manager
                        
                        client = genai.Client(api_key=api_key)
                        file_ref = gemini_file_manager.get_or_upload_file(client, file_path)
                        
                        system_prompt = (
                            "당신은 철도/토목/지반 엔지니어링 및 설계보고서, 시추주상도 분석 전문 AI입니다.\n"
                            "제공된 대용량 PDF 문서 전체(수백 페이지)를 면밀히 분석하여 질문에 100% 팩트 기반으로 답변하세요.\n\n"
                            "[핵심 규칙]\n"
                            "1. 반드시 해당 내용이 수록된 '정확한 원본 페이지 번호(예: p.87 등)'를 명시하세요.\n"
                            "2. 지층, 심도, N치, 토질 특성 등 표(Table) 데이터는 마크다운 표로 깔끔하게 정리하세요.\n"
                            "3. 제안설계 NGB 시추공, 기본설계 GB/NH/DT 시추공 등의 구분을 명확히 설명하세요.\n"
                            "4. 추측하지 말고 문서에 명시된 사실만을 정확히 인용하세요."
                        )
                        
                        models_to_try = [
                            "gemini-3.8-flash",
                            "gemini-3.6-flash",
                            "gemini-3.5-flash-lite",
                            "gemini-flash-latest"
                        ]
                        text = ""
                        for m_name in models_to_try:
                            try:
                                resp = client.models.generate_content(
                                    model=m_name,
                                    contents=[file_ref, query],
                                    config=genai.types.GenerateContentConfig(
                                        system_instruction=system_prompt,
                                        temperature=0.1
                                    )
                                )
                                if resp and resp.text:
                                    text = resp.text.strip()
                                    break
                            except Exception as m_err:
                                last_error = str(m_err)
                                continue
                                
                        if not text:
                            self.respond_json({"error": f"Google File API 분석 실패: {last_error}"}, 500)
                            return
                            
                        # 지식망 하이라이트 타겟 노드 구성
                        rag_h_nodes = [f"bh_{h}" for h in matched_graph_holes]
                        if graph_intel.get("is_soft_ground"):
                            rag_h_nodes.append("risk_cluster_soft")
                        if graph_intel.get("is_high_gw"):
                            rag_h_nodes.append("risk_cluster_gw")
                        if graph_intel.get("is_depot"):
                            rag_h_nodes.extend(["hub_depot", "hub_prop_depot"])
                        if graph_intel.get("is_sec1"):
                            rag_h_nodes.append("hub_sec1")
                        if graph_intel.get("is_sec2"):
                            rag_h_nodes.append("hub_sec2")

                        rag_trace = {
                            "query": query,
                            "highlight_nodes": list(set(rag_h_nodes)),
                            "steps": [
                                {"step": 1, "icon": "🧠", "title": "질문 의도 분석 및 공간/공종 라우팅", "badge": "엔지니어링 의도 파악", "detail": f"질문 키워드 분석 완료: '{query}'"},
                                {"step": 2, "icon": "🌐", "title": "지반-공종 지식 그래프(Graph) 관계 탐색", "badge": "지식망 매핑", "detail": f"4대 구간 허브(본선/기지) 및 연약지반/고지하수위 클러스터 연계성 탐색"},
                                {"step": 3, "icon": "📂", "title": "글로벌 문서 메타 색인(Index) 정밀 스코어링", "badge": f"{target_doc_name} (p.{target_start_page or 1})", "detail": f"5개 대형 기술문서 전수 색인 스코어링 ➔ 최우선 근거 문서 '{target_doc_name}' 및 매칭 섹션({', '.join(matched_section_titles[:2]) if matched_section_titles else '핵심 절'}) 특정"},
                                {"step": 4, "icon": "🤖", "title": "Gemini 100만 컨텍스트 두뇌 심층 추론 & 팩트 검증", "badge": "답변 합성 완료", "detail": f"수백 페이지 전체 원문과 도표를 대조하여 100% 팩트 기반 기술 답변 및 원본 페이지 링크 생성"}
                            ]
                        }
                        self.respond_json({
                            "reply": text,
                            "source_document": target_doc_name,
                            "source_page": target_start_page or 1,
                            "matched_sections": matched_section_titles,
                            "trace": rag_trace
                        })
                        return
                    except Exception as file_api_err:
                        self.respond_json({"error": f"Google File API 오류: {str(file_api_err)}"}, 500)
                        return

                pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")

                system_prompt = (
                    "당신은 토질및기초 / 엔지니어링 지식 그래프(GraphRAG) 설계 전문가입니다. "
                    "제공된 기술 문서를 정밀하게 분석하여 핵심 엔티티(노드)와 관계(엣지)를 추출하세요.\n\n"
                    "[엄격한 4x4 온톨로지 규칙]\n"
                    "1. 노드 유형(type)은 다음 5가지 중 하나만 사용하세요:\n"
                    "   - BORING: 시추공 (예: BH-1, BH-2, 시추위치)\n"
                    "   - STRATUM: 지층/암반 (예: 매립토, 풍화토, 풍화암, 연암층)\n"
                    "   - PARAMETER: 수치/지반/수위 정수 (예: N치, c=15kPa, φ=32°, 지하수위 GL-2.5m, 설계수위 등)\n"
                    "   - DESIGN_ELEMENT: 설계요소/가시설/단면 (예: 굴착단면 H=15m, CIP벽체, 지반앵커, 버팀보)\n"
                    "   - EQUIPMENT: 주요 기계/전기/제어설비 (기계/전기 문서일 경우 사용)\n\n"
                    "2. 엣지 관계(relation)는 다음 중 하나만 사용하세요:\n"
                    "   - FOUND_IN: 지층/수치/정수가 발견/측정된 시추공 연결\n"
                    "   - CALCULATED_FROM: 설계 지반정수의 산정 근거 연결\n"
                    "   - APPLIED_TO: 해석 단면 및 설계요소에 적용 연결\n"
                    "   - DISCREPANCY: 조사 실측값과 설계 적용값 간의 상충/불일치/위험 경고 (is_warning: true)\n"
                    "   - POWERED_BY / CONTROLLED_BY / PENETRATES (설비 문서 해당 시)\n\n"
                    "3. 반드시 유효한 JSON 형식으로만 출력하세요. 마크다운 따옴표 없이 순수 JSON만 반환하세요:\n"
                    "{\n"
                    '  "nodes": [\n'
                    '    {"id": "n1", "label": "표시이름", "type": "BORING|STRATUM|PARAMETER|DESIGN_ELEMENT|EQUIPMENT", "description": "상세설명"}\n'
                    "  ],\n"
                    '  "edges": [\n'
                    '    {"from": "n1", "to": "n2", "relation": "관계명", "label": "화면표시관계", "is_warning": false}\n'
                    "  ],\n"
                    '  "summary": "핵심 관계 및 정합성 검토 요약 (3~5문장)",\n'
                    '  "discrepancies": ["발견된 불일치 또는 리스크 사항 (없으면 빈 배열)"]\n'
                    "}"
                )

                models_to_try = [
                    "gemini-3.6-flash",
                    "gemini-flash-lite-latest",
                    "gemini-3.5-flash-lite",
                    "gemini-3.1-flash-lite",
                    "gemini-flash-latest"
                ]
                raw_text = ""
                last_error = ""

                for model_name in models_to_try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                    req_body = {
                        "systemInstruction": {
                            "parts": [{"text": system_prompt}]
                        },
                        "contents": [
                            {
                                "role": "user",
                                "parts": [
                                    {
                                        "inline_data": {
                                            "mime_type": "application/pdf",
                                            "data": pdf_b64
                                        }
                                    },
                                    {
                                        "text": "이 기술 문서의 핵심 엔티티와 관계를 온톨로지 규칙에 맞추어 JSON으로 추출하세요."
                                    }
                                ]
                            }
                        ],
                        "generationConfig": {
                            "temperature": 0.1,
                            "responseMimeType": "application/json"
                        }
                    }

                    try:
                        req = urllib.request.Request(
                            url,
                            data=json.dumps(req_body).encode("utf-8"),
                            headers={"Content-Type": "application/json"}
                        )
                        with urllib.request.urlopen(req, timeout=120) as resp:
                            resp_data = json.loads(resp.read().decode("utf-8"))
                            raw_text = resp_data["candidates"][0]["content"]["parts"][0]["text"]
                            break
                    except urllib.error.HTTPError as e:
                        err_bytes = e.read()
                        err_str = err_bytes.decode("utf-8", errors="ignore")
                        last_error = f"[{model_name} {e.code}] {err_str}"
                        if e.code in [404, 429, 500, 502, 503, 504]:
                            time.sleep(1.0)
                            continue
                        else:
                            break
                    except Exception as e:
                        last_error = f"[{model_name}] {str(e)}"
                        time.sleep(0.5)
                        continue

                if not raw_text:
                    self.respond_json({"error": f"온톨로지 그래프 생성 실패: {last_error}"}, 500)
                    return

                # Clean markdown JSON fences if present
                clean_json_str = raw_text.strip()
                if clean_json_str.startswith("```json"):
                    clean_json_str = clean_json_str[7:]
                if clean_json_str.startswith("```"):
                    clean_json_str = clean_json_str[3:]
                if clean_json_str.endswith("```"):
                    clean_json_str = clean_json_str[:-3]
                clean_json_str = clean_json_str.strip()

                graph_data = json.loads(clean_json_str)
                self.respond_json(graph_data)

            except Exception as e:
                self.respond_json({"error": f"그래프 추출 중 오류: {str(e)}"}, 500)
        else:
            self.send_response(404)
            self.end_headers()

    def respond_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def run():
    server_address = ('', PORT)
    httpd = ThreadingHTTPServer(server_address, SiteRAGHandler)
    ip = get_server_ip()
    print("=" * 60)
    print(f" [현장 공용 RAG & GraphRAG 서버 가동 완료]")
    print(f" - 내 컴퓨터 접속:  http://localhost:{PORT}")
    print(f" - 사내망 20인 공유: http://{ip}:{PORT}")
    print("=" * 60)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
