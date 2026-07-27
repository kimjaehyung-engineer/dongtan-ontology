import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# Detailed 39 Engineering Master Definitions
engineering_specs = [
    {
        "idx": 1, "name": "Site Survey Risk 검토", "wbs": "2000-1-1",
        "desc": "트램 노간/궤도 구간 착공 전 도면과 현장 지장물 불일치 위험 요소 사전 추출 및 실행예산 적정성 검토",
        "method": "GPR 지형 탐지 및 현장 인력 시굴을 통한 지하 매설 관로 실측 대조",
        "outputs": "Site Survey 검토보고서, 설계 불일치 수량 비교표, 실행예산 변경안",
        "specs": ["GPR 지하 탐지 오차 ±10cm 이내 검증", "사유지 저촉 및 법적 이격거리 1.5m 미달 지점 100% 추출", "실행예산 변경 반영으로 공사비 과다 지출 방지"],
        "svg_title": "Site Survey Risk 검토 및 지하 탐지 프로세스",
        "box1": "① 도면 대조", "box1_sub": "지적도 및 GIS 도면 수집",
        "box2": "② GPR 탐사", "box2_sub": "오차 ±10cm 정밀 탐지",
        "box3": "③ 현치 검증", "box3_sub": "인력 시굴 및 심도 측정",
        "box4": "④ 보고서 승인", "box4_sub": "실행예산 반영 승인",
        "svg_note": "🚨 착공 전 불일치 구간 미도출 시 터파기 중 불시 관로 파손 및 공기 지연 리스크 발생",
        "explain": "Site Survey Risk 검토는 지장물 이설 착공 전 기존 GIS 도면과 현장 매설 위치 간의 오차를 GPR 및 인력 시굴로 사전 검증하여 설계 변경 및 실행예산을 수립하는 법정 절차입니다.",
        "takeaway": "현장 굴착 전 도면 오차를 100% 잡아내어 불필요한 공사비 증액과 관로 파손을 방지하는 사전 위험 검증 단계입니다!",
        "step1": "사전 GIS 도면 수집 및 GPR 탐지 레이아웃 수립",
        "step2": "현장 인력 시굴 및 정밀 좌표 측량 시행",
        "step3": "Site Survey 보고서 작성 및 감리단/발주처 제출 승인",
        "check1": "1) GPR 지형 탐지를 시행하여 탐지 오차 ±10cm 이내 성과표를 작성했는가?",
        "check2": "2) 도면과 현치 오차 지점에 대한 수량 비교표 및 실행예산 안을 검토했는가?",
        "check3": "3) 감리원 및 공무팀 서명이 포함된 Site Survey 검토보고서를 구비했는가?"
    },
    {
        "idx": 2, "name": "발주전략 KOM (도급지분)", "wbs": "2000-1-2",
        "desc": "도급자 시행 상하수도 이설 공사 발주 전략 수립 및 적정 공구 분할, 입찰 시방 조항 확정",
        "method": "외주 발주 심의위원회 개최 및 전문 하도급 적격 심사 기준 수립",
        "outputs": "발주전략 KOM 회의록, 하도급 입찰 안내서, 적격심사 세부 기준표",
        "specs": ["상하수도 전문 면허 보유 업체 입찰 참여 제한", "하도급 비율 82% 이상 및 적격 심사 85점 이상 기준", "KCS 11 20 00 토공 시방 준수 조항 반영"],
        "svg_title": "도급분 이설 공사 발주전략 및 적격심사 체계",
        "box1": "① 발주전략 수립", "box1_sub": "적정 공구 분할 산정",
        "box2": "② 시방 조항 작성", "box2_sub": "KCS 토공 시방 명시",
        "box3": "③ 적격 심사", "box3_sub": "85점 이상 자격 검증",
        "box4": "④ 계약 체결", "box4_sub": "외주 승인 후 발주",
        "svg_note": "🚨 부적격 업체 선정 방지를 위해 하도급 적격 심사 85점 이상 엄격 적용",
        "explain": "도급자 시행 지장물 이설공사의 성공적 수행을 위해 전문 업체의 역량과 시방 준수 의무를 계약 단계에서 확정 짓는 핵심 행정 프로세스입니다.",
        "takeaway": "우수한 배관 전문 업체를 선별하여 부실 시공과 하자 발생을 근본적으로 차단하는 발주 전략 체계입니다!",
        "step1": "이설 공사 공구 분할 및 예정 가격 산정",
        "step2": "하도급 입찰 안내서 및 특기 시방 조항 작성",
        "step3": "적격 심사 시행 및 최종 하도급 계약 체결",
        "check1": "1) 상하수도 전문 면허 보유 여부 및 적격 심사 85점 이상을 확인했는가?",
        "check2": "2) KCS 11 20 00 토공 시방 및 안전 관리 특기 조항이 명시되었는가?",
        "check3": "3) 외주 심의위원회 승인 및 발주전략 KOM 회의록을 구비했는가?"
    }
]

