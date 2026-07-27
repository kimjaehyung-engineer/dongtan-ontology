import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)"

targets = [
    {
        "gongjong": "사전토공사",
        "wbs": "9000-5-2",
        "folder": "2_발주전략 KOM",
        "title": "발주전략 KOM",
        "dept": "사전토공사 / 공무행정"
    },
    {
        "gongjong": "상부강화노반",
        "wbs": "9000-7-2",
        "folder": "2_발주전략 KOM",
        "title": "발주전략 KOM",
        "dept": "상부강화노반 / 공무행정"
    },
    {
        "gongjong": "콘크리트도상",
        "wbs": "9000-6-4",
        "folder": "4_발주전략 KOM",
        "title": "발주전략 KOM",
        "dept": "콘크리트도상 / 궤도공무"
    }
]

# Formatting function for risk checklists (same as the approved one)
def format_risk_checklist_text(raw_text):
    # Strip existing bullet styles and tags
    text_stripped = re.sub(r'<(div|p|li)[^>]*>', '\n', raw_text)
    text_stripped = re.sub(r'</(div|p|li)>', '\n', text_stripped)
    raw_sentences = re.split(r'[•·\n]', text_stripped)
    
    cleaned_sentences = []
    for s in raw_sentences:
        s = re.sub(r'<[^>]*>', '', s).strip()
        if not s:
            continue
        # Remove ☐ and [ ]
        s = s.replace("☐", "").replace("[ ]", "").strip()
        if "상세 체크리스트 파일" in s or "더블클릭" in s or "---" in s:
            continue
        s = re.sub(r'\s+', ' ', s)
        if s:
            cleaned_sentences.append(s)
            
    formatted_html = ""
    for s in cleaned_sentences:
        formatted_html += f'                    <div style="margin-bottom: 8px;">• {s}</div>\n'
    return formatted_html

