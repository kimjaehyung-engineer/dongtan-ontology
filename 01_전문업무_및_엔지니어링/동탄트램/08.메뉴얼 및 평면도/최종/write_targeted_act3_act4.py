import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

act3_path = os.path.join(base_dir, "3_지장물 이설 요청 (위수탁고)")
act4_path = os.path.join(base_dir, "4_도급자분 이설업체 선정(상_하수)")

# Act 3 HTML Templates
act3_std = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 지장물 이설 요청 (위수탁고) 기술 표준서</title>
    <style>
        :root { --bg-primary: #f8fafc; --bg-card: #ffffff; --text-primary: #0f172a; --text-secondary: #475569; --accent-blue: #1e3a8a; --accent-cyan: #0284c7; --border-color: #e2e8f0; }
        body { font-family: 'Pretendard', 'Noto Sans KR', sans-serif; margin: 0; padding: 30px 20px; background: var(--bg-primary); color: var(--text-primary); line-height: 1.6; }
        .container { max-width: 1000px; margin: 0 auto; background: var(--bg-card); padding: 40px; border-radius: 16px; border: 1px solid var(--border-color); box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08); }
        .header { border-bottom: 3px solid var(--accent-blue); padding-bottom: 20px; margin-bottom: 30px; }
        .breadcrumb { font-size: 0.85rem; color: var(--accent-cyan); font-weight: 700; margin-bottom: 6px; }
        .title { font-size: 2.1rem; font-weight: 900; color: var(--text-primary); margin: 0; }
        .meta-info { display: flex; gap: 12px; font-size: 0.9rem; color: var(--text-secondary); margin-top: 12px; }
        .badge { background: #dbeafe; color: #1e40af; font-weight: 700; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; }
        h2 { font-size: 1.4rem; font-weight: 800; color: var(--accent-blue); border-left: 5px solid var(--accent-cyan); padding-left: 12px; margin-top: 35px; margin-bottom: 18px; }
        table { width: 100% !important; max-width: 100% !important; border-collapse: collapse; margin: 12px 0 20px 0; font-size: 0.92rem; }
        th, td { border: 1px solid var(--border-color); padding: 12px 16px; text-align: left; vertical-align: middle; }
        th { background: #f1f5f9; color: #1e293b; font-weight: 700; }
        .svg-container { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 20px; margin: 20px 0; text-align: center; }
        .diagram-explanation { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; margin-top: 15px; font-size: 0.9rem; color: #334155; text-align: left; }
        .key-takeaway { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 16px; margin-top: 15px; color: #166534; font-size: 0.9rem; }
        .footer-note { margin-top: 40px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid var(--border-color); padding-top: 20px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="breadcrumb">Dongtan Tram WBS 2000-1-3 Standard</div>
        <h1 class="title">지장물 이설 요청 (위수탁고) 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (행정·인허가)</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 공무팀 / 발주처(화성시)</span>
            <span>|</span>
            <span><span class="badge">위수탁 행정 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>동탄트램 궤도 노선 내 간섭되는 5대 위탁 지장관(가스, 난방, 통신, 전력, 광역상수)의 관리기관별 정식 이설 요청 및 행정적 협약 절차 수행</td></tr>
            <tr><th>수행 방법</th><td>현치 실측 위치도 및 개략 이설 물량 첨부 후 발주처(화성시) 경유 위탁기관 정식 공문 발송 (회신 법정 기한 14일 이내 관리)</td></tr>
            <tr><th>주요 산출물</th><td>지장물 이설 요청 공문 원본, 기관별 인수인계 접수증, 위수탁 이설 협약서</td></tr>
            <tr><th>관련 법령/기준</th><td>건설기술 진흥법 제48조, 지하안전관리에 관한 특별법, 지하시설물 통합관리체계 지침</td></tr>
        </tbody>
    </table>

    <h2>2. 지장물 이설 요청 4단계 표준 메커니즘 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="320" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">지장물 이설 요청 및 위수탁 기관 협의 프로세스</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① 이설 도면 작성</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 실측 현치 위치도</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 궤도 이격거리 H≥1.5m</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 개략 이설 수량 도출</text>
            </g>

            <text x="225" y="145" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② 공문 발송</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 발주처(화성시) 경유</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 5대 위탁기관 통보</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 법정기한 14일 명시</text>
            </g>

            <text x="450" y="145" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ 이설 소요공기 조율</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 관종별 표준 공기</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 전력(255일), 광역(160일)</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 통신(150일), 난방(80일)</text>
            </g>

            <text x="675" y="145" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="170" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ 협약 체결</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 이설 시방 확정</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 현장 입회관 지정</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 공정 릴레이 수립</text>
            </g>

            <rect x="30" y="250" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="278" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 공문 미발송 및 기관 협의 지연 시 후행 궤도/노반 공정 전체 멈춤 발생 예방</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 지장물 이설 요청 업무 해설</h4>
        <p style="margin: 0; line-height: 1.7;">이설 요청은 트램 궤도 노선 내 매설된 지하 유틸리티 관로를 정밀 조사하여 관리기관에 공식 이설을 이행하도록 만드는 법정 최초 행정 단계입니다. 각 위탁기관별 소요 공기(가스 62일, 난방 80일, 통신 150일, 전력 255일, 광역 160일)를 착공 공정표에 사전 반영하여 시공 간섭을 차단합니다.</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> 발주처 공문 발송과 14일 이내 법정 회신 관리를 통해 위수탁 기관의 지연을 막고 궤도 1.5m 이격거리를 확보하는 사전 행정 단계입니다!
    </div>

    <h2>3. 정량적 행정/공학 절대 기준 (Technical Specifications)</h2>
    <div style="background: #eff6ff; border: 1px solid #bfdbfe; padding: 20px; border-radius: 10px;">
        <ul style="margin: 0; padding-left: 20px; line-height: 1.9; color: #1e3a8a;">
            <li><strong>1) 이설 회신 법정 기한:</strong> 위수탁 이설 요청 공문 접수 후 <strong>14일 이내</strong> 정식 회신 접수 및 현장 감독관 지정</li>
            <li><strong>2) 트램 궤도 안전 이격거리:</strong> 이설 요청 도면 내 궤도 구조물 및 하부 강화노반과의 <strong>수평/수직 최소 이격거리 H ≥ 1.5m 이상</strong> 확보 명시</li>
            <li><strong>3) 관종별 이설 표준 소요 공기 반영:</strong> 특고압 전력관(255일), 광역상수관(160일), 통신관로(150일), 지역난방관(80일), 도시가스관(62일) 준수</li>
        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 2000-1-3 | 지장물이설
    </div>
</div>
</body>
</html>"""


# Act 4 HTML Templates
act4_std = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 도급자분 이설업체 선정(상_하수) 기술 표준서</title>
    <style>
        :root { --bg-primary: #f8fafc; --bg-card: #ffffff; --text-primary: #0f172a; --text-secondary: #475569; --accent-blue: #1e3a8a; --accent-cyan: #0284c7; --border-color: #e2e8f0; }
        body { font-family: 'Pretendard', 'Noto Sans KR', sans-serif; margin: 0; padding: 30px 20px; background: var(--bg-primary); color: var(--text-primary); line-height: 1.6; }
        .container { max-width: 1000px; margin: 0 auto; background: var(--bg-card); padding: 40px; border-radius: 16px; border: 1px solid var(--border-color); box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08); }
        .header { border-bottom: 3px solid var(--accent-blue); padding-bottom: 20px; margin-bottom: 30px; }
        .breadcrumb { font-size: 0.85rem; color: var(--accent-cyan); font-weight: 700; margin-bottom: 6px; }
        .title { font-size: 2.1rem; font-weight: 900; color: var(--text-primary); margin: 0; }
        .meta-info { display: flex; gap: 12px; font-size: 0.9rem; color: var(--text-secondary); margin-top: 12px; }
        .badge { background: #dbeafe; color: #1e40af; font-weight: 700; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; }
        h2 { font-size: 1.4rem; font-weight: 800; color: var(--accent-blue); border-left: 5px solid var(--accent-cyan); padding-left: 12px; margin-top: 35px; margin-bottom: 18px; }
        table { width: 100% !important; max-width: 100% !important; border-collapse: collapse; margin: 12px 0 20px 0; font-size: 0.92rem; }
        th, td { border: 1px solid var(--border-color); padding: 12px 16px; text-align: left; vertical-align: middle; }
        th { background: #f1f5f9; color: #1e293b; font-weight: 700; }
        .svg-container { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 20px; margin: 20px 0; text-align: center; }
        .diagram-explanation { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; margin-top: 15px; font-size: 0.9rem; color: #334155; text-align: left; }
        .key-takeaway { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 16px; margin-top: 15px; color: #166534; font-size: 0.9rem; }
        .footer-note { margin-top: 40px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid var(--border-color); padding-top: 20px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="breadcrumb">Dongtan Tram WBS 2000-1-4 Standard</div>
        <h1 class="title">도급자분 이설업체 선정(상_하수) 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (하도급·발주)</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 외주팀 / 공무팀</span>
            <span>|</span>
            <span><span class="badge">하도급 검증 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>도급자 시행 상하수도(상수관, 하수관, 오수관) 이설 공사의 성공적 수행을 위한 우수 전문 하도급 업체 선정 및 계약 수칙 수립</td></tr>
            <tr><th>수행 방법</th><td>전문 건설업 면허 검증, 적격 심사(85점 이상), 하도급율(82% 이상) 평가 및 외주 심의위원회 승인을 거쳐 계약 체결</td></tr>
            <tr><th>주요 산출물</th><td>하도급 적격 심사표, 외주 심의 승인서, 하도급 계약서, 발주처 하도급 통지서</td></tr>
            <tr><th>관련 법령/기준</th><td>건설산업기본법 제29조(하도급 제한), KCS 11 20 00 (토공사), KCS 47 10 00 (상하수도공사)</td></tr>
        </tbody>
    </table>

    <h2>2. 이설업체 적격 심사 및 계약 4단계 프로세스 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="320" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">상하수도 이설 전문 하도급 업체 선정 및 검증 체계</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① 입찰 자격 검증</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 상하수도 설비 면허</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 3년 내 동등 실적</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 재무 건전성 평가</text>
            </g>

            <text x="225" y="145" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② 적격 심사 평가</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 적격점수 ≥ 85점</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 하도급율 ≥ 82%</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 저가 하도급 방지</text>
            </g>

            <text x="450" y="145" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ 특기 시방 조항</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 수압 10kg/cm² 명시</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 하수 CCTV 100%</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 층다짐 95% 준수</text>
            </g>

            <text x="675" y="145" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="170" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ 계약 & 통보</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 하도급 계약 체결</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 30일 내 발주처 통지</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 현장 투입 승인</text>
            </g>

            <rect x="30" y="250" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="278" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 부적격 업체 투입에 따른 배관 수밀 시험 실패 및 도로 재굴착 리스크 철저 차단</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 상하수도 이설업체 선정 프로세스 해설</h4>
        <p style="margin: 0; line-height: 1.7;">본 과업은 도급자가 직접 시공하는 상수관, 하수관, 오수관 이설 공사의 수밀성 및 구조적 안정성을 보장하기 위해 상하수도 전문 면허 업체를 객관적 적격 심사(85점 이상)로 선별하고 시방 준수 의무를 계약화하는 절차입니다.</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> 적격 심사 85점 이상과 하도급율 82% 이상을 적용하고, 계약서에 수압 10kg/cm² 및 CCTV 100% 조항을 명시하여 최고 품질의 배관 시공을 보장하는 단계입니다!
    </div>

    <h2>3. 정량적 행정/공학 절대 기준 (Technical Specifications)</h2>
    <div style="background: #eff6ff; border: 1px solid #bfdbfe; padding: 20px; border-radius: 10px;">
        <ul style="margin: 0; padding-left: 20px; line-height: 1.9; color: #1e3a8a;">
            <li><strong>1) 자격 및 적격 심사 기준:</strong> 상하수도설비공업 전문 면허 보유, 최근 3년 동등 관경 이설 실적 구비, 하도급 적격 심사 <strong>85점 이상</strong> 획득</li>
            <li><strong>2) 하도급율 및 저가 방지:</strong> 실행예산 대비 하도급 계약 금액 비율 <strong>82% 이상</strong> 준수로 품질 부실 예방</li>
            <li><strong>3) 계약 시방 수칙 명시:</strong> 상수도 수압시험(10kg/cm² 1시간 Zero 누수), 하수도 CCTV 내시경 조사(100%), 토사 되메우기 층다짐도(95% 이상) 계약 특기 조항 반영</li>
            <li><strong>4) 법정 통지 기한:</strong> 하도급 계약 체결 후 <strong>30일 이내</strong> 발주처(화성시)에 건설산업기본법에 따른 하도급 통지 완료</li>
        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 2000-1-4 | 지장물이설
    </div>
</div>
</body>
</html>"""

# Write files to Act 3 folder
if os.path.exists(act3_path):
    with open(os.path.join(act3_path, "표준서", "지장물 이설 요청 (위수탁고)_표준서.html"), 'w', encoding='utf-8') as f:
        f.write(act3_std)
    print("Writing pristine Act 3 Standard HTML...")

# Write files to Act 4 folder
if os.path.exists(act4_path):
    with open(os.path.join(act4_path, "표준서", "도급자분 이설업체 선정(상_하수)_표준서.html"), 'w', encoding='utf-8') as f:
        f.write(act4_std)
    print("Writing pristine Act 4 Standard HTML...")

print("🎉 Finished writing targeted pristine Act 3 and Act 4 HTML files!")
