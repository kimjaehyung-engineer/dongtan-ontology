import re, sys

target_path = r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG\server.py"
with open(target_path, "r", encoding="utf-8") as f:
    code = f.read()

# Replace extract_target_numbers
old_extractor_start = "def extract_target_numbers(query):"
old_extractor_end = "def get_smart_pdf_payload(file_path, query=\"\"):"

pos_s = code.find(old_extractor_start)
pos_e = code.find(old_extractor_end)

if pos_s == -1 or pos_e == -1:
    print(f"Extractor boundaries not found: {pos_s}, {pos_e}")
    sys.exit(1)

new_extractor = '''def extract_target_numbers(query):
    nums = set()
    # 1. Clean query: eliminate depths (3m, 3.0m, 3미터) and N-value conditions (n<6, n <= 6, n치 5 등)
    clean_q = re.sub(r'\\d+(?:\\.\\d+)?\\s*(?:m|m이내|m이상|m이하|미터)', ' ', query, flags=re.I)
    clean_q = re.sub(r'n\\s*치?\\s*[<>=≤≥]\\s*\\d+', ' ', clean_q, flags=re.I)
    clean_q = re.sub(r'n\\s*치?\\s*(?:이|가)?\\s*\\d+\\s*(?:이하|미만|이상|초과)', ' ', clean_q, flags=re.I)
    clean_q = re.sub(r'n\\s*<\\s*\\d+', ' ', clean_q, flags=re.I)
    
    # 2. Match ranges like 7~9번, 7-9, GB 7~9
    for m in re.finditer(r'(\\d+)\\s*[~-]\\s*(\\d+)', clean_q):
        try:
            s_n, e_n = int(m.group(1)), int(m.group(2))
            if s_n <= e_n and e_n - s_n <= 45:
                nums.update(range(s_n, e_n + 1))
        except ValueError:
            pass
            
    # 3. Match explicit borehole names: GB-7, NH-3, DT-5, 7번, 7호, 공번 7, 7공
    for m in re.finditer(r'(?:gb|nh|dt|공번|시추공|보링공)\\s*[-_#]?\\s*(\\d+)', clean_q, re.I):
        try:
            nums.add(int(m.group(1)))
        except ValueError:
            pass
            
    for m in re.finditer(r'(\\d+)\\s*(?:번공?|호공?|공)', clean_q, re.I):
        try:
            nums.add(int(m.group(1)))
        except ValueError:
            pass

    return nums


def scan_all_boreholes_for_condition(file_path, max_depth=3.0, max_n=6):
    """Full-scan all borehole logs in PDF for depth <= max_depth and N < max_n."""
    try:
        import pypdf
        reader = pypdf.PdfReader(str(file_path))
        findings = []
        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if "HOLE No." not in text:
                continue
            m_hole = re.search(r'HOLE No\\.\\s*([A-Za-z0-9_-]+)', text)
            hole_no = m_hole.group(1) if m_hole else f"공번_p{page_idx+1}"
            lines = [l.strip() for l in text.split('\\n') if l.strip()]
            depths = []
            n_values = []
            for l in lines:
                if re.match(r'^\\d+\\.0$', l):
                    depths.append(float(l))
                elif re.match(r'^\\d+/\\d+$', l):
                    n_values.append(l)
            matched_depths = [d for d in depths if d <= max_depth]
            for d, n in zip(matched_depths, n_values[:len(matched_depths)]):
                parts = n.split('/')
                blows = int(parts[0])
                pen = int(parts[1])
                if pen >= 30 and blows < max_n:
                    findings.append({
                        "hole_no": hole_no,
                        "page": page_idx + 1,
                        "depth": d,
                        "n_str": n,
                        "blows": blows
                    })
        return findings
    except Exception as e:
        return []

'''

code = code[:pos_s] + new_extractor + code[pos_e:]
print("Updated extract_target_numbers and added scan_all_boreholes_for_condition")

with open(target_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Saved server.py")