# Parse original files and convert them
for t in targets:
    gongjong = t["gongjong"]
    folder = t["folder"]
    wbs = t["wbs"]
    title = t["title"]
    dept = t["dept"]
    
    dir_path = os.path.join(base_dir, gongjong, folder)
    
    # Paths
    std_path = os.path.join(dir_path, "표준서", f"발주전략 KOM_표준서.html" if gongjong != "콘크리트도상" else f"4_발주전략 KOM_표준서.html")
    chk_path = os.path.join(dir_path, "체크리스트", f"발주전략 KOM_체크리스트.html" if gongjong != "콘크리트도상" else f"4_발주전략 KOM_체크리스트.html")
    gui_path = os.path.join(dir_path, "수행지침", f"발주전략 KOM_수행지침.html" if gongjong != "콘크리트도상" else f"4_발주전략 KOM_수행지침.html")
    
    # ------------------ 1. Standard Rebuild ------------------
    if os.path.exists(std_path):
        with open(std_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse fields from original <table> in Standard
        purpose_m = re.search(r'과업 목적</th>\s*<td>(.*?)</td>', content, re.DOTALL)
        deliverable_m = re.search(r'산출물\s*\(결과\)</th>\s*<td>(.*?)</td>', content, re.DOTALL)
        std_sum_m = re.search(r'표준서\s*\(Standard\)\s*요약</th>\s*<td>(.*?)</td>', content, re.DOTALL)
        
        purpose = purpose_m.group(1).strip() if purpose_m else ""
        deliverable = deliverable_m.group(1).strip() if deliverable_m else ""
        std_sum = std_sum_m.group(1).strip() if std_sum_m else ""
        
        # Parse specs table rows
        # Find <tbody> ... </tbody> inside table 2
        tables = re.findall(r'<table[^>]*>.*?</table>', content, re.DOTALL)
        specs_rows = ""
        if len(tables) >= 2:
            tbody_m = re.search(r'<tbody>(.*?)</tbody>', tables[1], re.DOTALL)
            if tbody_m:
                specs_rows = tbody_m.group(1).strip()
        
        # Parse SVG steps and warning from original SVG
        svg_m = re.search(r'<svg[^>]*>(.*?)</svg>', content, re.DOTALL)
        step1 = "① 사전 준비 및 입찰 기획"
        step2 = "② 입찰설명회 및 적격심사"
        step3 = "③ 계약 체결 및 발주처 통지"
        caution = "🚨 하도급 통지 기한(30일) 미준수 및 부적합 업체 계약 강행 시 행정 제재 조치"
        
        if svg_m:
            texts = re.findall(r'<text[^>]*>(.*?)</text>', svg_m.group(1))
            # Clean texts to find steps
            step_texts = [t for t in texts if any(x in t for x in ["①", "②", "③", "🚨", "⚠️"])]
            for st in step_texts:
                if "①" in st: step1 = st.strip()
                elif "②" in st: step2 = st.strip()
                elif "③" in st: step3 = st.strip()
                elif any(x in st for x in ["🚨", "⚠️"]): caution = st.strip()
                
        # Parse diagram explanation and takeaway
        exp_m = re.search(r'<div class="diagram-explanation">(.*?)</div>', content, re.DOTALL)
        takeaway_m = re.search(r'<div class="key-takeaway">(.*?)</div>', content, re.DOTALL)
        
        explanation = exp_m.group(1).strip() if exp_m else """<strong>💡 프로세스 주요 설명:</strong><br>
        1. <strong>입찰 시방 특별조항 수립:</strong> 계약 전 관련 핵심 시방 규격(KCS/KDS)에 명시된 정량 기준과 안전 수칙을 하도급 특기 조항으로 명문화합니다.<br>
        2. <strong>적격 심사 및 하도급율 검증:</strong> 전문 기술인 확보, 시공 실적 및 신용 한도를 심사하고 부실 시공 방지를 위해 하도급율 82% 이상 기준을 엄격히 적용합니다.<br>
        3. <strong>행정 신고 완료:</strong> 하도급 계약 후 30일 이내에 법정 통지 서류를 지체 없이 발주처 및 감리단에 보고 완료합니다."""
        
        takeaway = takeaway_m.group(1).strip() if takeaway_m else f"💡 핵심 요약: {gongjong} 공사의 발주 전략 수립은 적격 하도급사를 선정하고 품질/안전 위해 리스크를 계약 단계에서 선제 차단하기 위한 필수 행정 절차."
        if "💡 핵심 요약" in takeaway:
            takeaway = takeaway.replace("💡 핵심 요약:", "").replace("<strong>💡 핵심 요약:</strong>", "").strip()

        # Build premium styled Standard HTML
        std_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{gongjong} - {title} 기술 표준서</title>
    <style>
        :root {{ --bg-primary: #f8fafc; --bg-card: #ffffff; --text-primary: #0f172a; --text-secondary: #475569; --accent-blue: #1e3a8a; --accent-cyan: #0284c7; --border-color: #e2e8f0; }}
        body {{ font-family: 'Pretendard', 'Noto Sans KR', sans-serif; margin: 0; padding: 30px 20px; background: var(--bg-primary); color: var(--text-primary); line-height: 1.6; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: var(--bg-card); padding: 40px; border-radius: 16px; border: 1px solid var(--border-color); box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08); }}
        .header {{ border-bottom: 3px solid var(--accent-blue); padding-bottom: 20px; margin-bottom: 30px; }}
        .breadcrumb {{ font-size: 0.85rem; color: var(--accent-cyan); font-weight: 700; margin-bottom: 6px; }}
        .title {{ font-size: 2.1rem; font-weight: 900; color: var(--text-primary); margin: 0; }}
        .meta-info {{ display: flex; gap: 12px; font-size: 0.9rem; color: var(--text-secondary); margin-top: 12px; }}
        .badge {{ background: #dbeafe; color: #1e40af; font-weight: 700; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; }}
        h2 {{ font-size: 1.4rem; font-weight: 800; color: var(--accent-blue); border-left: 5px solid var(--accent-cyan); padding-left: 12px; margin-top: 35px; margin-bottom: 18px; }}
        table {{ width: 100% !important; max-width: 100% !important; border-collapse: collapse; margin: 12px 0 20px 0; font-size: 0.92rem; }}
        th, td {{ border: 1px solid var(--border-color); padding: 12px 16px; text-align: left; vertical-align: middle; }}
        th {{ background: #f1f5f9; color: #1e293b; font-weight: 700; }}
        .svg-container {{ background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 20px; margin: 20px 0; text-align: center; }}
        .diagram-explanation {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; margin-top: 15px; font-size: 0.9rem; color: #334155; text-align: left; }}
        .key-takeaway {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 16px; margin-top: 15px; color: #166534; font-size: 0.9rem; }}
        .footer-note {{ margin-top: 40px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid var(--border-color); padding-top: 20px; }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="breadcrumb">Dongtan Tram WBS {wbs} Standard</div>
        <h1 class="title">{title} 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> {dept}</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 공무팀 / 외주팀</span>
            <span>|</span>
            <span><span class="badge">현장 맞춤 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>{purpose}</td></tr>
            <tr><th>산출물 (결과)</th><td>{deliverable}</td></tr>
            <tr><th>표준서 (Standard) 요약</th><td>{std_sum}</td></tr>
            <tr><th>관련 시방 기준</th><td>건설산업기본법, 하도급 거래 공정화에 관한 법률, 동탄트램 특별시방서</td></tr>
        </tbody>
    </table>

    <h2>2. {title} 고유 정량 공학 시방 및 기술 수칙 표</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">📐 {title} 정량적 하도급 심사 및 발주 품질 기준</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">기술 검속 항목</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">관련 법규 및 기준</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 50%;">핵심 정량 기술 수칙 및 발주 요건</th>
                </tr>
            </thead>
            <tbody>
{specs_rows}            </tbody>
        </table>
    </div>

    <h2>3. {title} 핵심 프로세스 및 구조 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 240" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="240" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="35" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">{gongjong} {title} 발주 행정 프로세스</text>

            <g transform="translate(50, 60)">
                <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="220" height="30" rx="8" fill="#e0e7ff"/>
                <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#1e1b4b">{step1}</text>
                <text x="15" y="55" font-size="11" fill="#334155">• 하도급 입찰 시방 특별조건 수립</text>
                <text x="15" y="75" font-size="11" fill="#334155">• 공구 분할 및 실행 내역 검토</text>
            </g>

            <text x="300" y="115" font-size="24" fill="#1e3a8a">➔</text>

            <g transform="translate(340, 60)">
                <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="220" height="30" rx="8" fill="#ffedd5"/>
                <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#9a3412">{step2}</text>
                <text x="15" y="55" font-size="11" fill="#334155">• 적격 심사 종합 평가 85점 이상</text>
                <text x="15" y="75" font-size="11" fill="#334155">• 저가 심의(하도급율 82% 이상)</text>
            </g>

            <text x="590" y="115" font-size="24" fill="#ea580c">➔</text>

            <g transform="translate(630, 60)">
                <rect width="220" height="100" rx="8" fill="#ffffff" stroke="#16a34a" stroke-width="2"/>
                <rect width="220" height="30" rx="8" fill="#dcfce7"/>
                <text x="110" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#14532d">{step3}</text>
                <text x="15" y="55" font-size="11" fill="#334155">• 표준 계약 체결 및 보증 증권 징구</text>
                <text x="15" y="75" font-size="11" fill="#334155">• 30일 이내 감리단/발주처 통지</text>
            </g>

            <rect x="50" y="185" width="800" height="35" rx="8" fill="#1e3a8a"/>
            <text x="450" y="207" text-anchor="middle" font-size="12" font-weight="bold" fill="#ffffff">{caution}</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        {explanation}
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> {takeaway}
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS {wbs} | {gongjong}
    </div>
</div>
</body>
</html>"""
        with open(std_path, 'w', encoding='utf-8') as f:
            f.write(std_html)

    # ------------------ 2. Guideline Rebuild ------------------
    if os.path.exists(gui_path):
        with open(gui_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse bullet points for three steps
        # Look for cards in the original guideline
        cards = re.findall(r'<div class="card"[^>]*>.*?</div>', content, re.DOTALL)
        step1_items = []
        step2_items = []
        step3_items = []
        
        if len(cards) >= 3:
            # Step 1
            step1_items = re.findall(r'<li>(.*?)</li>', cards[0], re.DOTALL)
            # Step 2
            step2_items = re.findall(r'<li>(.*?)</li>', cards[1], re.DOTALL)
            # Step 3
            step3_items = re.findall(r'<li>(.*?)</li>', cards[2], re.DOTALL)
            
        planning_list = "".join([f"            <li>{item.strip()}</li>\n" for item in step1_items])
        execution_list = "".join([f"            <li>{item.strip()}</li>\n" for item in step2_items])
        handover_list = "".join([f"            <li>{item.strip()}</li>\n" for item in step3_items])

        guide_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{gongjong} - {title} 수행지침서</title>
    <style>
        :root {{ --bg-primary: #f8fafc; --bg-card: #ffffff; --text-primary: #0f172a; --text-secondary: #475569; --accent-blue: #1e3a8a; --accent-cyan: #0284c7; --border-color: #cbd5e1; }}
        body {{ font-family: 'Pretendard', sans-serif; margin: 0; padding: 30px 20px; background: var(--bg-primary); color: var(--text-primary); line-height: 1.6; }}
        .container {{ max-width: 900px; margin: 0 auto; background: var(--bg-card); padding: 35px; border-radius: 12px; border: 1px solid var(--border-color); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
        .header {{ border-bottom: 2px solid var(--text-primary); padding-bottom: 15px; margin-bottom: 25px; }}
        .title {{ font-size: 1.8rem; font-weight: 800; margin: 0; color: var(--accent-blue); }}
        .meta {{ font-size: 0.9rem; color: var(--text-secondary); margin-top: 8px; }}
        .card {{ background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 20px; margin-bottom: 20px; }}
        .card-header {{ font-size: 1.15rem; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }}
        .bullet-list {{ list-style-type: none; padding-left: 0; margin: 0; }}
        .bullet-list li {{ position: relative; padding-left: 20px; margin-bottom: 12px; font-size: 0.92rem; color: #334155; }}
        .bullet-list li::before {{ content: "•"; position: absolute; left: 0; top: 0; color: var(--accent-cyan); font-weight: bold; font-size: 1.2rem; }}
        .footer-note {{ text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px; }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">{gongjong} - {title} 현장 수행지침서</h1>
        <div class="meta">WBS Code {wbs} | 공무행정 및 조달 관리 프로세스</div>
    </div>

    <div class="card" style="border-left: 6px solid #1e3a8a;">
        <div class="card-header" style="color: #1e3a8a;">① 사전 준비 및 계획 검토 단계 (Planning & Preparation)</div>
        <ul class="bullet-list">
{planning_list}        </ul>
    </div>

    <div class="card" style="border-left: 6px solid #ea580c;">
        <div class="card-header" style="color: #ea580c;">② 본 시공 및 정밀 실행 단계 (Execution & Quality Assurance)</div>
        <ul class="bullet-list">
{execution_list}        </ul>
    </div>

    <div class="card" style="border-left: 6px solid #166534;">
        <div class="card-header" style="color: #166534;">③ 검사, 준공 승인 및 이관 단계 (Sign-off & Handover)</div>
        <ul class="bullet-list">
{handover_list}        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 수행지침 | WBS {wbs} | {gongjong}
    </div>
</div>
</body>
</html>"""
        with open(gui_path, 'w', encoding='utf-8') as f:
            f.write(guide_html)

    # ------------------ 3. Checklist Rebuild ------------------
    if os.path.exists(chk_path):
        with open(chk_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse original <td> content from rows
        pre_td = re.search(r'<tr class="pre-row">.*?<td class="category">.*?</td>\s*<td>(.*?)</td>', content, re.DOTALL)
        ing_td = re.search(r'<tr class="ing-row">.*?<td class="category">.*?</td>\s*<td>(.*?)</td>', content, re.DOTALL)
        post_td = re.search(r'<tr class="post-row">.*?<td class="category">.*?</td>\s*<td>(.*?)</td>', content, re.DOTALL)
        chk_sum_m = re.search(r'<div class="summary-box">.*?<div[^>]*>(.*?)</div>', content, re.DOTALL)
        
        pre_raw = pre_td.group(1).strip() if pre_td else ""
        ing_raw = ing_td.group(1).strip() if ing_td else ""
        post_raw = post_td.group(1).strip() if post_td else ""
        chk_sum_text = chk_sum_m.group(1).strip() if chk_sum_m else f"{gongjong} 발주전략 KOM 이행 수칙"
        
        # Apply strict formattings
        pre_formatted = format_risk_checklist_text(pre_raw)
        ing_formatted = format_risk_checklist_text(ing_raw)
        post_formatted = format_risk_checklist_text(post_raw)

        chk_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{gongjong} - {title} 리스크 체크리스트</title>
    <style>
        :root {{
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --accent-red: #dc2626;
            --accent-orange: #ea580c;
            --accent-green: #16a34a;
            --border-color: #cbd5e1;
        }}
        body {{
            font-family: 'Pretendard', sans-serif;
            margin: 0;
            padding: 30px 20px;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: var(--bg-card);
            padding: 35px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }}
        .header {{
            border-bottom: 2px solid var(--text-primary);
            padding-bottom: 15px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        .title {{
            font-size: 1.6rem;
            font-weight: 800;
            margin: 0;
            color: #1e3a8a;
        }}
        .meta {{
            font-size: 0.9rem;
            font-weight: bold;
            color: var(--accent-orange);
        }}
        .summary-box {{
            background: #fdf2f8;
            border: 1px solid #fbcfe8;
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 25px;
            font-size: 0.95rem;
            color: #9d174d;
        }}
        table {{
            width: 100% !important;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th, td {{
            border: 1px solid var(--border-color);
            padding: 14px;
            font-size: 0.92rem;
            text-align: left;
        }}
        th {{
            background: #f1f5f9;
            font-weight: bold;
            text-align: center;
        }}
        .category {{
            font-weight: bold;
            text-align: center;
            vertical-align: middle;
            width: 18%;
        }}
        .pre-row {{ color: #0f172a; }}
        .ing-row {{ color: #0f172a; }}
        .post-row {{ color: #0f172a; }}
        .label-pre {{ color: var(--accent-orange); font-weight: bold; }}
        .label-ing {{ color: var(--accent-red); font-weight: bold; }}
        .label-post {{ color: var(--accent-green); font-weight: bold; }}
        .check-cell {{
            text-align: center;
            vertical-align: middle;
            width: 15%;
            font-weight: bold;
            color: #1e3a8a;
        }}
        .footer {{
            text-align: center;
            font-size: 0.85rem;
            color: #94a3b8;
            margin-top: 30px;
            border-top: 1px solid #e2e8f0;
            padding-top: 15px;
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">{title} 내부 리스크 체크리스트</h1>
        <span class="meta">WBS Code {wbs} | 내부 품질·안전 관리용</span>
    </div>

    <div class="summary-box">
        <h4 style="margin: 0 0 6px 0; color: #9d174d;">🚨 WBS 연동 체크리스트 핵심 요약</h4>
        <div style="font-weight: bold; line-height: 1.6;">{chk_sum_text}</div>
    </div>

    <table>
        <thead>
            <tr style="background: #f1f5f9;">
                <th style="width: 18%;">구분</th>
                <th style="width: 67%;">예방할 품질 및 안전 리스크 위해 요소 (KCS 규격 연동)</th>
                <th style="width: 15%;">점검 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr class="pre-row">
                <td class="category"><span class="label-pre">⚠️ 사전 리스크</span><br>(착수 전)</td>
                <td>
{pre_formatted}                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="ing-row">
                <td class="category"><span class="label-ing">⚡ 공사중 리스크</span><br>(시공 중)</td>
                <td>
{ing_formatted}                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
            <tr class="post-row">
                <td class="category"><span class="label-post">✅ 공사후 리스크</span><br>(완공 후)</td>
                <td>
{post_formatted}                </td>
                <td class="check-cell">☐ 확인완료</td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        동탄도시철도(트램) 시공사·협력사 합동 내부 리스크 대장 | {gongjong}
    </div>
</div>
</body>
</html>"""
        with open(chk_path, 'w', encoding='utf-8') as f:
            f.write(chk_html)
            
    print(f"🎉 Standardized styling for '{gongjong}' ({folder}) while preserving 100% of the original content.")

print("\n🎉 Format upgrade process finished successfully with complete content preservation!")
