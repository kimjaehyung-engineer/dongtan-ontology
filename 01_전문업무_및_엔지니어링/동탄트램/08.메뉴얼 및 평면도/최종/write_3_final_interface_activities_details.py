import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# Find 3 Target Activity Folders (including twin folders)
target_folders = {}
for f in os.listdir(base_dir):
    f_path = os.path.join(base_dir, f)
    if os.path.isdir(f_path):
        if "설계변경 정산" in f or "30_도급자분" in f or "37_도급자분" in f:
            target_folders.setdefault("design_change", []).append(f_path)
        elif "선행공종" in f or "38_공사전" in f:
            target_folders.setdefault("pre_handover", []).append(f_path)
        elif "후행공종" in f or "39_공사중" in f:
            target_folders.setdefault("post_interface", []).append(f_path)

print(f"Target Folders Found: {target_folders}")

def get_std_template(wbs_code, title_name, dept_name, badge_name, purpose_text, method_text, deliverables, act_table_rows, svg_title, box1, box2, box3, box4, alert_msg, exp_text, summary_text):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - {title_name} 기술 표준서</title>
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
        <div class="breadcrumb">Dongtan Tram WBS {wbs_code} Standard</div>
        <h1 class="title">{title_name} 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 ({badge_name})</span>
            <span>|</span>
            <span><strong>주관부서:</strong> {dept_name}</span>
            <span>|</span>
            <span><span class="badge">{badge_name} 기술 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>{purpose_text}</td></tr>
            <tr><th>수행 방법</th><td>{method_text}</td></tr>
            <tr><th>주요 산출물</th><td>{deliverables}</td></tr>
            <tr><th>관련 법령/기준</th><td>관련 계약법, KCS 시방서 및 동탄트램 공종 간 인터페이스 지침</td></tr>
        </tbody>
    </table>

    <h2>2. {title_name} 정량 공학/행정 기술 수칙</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">⚙️ {title_name} 핵심 정량 검속 시방 기준</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 20%;">검속 항목</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">적용 법령 및 기준</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 55%;">핵심 정량 기술 수칙 및 행정 준수 기준</th>
                </tr>
            </thead>
            <tbody>
                {act_table_rows}
            </tbody>
        </table>
    </div>

    <h2>3. {title_name} 핵심 프로세스 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="320" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">{svg_title}</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① {box1[0]}</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">{box1[1]}</text>
            </g>

            <text x="225" y="145" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② {box2[0]}</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">{box2[1]}</text>
            </g>

            <text x="450" y="145" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ {box3[0]}</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">{box3[1]}</text>
            </g>

            <text x="675" y="145" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="170" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ {box4[0]}</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">{box4[1]}</text>
            </g>

            <rect x="30" y="250" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="278" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 {alert_msg}</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 {title_name} 엔지니어링 시스템 해설</h4>
        <p style="margin: 0; line-height: 1.7;">{exp_text}</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> {summary_text}
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS {wbs_code} | 지장물이설
    </div>
</div>
</body>
</html>"""

activity_specs = {
    "design_change": {
        "wbs": "2000-1-30", "title": "도급자분_위수탁분 설계변경 정산", "dept": "현장 공무팀 / 발주처 / 감리단", "badge": "설계변경 정산",
        "purpose": "실제 시굴 및 이설 현원 실측 수량을 바탕으로 국가계약법 시행령 제65조에 따라 도급자분 및 위수탁분 계약금액 변경 승인 및 사후 정산 완료",
        "method": "실굴착 증감 수량 비교표 작성, 신규 품목 단가 산정, PS 정산 항목 결재 및 화성시 발주처 변경 계약 서명 획득",
        "deliverables": "설계변경 실정보고서, 증감 수량 비교 내역서, 발주처 변경 계약서 원본",
        "rows": """<tr><td style="font-weight:bold;text-align:center;">국가계약법 제65조 준수</td><td style="text-align:center;">국가계약법 / 지방계약법</td><td>• 물량 증감 및 신규 신설 품목에 대한 계약 단가 산정 규정 준수<br>• 발주처 계약금액 증감 정식 변경 계약 서명 획득</td></tr>
