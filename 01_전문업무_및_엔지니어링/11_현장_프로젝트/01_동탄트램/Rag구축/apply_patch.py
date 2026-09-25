import re

server_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"

with open(server_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Replace extract_target_numbers
new_extract_func = '''def extract_target_numbers(query):
    nums = set()
    # 1. Clean query from depth, N-value conditions, page numbers to avoid false positives
    # e.g. "3m", "3.0m", "n<6", "n < 6", "n=10", "n치 6", "p.4", "페이지 5"
    cleaned = re.sub(r'\\b\\d+(?:\\.\\d+)?\\s*(?:m|meter|미터|cm|km)\\b', ' ', query, flags=re.I)
    cleaned = re.sub(r'[nN]\\s*(?:치)?\\s*([<>]=?|=)\\s*\\d+', ' ', cleaned)
    cleaned = re.sub(r'[nN]\\s*치\\s*[<>=]?\\s*\\d+', ' ', cleaned)
    cleaned = re.sub(r'p(?:age|\\.)?\\s*\\d+', ' ', cleaned, flags=re.I)
    cleaned = re.sub(r'심도\\s*\\d+(?:\\.\\d+)?', ' ', cleaned)

    # 2. range like 7~9, 7-9, 7 - 9
    for m in re.finditer(r'(\\d+)\\s*[~-]\\s*(\\d+)', cleaned):
        try:
            s_n, e_n = int(m.group(1)), int(m.group(2))
            if s_n <= e_n and e_n - s_n <= 30:
                nums.update(range(s_n, e_n + 1))
        except ValueError:
            pass

    # 3. Explicit borehole patterns: GB-7, NH-3, DT-1, 7번, 7공, 7호
    for m in re.finditer(r'(?:gb|nh|dt|공|시추공|번|호)\\s*[-_]?\\s*(\\d+)', cleaned, re.I):
        try:
            nums.add(int(m.group(1)))
        except ValueError:
            pass
    for m in re.finditer(r'(\\d+)\\s*(?:공|호|번|공구)', cleaned, re.I):
        try:
            nums.add(int(m.group(1)))
        except ValueError:
            pass
    return nums'''

text = re.sub(r'def extract_target_numbers\(query\):.*?(?=\ndef )', lambda m: new_extract_func + '\n', text, flags=re.DOTALL)
print("Replaced extract_target_numbers")

# 2. Add scan_all_boreholes_for_condition before get_smart_pdf_payload
scanner_code = '''
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
            m_hole = re.search(r'HOLE\\s*No\\.?\\s*([A-Z0-9_-]+)', txt, re.I)
            if not m_hole:
                m_hole = re.search(r'\\b(NH-\\d+|GB-\\d+|DT-\\d+)\\b', txt)
            hole_name = m_hole.group(1).strip() if m_hole else f"p.{p_idx+1}"
            
            lines = [l.strip() for l in txt.split('\\n') if l.strip()]
            samples = [l for l in lines if re.match(r'^S-\\d+$', l)]
            n_values = [l for l in lines if re.match(r'^\\d+/\\d+$', l)]
            depths = [float(l) for l in lines if re.match(r'^\\d+\\.\\d+$', l) and 0.5 <= float(l) <= 50.0]
            
            matched_records = []
            if len(depths) >= len(n_values) and len(n_values) > 0:
                num_spt = len(n_values)
                spt_depths = depths[-num_spt:] if len(depths) >= num_spt else depths
                for i, n_str in enumerate(n_values):
                    d = spt_depths[i] if i < len(spt_depths) else (i + 1) * 1.0
                    m_blow = re.match(r'^(\\d+)/(\\d+)$', n_str)
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
'''

if "def scan_all_boreholes_for_condition" not in text:
    text = text.replace("def get_smart_pdf_payload(", scanner_code + "\ndef get_smart_pdf_payload(")
    print("Added scan_all_boreholes_for_condition")

with open(server_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved updated server.py successfully!")
