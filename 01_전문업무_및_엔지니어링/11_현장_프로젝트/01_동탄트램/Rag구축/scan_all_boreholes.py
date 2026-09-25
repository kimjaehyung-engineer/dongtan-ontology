import pypdf, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

rag_dir = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\14_개발_및_자동화_앱\RAG")
doc_path = rag_dir / "documents" / "기본설계 시추주상도(1공구)_45공.pdf"

reader = pypdf.PdfReader(str(doc_path))

results = []

for page_idx, page in enumerate(reader.pages):
    text = page.extract_text()
    if "HOLE No." not in text:
        continue
    
    # Extract hole no
    m_hole = re.search(r'HOLE No\.\s*([A-Za-z0-9_-]+)', text)
    hole_no = m_hole.group(1) if m_hole else f"Unknown_p{page_idx+1}"
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # Find depths (e.g. 1.0, 2.0, 3.0) and N-values (e.g. 3/30, 50/15)
    depths = []
    n_values = []
    
    for l in lines:
        if re.match(r'^\d+\.0$', l):
            depths.append(float(l))
        elif re.match(r'^\d+/\d+$', l):
            n_values.append(l)
            
    # Pair depths <= 3.0 with N-values
    matched_depths = [d for d in depths if d <= 3.0]
    for d, n in zip(matched_depths, n_values[:len(matched_depths)]):
        blows = int(n.split('/')[0])
        pen = int(n.split('/')[1])
        # N < 6
        if pen >= 30 and blows < 6:
            results.append({
                "hole_no": hole_no,
                "page": page_idx + 1,
                "depth": d,
                "n_str": n,
                "n_val": blows
            })

print(f"Total N < 6 within depth 3.0m findings across ALL 45 boreholes:")
for r in results:
    print(f"  - {r['hole_no']} (p.{r['page']}): 심도 {r['depth']}m ➔ N={r['n_str']}")
