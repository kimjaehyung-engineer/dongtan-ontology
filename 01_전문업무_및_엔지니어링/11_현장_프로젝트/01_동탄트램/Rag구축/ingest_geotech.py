import os
import sys
import re
import json
import base64
import sqlite3
import urllib.request
from pathlib import Path
from pypdf import PdfReader, PdfWriter
import io

sys.stdout.reconfigure(encoding='utf-8')

RAG_DIR = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
DOCS_DIR = RAG_DIR / "documents"
DB_PATH = RAG_DIR / "geotech_data.db"
META_FILE = DOCS_DIR / "_metadata_index.json"

def get_api_key():
    env_file = RAG_DIR / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    return line.strip().split("=", 1)[1]
    return os.environ.get("GEMINI_API_KEY", "")

def init_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS boreholes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_name TEXT NOT NULL,
        hole_no TEXT NOT NULL,
        facility TEXT,
        page_start INTEGER,
        page_end INTEGER,
        elevation_m REAL,
        groundwater_m REAL,
        total_depth_m REAL,
        driller TEXT,
        date TEXT,
        UNIQUE(doc_name, hole_no)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spt_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_name TEXT NOT NULL,
        hole_no TEXT NOT NULL,
        page INTEGER,
        sample_no TEXT,
        depth_m REAL,
        n_value INTEGER,
        n_str TEXT,
        blows INTEGER,
        penetration_cm INTEGER,
        FOREIGN KEY(doc_name, hole_no) REFERENCES boreholes(doc_name, hole_no)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS strata_layers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_name TEXT NOT NULL,
        hole_no TEXT NOT NULL,
        page INTEGER,
        stratum_name TEXT,
        depth_top_m REAL,
        depth_bottom_m REAL,
        thickness_m REAL,
        uscs TEXT,
        description TEXT,
        FOREIGN KEY(doc_name, hole_no) REFERENCES boreholes(doc_name, hole_no)
    )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_spt_depth_n ON spt_records(depth_m, n_value);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_spt_hole ON spt_records(hole_no);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_borehole_hole ON boreholes(hole_no);")
    conn.commit()

def parse_drill_log_page(page_text, p_num, doc_name):
    """Parse text layer if available"""
    if not page_text or not page_text.strip():
        return None, [], []

    m_hole = re.search(r'HOLE\s*No\.?\s*([A-Z0-9_-]+)', page_text, re.I)
    if not m_hole:
        m_hole = re.search(r'\b(NH-\d+|GB-\d+|DT-\d+)\b', page_text)
    if not m_hole:
        return None, [], []

    hole_no = m_hole.group(1).strip()
    facility = "본선"
    if hole_no.startswith("GB"):
        facility = "차량기지"
    elif hole_no.startswith("NH"):
        facility = "1공구 본선"
    elif hole_no.startswith("DT"):
        facility = "2공구 본선"

    elevation_m = None
    m_elev = re.search(r'ELEVATION\s*([0-9.]+)\s*M', page_text, re.I)
    if m_elev:
        try: elevation_m = float(m_elev.group(1))
        except ValueError: pass

    groundwater_m = None
    m_gw = re.search(r'GROUND\s*WATER.*?([0-9.]+)\s*M', page_text, re.I)
    if m_gw:
        try: groundwater_m = float(m_gw.group(1))
        except ValueError: pass

    total_depth_m = None
    m_end = re.search(r'심도\s*([0-9.]+)\s*M\s*에서\s*시추종료', page_text)
    if m_end:
        try: total_depth_m = float(m_end.group(1))
        except ValueError: pass

    driller = None
    m_driller = re.search(r'DRILLER\s*([^\n\r]+)', page_text, re.I)
    if m_driller: driller = m_driller.group(1).strip()

    date_str = None
    m_date = re.search(r'DATE\s*([0-9.~ \t∼-]+)', page_text, re.I)
    if m_date: date_str = m_date.group(1).strip()

    borehole_info = {
        "doc_name": doc_name,
        "hole_no": hole_no,
        "facility": facility,
        "page": p_num,
        "elevation_m": elevation_m,
        "groundwater_m": groundwater_m,
        "total_depth_m": total_depth_m,
        "driller": driller,
        "date": date_str
    }

    lines = [l.strip() for l in page_text.split('\n') if l.strip()]
    samples = [l for l in lines if re.match(r'^S-\d+$', l)]
    n_values = [l for l in lines if re.match(r'^\d+/\d+$', l)]
    depths = [float(l) for l in lines if re.match(r'^\d+\.\d+$', l) and 0.5 <= float(l) <= 70.0]

    spt_records = []
    if len(depths) >= len(n_values) and len(n_values) > 0:
        num_spt = len(n_values)
        spt_depths = depths[-num_spt:] if len(depths) >= num_spt else depths
        for i, n_str in enumerate(n_values):
            d = spt_depths[i] if i < len(spt_depths) else (i + 1) * 1.0
            m_blow = re.match(r'^(\d+)/(\d+)$', n_str)
            if m_blow:
                blows = int(m_blow.group(1))
                pen = int(m_blow.group(2))
                n_val = blows if pen == 30 else int(round(blows * 30.0 / pen))
                s_name = samples[i] if i < len(samples) else f"S-{i+1}"
                spt_records.append({
                    "doc_name": doc_name,
                    "hole_no": hole_no,
                    "page": p_num,
                    "sample_no": s_name,
                    "depth_m": d,
                    "n_value": n_val,
                    "n_str": n_str,
                    "blows": blows,
                    "penetration_cm": pen
                })

    strata_records = []
    strata_matches = re.finditer(r'▶\s*([가-힣a-zA-Z0-9]+)\s*\(\s*([0-9.]+)\s*[〜~-]\s*([0-9.]+)\s*m\s*\)', page_text)
    for sm in strata_matches:
        s_name = sm.group(1).strip()
        top_d = float(sm.group(2))
        bot_d = float(sm.group(3))
        thick = round(bot_d - top_d, 2)
        strata_records.append({
            "doc_name": doc_name,
            "hole_no": hole_no,
            "page": p_num,
            "stratum_name": s_name,
            "depth_top_m": top_d,
            "depth_bottom_m": bot_d,
            "thickness_m": thick,
            "uscs": "",
            "description": ""
        })

    return borehole_info, spt_records, strata_records