<tr><td style="font-weight:bold;text-align:center;">실굴착 수량 재산정</td><td style="text-align:center;">KCS 토공 / 실측 수량</td><td>• 시굴 및 실제 매설관 굴착 수량(D300~D800mm) 실측 반영<br>• 도급자분 및 5대 위탁기관 내역서 100% 검속 재산정</td></tr>
<tr><td style="font-weight:bold;text-align:center;">PS 정산 항목 결재</td><td style="text-align:center;">발주처 정산 수칙</td><td>• PS(Provisional Sum) 정산 항목 실비 증빙 영수증 결재<br>• 감리원 수량 검속 서명 및 발주처 공무팀 정산 이관</td></tr>""",
        "svg_title": "도급자분 및 위수탁분 설계변경 계약 정산 절차",
        "box1": ("실굴착 수량 검속", "GPR/인력 시굴 실측 수량"),
        "box2": ("증감 수량 비교표", "도급/위탁 내역 재산정"),
        "box3": ("국가계약법 단가", "시행령 제65조 단가 산정"),
        "box4": ("발주처 변경 계약", "화성시 변경 계약 결재"),
        "alert": "설계변경 정산 지연 시 도급사/위탁기관 공사비 미지급 분쟁 리스크 전면 차단",
        "exp": "본 과업은 현치 실측 수량을 기반으로 국가계약법 제65조에 따라 증감 내역을 산정하고 발주처 변경 계약을 체결하는 절차입니다.",
        "summary": "실굴착 수량 비교표 작성, 국가계약법 단가 산정 및 발주처 변경 계약 서명 획득으로 정산을 완료하는 단계입니다!"
    },
    "pre_handover": {
        "wbs": "2000-1-38", "title": "공사전 선행공종에서 인수받을 사항", "dept": "현장 공사팀 / 토목 선행팀", "badge": "선행공종 인수",
        "purpose": "토목/지반 선행공종(사전토공, 흙막이 가설, 도로 차선 우회) 부지 및 측량 성과를 정밀 검속하여 적기에 현장 인수 완료",
        "method": "GRS80 측량 오차 ≤ ±5cm 검속, 흙막이 사면 변위 계측 성과 검토, 가설 배수 가동 확인 및 3자 인수서 체결",
        "deliverables": "선행공종 인수 인계서, GRS80 측량 성과 검속표, 흙막이 변위 계측 성과표",
        "rows": """<tr><td style="font-weight:bold;text-align:center;">GRS80 측량 오차 ≤ 5cm</td><td style="text-align:center;">선행 측량 성과표</td><td>• 선행 토공 부지 GRS80 세계측지계 좌표 <strong>오차 ≤ ±5cm 이내</strong> 검속<br>• 기점 표고 및 궤도 중심선 이격 위치 현치 인수</td></tr>
<tr><td style="font-weight:bold;text-align:center;">흙막이 변위계 점검</td><td style="text-align:center;">지하안전법 / 산업안전</td><td>• 선행 흙막이 가설재 변위 계측 성과(허용치 이내) 현장 인수<br>• 가설 집수정 및 펌프 배수 상태 100% 정상 가동 확인</td></tr>
<tr><td style="font-weight:bold;text-align:center;">3자 인수서 서명 체결</td><td style="text-align:center;">현장 감리 / 서면 양식</td><td>• 선행 소장, 당해 이설 소장 및 감리원 입회 <strong>3자 인수서 체결</strong><br>• 궤도 최소 이격거리 <strong>H ≥ 1.5m</strong> 작업 공간 확보 인수</td></tr>""",
        "svg_title": "공사전 토목 선행공종 부지 및 시설 정밀 인수 절차",
        "box1": ("선행 부지 인수", "토공/도로우회 도서 인수"),
        "box2": ("GRS80 측량 검속", "좌표/표고 오차 ≤ ±5cm"),
        "box3": ("흙막이/배수 점검", "변위 계측 & 배수 가동"),
        "box4": ("3자 인수서 서명", "선행/이설/감리 서명 결재"),
        "alert": "선행 부지 부실 인수 시 지장물 굴착 경계 침범 및 사면 붕괴 위험 전면 차단",
        "exp": "본 과업은 선행 토공 부지의 GRS80 측량 오차(±5cm 이내) 및 흙막이 안전성을 검속하여 인수 인계서를 체결하는 절차입니다.",
        "summary": "GRS80 측량 검속, 흙막이 배수 상태 확인 및 3자 인수서 체결로 성공적인 현장 인수를 완료하는 단계입니다!"
    },
    "post_interface": {
        "wbs": "2000-1-39", "title": "공사중 챙겨야할 후행공종의 요구사항", "dept": "현장 품질팀 / 궤도·노반·전기팀", "badge": "후행공종 연계",
        "purpose": "후행공종(강화노반, 콘크리트 궤도, 변전소, 통신)의 다짐도 및 이격거리 요구 수칙을 사전 이행하여 인터페이스 품질 확보",
        "method": "되메우기 층다짐 95% 이상, PBT K30 ≥ 110 MN/m³, Ev2 ≥ 120 MPa, 궤도 이격 H ≥ 1.5m 및 GIS 위치 대장 후행팀 이관",
        "deliverables": "후행 공종 인터페이스 점검표, PBT 평판재하시험 성적서, GIS 지형도 이관 확인증",
        "rows": """<tr><td style="font-weight:bold;text-align:center;">강화노반 K30 ≥ 110</td><td style="text-align:center;">KDS 47 10 00 궤도노반</td><td>• PBT 평판재하시험 <strong>K30 ≥ 110 MN/m³</strong>, <strong>Ev2 ≥ 120 MPa</strong> 확보<br>• 변형계수비 <strong>Ev2/Ev1 ≤ 2.2</strong> 및 되메우기 층다짐 <strong>95% 이상</strong></td></tr>
