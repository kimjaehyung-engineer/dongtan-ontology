import sys
sys.stdout.reconfigure(encoding='utf-8')
import re
from pathlib import Path
from pypdf import PdfReader
from pypdf import PdfReader

root = Path(r"C:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\11_현장_프로젝트\01_동탄트램\Rag구축\01_SOURCE_DOCUMENTS\02_기본설계_기술제안")

def extract_proposals():
    results = {}
    for f in sorted(root.glob("*.pdf")):
        reader = PdfReader(str(f))
        total_p = len(reader.pages)
        sections = []
        
        for idx, page in enumerate(reader.pages):
            p_num = idx + 1
            text = page.extract_text() or ""
            
            # Find proposal number e.g. 신호-01, 건축-01, 철도, 궤도-02
            m = re.search(r'제안번호\s*([가-힣\w\s,]+-\d{2})\s*(?:기술적\s*과제)?([^\n\r]+)?', text)
            if m:
                code = m.group(1).strip()
                desc = (m.group(2) or "").strip()
                # Clean up title
                full_title = f"[{code}] {desc}" if desc else f"[{code}] 기술제안 세부내용"
                # Check keywords in text
                kws = [code]
                if "정거장" in text: kws.append("정거장")
                if "차량기지" in text: kws.append("차량기지")
                if "환승" in text: kws.append("환승")
                if "1공구" in text: kws.append("1공구")
                if "2공구" in text: kws.append("2공구")
                if "안전" in text: kws.append("안전")
                if "경제성" in text or "원가" in text: kws.append("경제성")
                
                facility = []
                if "차량기지" in text: facility.append("차량기지")
                if "정거장" in text: facility.append("정거장")
                if "본선" in text or "1공구" in text or "2공구" in text: facility.append("본선")
                if not facility: facility = ["전구간"]
                
                sections.append({
                    "title": full_title[:80],
                    "task_id": code,
                    "start_page": p_num,
                    "end_page": p_num + 1 if p_num < total_p else p_num,
                    "facility": facility,
                    "keywords": kws
                })
                
        # If no explicit sections found, add chapter 1 and 2
        if not sections:
            sections = [
                {
                    "title": f"제1장 제안개요 및 핵심요약",
                    "task_id": f"{f.stem}-ch1",
                    "start_page": 1,
                    "end_page": min(3, total_p),
                    "facility": ["전구간"],
                    "keywords": [f.stem, "제안개요"]
                },
                {
                    "title": f"제2장 기술제안 세부사항",
                    "task_id": f"{f.stem}-ch2",
                    "start_page": min(4, total_p),
                    "end_page": total_p,
                    "facility": ["전구간"],
                    "keywords": [f.stem, "세부제안"]
                }
            ]
        else:
            # Add Ch1 overview at start if not present
            if sections[0]["start_page"] > 1:
                sections.insert(0, {
                    "title": "제1장 제안개요 및 총괄 요약",
                    "task_id": f"{f.stem}-overview",
                    "start_page": 1,
                    "end_page": sections[0]["start_page"] - 1,
                    "facility": ["전구간"],
                    "keywords": ["제안개요", "핵심요약"]
                })
                
        results[f.name] = {
            "total_pages": total_p,
            "sections": sections
        }
        
    return results

if __name__ == "__main__":
    res = extract_proposals()
    import json
    print(json.dumps(res, ensure_ascii=False, indent=2))