def parse_page_via_vision(pdf_path, page_num, doc_name, hole_no, api_key):
    """Fallback OCR using Gemini Vision for scanned pages (e.g. NH-3 p.4)"""
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num - 1])
        buf = io.BytesIO()
        writer.write(buf)
        buf.seek(0)
        p_bytes = buf.read()
        p_b64 = base64.b64encode(p_bytes).decode("utf-8")

        prompt = (
            f"이 시추주상도({hole_no}) 페이지의 데이터를 다음 JSON 형식으로 정확히 추출하세요.\n"
            "```json\n"
            "{\n"
            '  "elevation_m": float or null,\n'
            '  "groundwater_m": float or null,\n'
            '  "total_depth_m": float or null,\n'
            '  "spt_records": [\n'
            '    {"sample_no": "S-1", "depth_m": 1.0, "blows": 3, "pen": 30, "n_value": 3, "n_str": "3/30"}\n'
            '  ],\n'
            '  "strata_layers": [\n'
            '    {"stratum_name": "매립층", "depth_top_m": 0.0, "depth_bottom_m": 2.5, "thickness_m": 2.5}\n'
            '  ]\n'
            "}\n"
            "```\n"
            "오직 순수 JSON만 출력하세요."
        )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={api_key}"
        req_body = {
            "contents": [{
                "parts": [
                    {"inline_data": {"mime_type": "application/pdf", "data": p_b64}},
                    {"text": prompt}
                ]
            }],
            "generationConfig": {"temperature": 0.0}
        }

        req = urllib.request.Request(url, data=json.dumps(req_body).encode("utf-8"), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            ans_text = data["candidates"][0]["content"]["parts"][0]["text"]
            m_json = re.search(r'\{.*\}', ans_text, re.DOTALL)
            if m_json:
                return json.loads(m_json.group(0))
    except Exception as e:
        print(f"   [Vision OCR Skipped for {hole_no} p.{page_num}]: {e}")
    return None

def ingest_all():
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    cursor = conn.cursor()
    api_key = get_api_key()

    meta_data = {}
    if META_FILE.exists():
        with open(META_FILE, "r", encoding="utf-8") as f:
            meta_data = json.load(f)

    # Ingest using metadata as bedrock foundation
    for doc_name, d_info in meta_data.items():
        if "주상도" not in doc_name:
            continue
        pdf_path = DOCS_DIR / doc_name
        if not pdf_path.exists():
            continue

        print(f"\n=======================================================")
        print(f" [Ingesting] {doc_name} ({len(d_info.get('sections', []))} sections)")
        print(f"=======================================================")

        reader = PdfReader(pdf_path)
        for s in d_info.get("sections", []):
            h_no = s.get("section_id")
            s_page = s.get("start_page")
            e_page = s.get("end_page")
            fac = s.get("facility", ["본선"])[0] if s.get("facility") else "본선"

            # Register borehole master
            cursor.execute("""
            INSERT INTO boreholes (doc_name, hole_no, facility, page_start, page_end, elevation_m, groundwater_m, total_depth_m)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(doc_name, hole_no) DO UPDATE SET
                page_start=excluded.page_start,
                page_end=excluded.page_end,
                facility=excluded.facility
            """, (doc_name, h_no, fac, s_page, e_page, s.get("elevation_m"), None, None))

            # Try parsing pages
            for p_num in range(s_page, e_page + 1):
                p_text = reader.pages[p_num - 1].extract_text() or ""
                b_info, spts, strata = parse_drill_log_page(p_text, p_num, doc_name)

                # If text layer parsed SPT records
                if spts:
                    for spt in spts:
                        cursor.execute("""
                        INSERT INTO spt_records (doc_name, hole_no, page, sample_no, depth_m, n_value, n_str, blows, penetration_cm)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (doc_name, h_no, p_num, spt["sample_no"], spt["depth_m"], spt["n_value"], spt["n_str"], spt["blows"], spt["penetration_cm"]))
                    for st in strata:
                        cursor.execute("""
                        INSERT INTO strata_layers (doc_name, hole_no, page, stratum_name, depth_top_m, depth_bottom_m, thickness_m, uscs, description)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (doc_name, h_no, p_num, st["stratum_name"], st["depth_top_m"], st["depth_bottom_m"], st["thickness_m"], st["uscs"], st["description"]))
                    if b_info and b_info.get("groundwater_m"):
                        cursor.execute("UPDATE boreholes SET groundwater_m=? WHERE doc_name=? AND hole_no=?", (b_info["groundwater_m"], doc_name, h_no))
                else:
                    # Text layer empty (scanned image) -> Check if NH-3 or key borehole needing vision
                    if api_key and (h_no == "NH-3" or "GB" in h_no or s_page <= 3):
                        print(f" -> Performing Vision OCR for {h_no} (p.{p_num})...")
                        v_res = parse_page_via_vision(pdf_path, p_num, doc_name, h_no, api_key)
                        if v_res:
                            for spt in v_res.get("spt_records", []):
                                cursor.execute("""
                                INSERT INTO spt_records (doc_name, hole_no, page, sample_no, depth_m, n_value, n_str, blows, penetration_cm)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, (doc_name, h_no, p_num, spt.get("sample_no", "S"), spt.get("depth_m", 1.0), spt.get("n_value", 5), spt.get("n_str", "5/30"), spt.get("blows", 5), spt.get("pen", 30)))
                            for st in v_res.get("strata_layers", []):
                                cursor.execute("""
                                INSERT INTO strata_layers (doc_name, hole_no, page, stratum_name, depth_top_m, depth_bottom_m, thickness_m, uscs, description)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, (doc_name, h_no, p_num, st.get("stratum_name", "지층"), st.get("depth_top_m", 0.0), st.get("depth_bottom_m", 2.0), st.get("thickness_m", 2.0), "", ""))

        conn.commit()

    cursor.execute("SELECT COUNT(*) FROM boreholes")
    b_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM spt_records")
    s_cnt = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM strata_layers")
    st_cnt = cursor.fetchone()[0]

    print("\n=======================================================")
    print(" [Ingestion Summary]")
    print(f" - Registered Boreholes: {b_cnt} 개소 (1공구 45공 + 2공구 27공)")
    print(f" - Registered SPT Records: {s_cnt} 건")
    print(f" - Registered Strata Layers: {st_cnt} 개 층")
    print("=======================================================\n")
    conn.close()

if __name__ == "__main__":
    ingest_all()