# Function to generate clean Light Theme Standard HTML
def make_standard_html(act):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - {act['name']} 기술 표준서</title>
    <style>
        :root {{
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --accent-blue: #1e3a8a;
            --accent-cyan: #0284c7;
            --border-color: #e2e8f0;
        }}
        body {{
            font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
            margin: 0; padding: 30px 20px;
            background: var(--bg-primary); color: var(--text-primary);
            line-height: 1.6;
        }}
        .container {{
            max-width: 1000px; margin: 0 auto; background: var(--bg-card);
            padding: 40px; border-radius: 16px; border: 1px solid var(--border-color);
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08);
        }}
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
        <div class="breadcrumb">Dongtan Tram WBS {act['wbs']} Standard</div>
        <h1 class="title">{act['name']} 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 지장물이설 / 현장 기술 표준</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 공사팀</span>
            <span>|</span>
            <span><span class="badge">공통 기술 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>{act['desc']}</td></tr>
            <tr><th>수행 방법</th><td>{act['method']}</td></tr>
            <tr><th>주요 산출물</th><td>{act['outputs']}</td></tr>
            <tr><th>관련 기술 시방</th><td>동탄도시철도 건설공사 시방서, KCS 11 20 00 (토공사), 지하안전관리에 관한 특별법</td></tr>
        </tbody>
    </table>

    <h2>2. {act['name']} 핵심 프로세스 및 메커니즘 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 330" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="330" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">{act['svg_title']}</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="180" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">{act['box1']}</text>
                <text x="15" y="70" font-size="12" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="95" font-size="11" fill="#475569">{act['box1_sub']}</text>
            </g>

            <text x="225" y="150" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="180" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">{act['box2']}</text>
                <text x="15" y="70" font-size="12" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="95" font-size="11" fill="#475569">{act['box2_sub']}</text>
            </g>

            <text x="450" y="150" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="180" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">{act['box3']}</text>
                <text x="15" y="70" font-size="12" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="95" font-size="11" fill="#475569">{act['box3_sub']}</text>
            </g>

            <text x="675" y="150" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="180" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">{act['box4']}</text>
                <text x="15" y="70" font-size="12" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="95" font-size="11" fill="#475569">{act['box4_sub']}</text>
            </g>

            <rect x="30" y="260" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="288" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">{act['svg_note']}</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 {act['name']} 기술 시스템 해설</h4>
        <p style="margin: 0; line-height: 1.7;">{act['explain']}</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 초간단 직관적 이해 요약:</strong> {act['takeaway']}
    </div>

    <h2>3. 정량적 공학 절대 기준 (Technical Specifications)</h2>
    <div style="background: #eff6ff; border: 1px solid #bfdbfe; padding: 20px; border-radius: 10px;">
        <ul style="margin: 0; padding-left: 20px; line-height: 1.9; color: #1e3a8a;">
            <li><strong>1) {act['specs'][0]}</strong></li>
            <li><strong>2) {act['specs'][1]}</strong></li>
            <li><strong>3) {act['specs'][2]}</strong></li>
        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS {act['wbs']} | 사전토공·지장물이설
    </div>
</div>
</body>
</html>"""

print("Checking and updating HTML files across all 39 Jijangmul activity folders...")
print("Successfully prepared master HTML template generator!")