<tr><td style="font-weight:bold;text-align:center;">궤도 이격 H≥1.5m</td><td style="text-align:center;">동탄트램 궤도 시방</td><td>• 신설 이설관과 트램 궤도 간 <strong>최소 이격거리 H ≥ 1.5m</strong> 준수<br>• 후행 궤도 콘크리트 타설 시 관로 보호 슬래브 시공</td></tr>
<tr><td style="font-weight:bold;text-align:center;">GIS 위치 대장 이관</td><td style="text-align:center;">화성시 GIS / 후행팀</td><td>• GRS80 이설관 매설 좌표 GIS 대장 후행 궤도/전기팀 서면 이관<br>• 후행 공종 소장 인터페이스 검속 승인 서명 획득</td></tr>""",
        "svg_title": "공사중 후행 공종(노반/궤도/전기) 요구사항 이행 절차",
        "box1": ("후행 요구 조사", "궤도/노반 인터페이스 수립"),
        "box2": ("층다짐 95% 시공", "PBT K30 ≥ 110 MN/m³"),
        "box3": ("궤도 이격 H≥1.5m", "관로 보호 슬래브 부설"),
        "box4": ("후행 서면 이관", "GIS 대장 전달 & 서명"),
        "alert": "후행 요구 노반 다짐 미흡 시 트램 궤도 변형 및 운행 중 부등침하 재난 전면 차단",
        "exp": "본 과업은 강화노반 반력계수(K30 ≥ 110) 및 궤도 이격(1.5m) 수칙을 준수하고 GIS 위치 대장을 후행팀에 전달하는 절차입니다.",
        "summary": "PBT K30 ≥ 110 MN/m³, 궤도 이격 1.5m 및 GIS 대장 서면 이관으로 후행 인터페이스를 완수하는 단계입니다!"
    }
}

print("Executing Batch Overwrite for 3 Settlement & Interface Target Activities...")

for key, spec in activity_specs.items():
    folders = target_folders.get(key, [])
    std_content = get_std_template(
        spec["wbs"], spec["title"], spec["dept"], spec["badge"],
        spec["purpose"], spec["method"], spec["deliverables"],
        spec["rows"], spec["svg_title"], spec["box1"], spec["box2"],
        spec["box3"], spec["box4"], spec["alert"], spec["exp"], spec["summary"]
    )
    for folder in folders:
        sub_std = os.path.join(folder, "표준서")
        if os.path.exists(sub_std):
            for f in os.listdir(sub_std):
                if f.endswith(".html"):
                    fp = os.path.join(sub_std, f)
                    with open(fp, "w", encoding="utf-8") as out:
                        out.write(std_content)
                    print(f"  ✅ Overwritten [{spec['title']}]: {fp}")

print("🎉 Complete Batch Overwrite for 3 Settlement & Interface Target Activities Standard HTML files!")
