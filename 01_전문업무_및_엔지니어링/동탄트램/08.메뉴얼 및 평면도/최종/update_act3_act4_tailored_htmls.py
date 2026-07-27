import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# ----------------------------------------------------
# 1. Activity 3: 지장물 이설 요청 (위수탁고) HTML Templates
# ----------------------------------------------------
act3_standard_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 지장물 이설 요청 (위수탁고) 기술 표준서</title>
    <style>
        :root {
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --accent-blue: #1e3a8a;
            --accent-cyan: #0284c7;
            --border-color: #e2e8f0;
        }
        body {
            font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
            margin: 0; padding: 30px 20px;
            background: var(--bg-primary); color: var(--text-primary);
            line-height: 1.6;
        }
        .container {
            max-width: 1000px; margin: 0 auto; background: var(--bg-card);
            padding: 40px; border-radius: 16px; border: 1px solid var(--border-color);
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08);
        }
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

act3_guideline_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 지장물 이설 요청 (위수탁고) 수행지침</title>
    <style>
        body { font-family: 'Pretendard', 'Noto Sans KR', sans-serif; margin: 0; padding: 25px; background: #f8fafc; color: #0f172a; line-height: 1.6; }
        .container { max-width: 950px; margin: 0 auto; background: #ffffff; padding: 35px; border-radius: 14px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); }
        .header { border-bottom: 3px solid #16a34a; padding-bottom: 18px; margin-bottom: 25px; }
        .title { font-size: 1.9rem; font-weight: 900; color: #14532d; margin: 0; }
        .meta-info { font-size: 0.9rem; color: #475569; margin-top: 8px; font-weight: 600; }
        h2 { font-size: 1.35rem; font-weight: 800; color: #15803d; border-left: 5px solid #22c55e; padding-left: 12px; margin-top: 30px; margin-bottom: 18px; }
        .card { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px; margin-bottom: 16px; }
        .card-header { font-weight: 800; font-size: 1.05rem; margin-bottom: 8px; color: #166534; }
        .bullet-list { margin: 0; padding-left: 20px; font-size: 0.9rem; color: #334155; }
        .bullet-list li { margin-bottom: 6px; }
        .footer-note { margin-top: 35px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 18px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">지장물 이설 요청 (위수탁고) 3단계 현장 수행지침</h1>
        <div class="meta-info">Dongtan Tram WBS 2000-1-3 | 위수탁 기관 요청 및 협약 이행 가이드</div>
    </div>

    <h2>📌 지장물 이설 요청 3단계 정밀 수행 지침 (Playbook)</h2>

    <div class="card" style="border-left: 5px solid #2563eb;">
        <div class="card-header" style="color: #2563eb;">① 사전 준비 단계 (Preparation)</div>
        <ul class="bullet-list">
            <li><strong>지장관 현치 도면 첨부:</strong> GPR 지하탐지 및 인력 시굴로 확보된 매설 관로 측량 도면과 궤도 구조물(이격거리 H ≥ 1.5m) 간섭 현황도를 작성합니다.</li>
            <li><strong>이설 수량 산출:</strong> 관종별(가스, 난방, 통신, 전력, 광역상수) 이설 연장, 깊이 및 신설 관경을 정밀 도출합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 5px solid #ea580c;">
        <div class="card-header" style="color: #ea580c;">② 요청 공문 발송 및 기한 관리 단계 (Execution)</div>
        <ul class="bullet-list">
            <li><strong>발주처 경유 공문 발송:</strong> 발주처(화성시)의 정식 결재를 거쳐 5대 위탁 관리기관에 이설 착수 요청 공문을 정식 발송합니다.</li>
            <li><strong>회신 기한 모니터링:</strong> 공문 발송 후 법정 회신 기한(14일 이내) 내 기관별 담당자 지정 및 이설 승인을 확인합니다.</li>
            <li><strong>이설 소요 공기 반영:</strong> 전력관(255일), 광역상수(160일), 통신관(150일), 난방관(80일), 가스관(62일)을 전체 착공 공정표에 반영합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 5px solid #166534;">
        <div class="card-header" style="color: #166534;">③ 협약 체결 및 현장 인수인계 단계 (Sign-off)</div>
        <ul class="bullet-list">
            <li><strong>이설 협약서 작성:</strong> 기관별 이설 시방 수칙, 현장 입회관 지정, 이설 구배 및 구조물 보호 조건을 협약서에 명시합니다.</li>
            <li><strong>인수인계 접수증 구비:</strong> 요청 공문 원본, 기관별 회신 문서, 현장 입회 확인서를 공무 파일로 완비합니다.</li>
        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 수행지침 | WBS 2000-1-3 | 지장물이설
    </div>
</div>
</body>
</html>"""

act3_checklist_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 지장물 이설 요청 (위수탁고) 체크리스트</title>
    <style>
        body { font-family: 'Pretendard', 'Noto Sans KR', sans-serif; margin: 0; padding: 25px; background: #f8fafc; color: #0f172a; line-height: 1.6; }
        .container { max-width: 950px; margin: 0 auto; background: #ffffff; padding: 35px; border-radius: 14px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); }
        .header { border-bottom: 3px solid #0284c7; padding-bottom: 18px; margin-bottom: 25px; }
        .title { font-size: 1.9rem; font-weight: 900; color: #0369a1; margin: 0; }
        .meta-info { font-size: 0.9rem; color: #475569; margin-top: 8px; font-weight: 600; }
        h2 { font-size: 1.35rem; font-weight: 800; color: #0284c7; border-left: 5px solid #38bdf8; padding-left: 12px; margin-top: 30px; margin-bottom: 18px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem; }
        th, td { border: 1px solid #cbd5e1; padding: 12px; vertical-align: middle; }
        th { background: #f1f5f9; color: #1e293b; font-weight: 700; text-align: center; }
        .footer-note { margin-top: 35px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 18px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">지장물 이설 요청 (위수탁고) 실시간 검측 체크리스트</h1>
        <div class="meta-info">Dongtan Tram WBS 2000-1-3 | 이설 요청 행정 O/X 검측표</div>
    </div>

    <h2>📋 지장물 이설 요청 9대 핵심 실시간 O/X 검측 항목</h2>

    <table>
        <thead>
            <tr>
                <th style="width: 12%;">구분</th>
                <th style="width: 70%;">지장물 이설 요청 핵심 행정/기술 검측 항목 (정량 수칙)</th>
                <th style="width: 18%;">검측 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="text-align: center; font-weight: bold;">공문발송</td>
                <td>1. 5대 위탁 관리기관(가스, 난방, 통신, 전력, 광역상수)에 발주처 정식 이설 요청 공문을 발송했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">회신기한</td>
                <td>2. 요청 공문 발송 후 법정 회신 기한(14일 이내) 내 기관별 공식 회신 및 담당자를 구비했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">이격거리</td>
                <td>3. 이설 요청 도면에 트램 궤도 구조물과 매설관 간 수평/수직 최소 이격거리(H ≥ 1.5m)를 명시했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">전력공기</td>
                <td>4. 특고압 전력관(22.9kV) 이설 표준 소요 공기(255일)를 전체 공정표에 반영했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">광역공기</td>
                <td>5. 광역상수도관(D800mm 이상) 이설 표준 소요 공기(160일)를 전체 공정표에 반영했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">통신공기</td>
                <td>6. 통신관로 및 광케이블 이설 표준 소요 공기(150일)를 전체 공정표에 반영했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">난방공기</td>
                <td>7. 지역난방관(열수송관) 이설 표준 소요 공기(80일)를 전체 공정표에 반영했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">가스공기</td>
                <td>8. 도시가스관 이설 표준 소요 공기(62일)를 전체 공정표에 반영했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">입회지정</td>
                <td>9. 위수탁 기관별 이설 시공 시 현장 동행 입회관 지정 서명을 확인했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
        </tbody>
    </table>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 체크리스트 | WBS 2000-1-3 | 지장물이설
    </div>
</div>
</body>
</html>"""


# ----------------------------------------------------
# 2. Activity 4: 도급자분 이설업체 선정(상_하수) HTML Templates
# ----------------------------------------------------
act4_standard_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 도급자분 이설업체 선정(상_하수) 기술 표준서</title>
    <style>
        :root {
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --accent-blue: #1e3a8a;
            --accent-cyan: #0284c7;
            --border-color: #e2e8f0;
        }
        body {
            font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
            margin: 0; padding: 30px 20px;
            background: var(--bg-primary); color: var(--text-primary);
            line-height: 1.6;
        }
        .container {
            max-width: 1000px; margin: 0 auto; background: var(--bg-card);
            padding: 40px; border-radius: 16px; border: 1px solid var(--border-color);
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08);
        }
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
            <li><strong>2) 하도급율 및 저가 방지:</strong> 실행예산 대비 하도급 계약 비율 <strong>82% 이상</strong> 준수로 품질 부실 예방</li>
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

act4_guideline_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 도급자분 이설업체 선정(상_하수) 수행지침</title>
    <style>
        body { font-family: 'Pretendard', 'Noto Sans KR', sans-serif; margin: 0; padding: 25px; background: #f8fafc; color: #0f172a; line-height: 1.6; }
        .container { max-width: 950px; margin: 0 auto; background: #ffffff; padding: 35px; border-radius: 14px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); }
        .header { border-bottom: 3px solid #16a34a; padding-bottom: 18px; margin-bottom: 25px; }
        .title { font-size: 1.9rem; font-weight: 900; color: #14532d; margin: 0; }
        .meta-info { font-size: 0.9rem; color: #475569; margin-top: 8px; font-weight: 600; }
        h2 { font-size: 1.35rem; font-weight: 800; color: #15803d; border-left: 5px solid #22c55e; padding-left: 12px; margin-top: 30px; margin-bottom: 18px; }
        .card { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px; margin-bottom: 16px; }
        .card-header { font-weight: 800; font-size: 1.05rem; margin-bottom: 8px; color: #166534; }
        .bullet-list { margin: 0; padding-left: 20px; font-size: 0.9rem; color: #334155; }
        .bullet-list li { margin-bottom: 6px; }
        .footer-note { margin-top: 35px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 18px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">도급자분 이설업체 선정(상_하수) 3단계 현장 수행지침</h1>
        <div class="meta-info">Dongtan Tram WBS 2000-1-4 | 상하수도 전문 하도급 업체 심사 및 계약 가이드</div>
    </div>

    <h2>📌 도급자분 이설업체 선정 3단계 정밀 수행 지침 (Playbook)</h2>

    <div class="card" style="border-left: 5px solid #2563eb;">
        <div class="card-header" style="color: #2563eb;">① 사전 입찰 자격 검증 단계 (Preparation)</div>
        <ul class="bullet-list">
            <li><strong>면허 및 실적 조회:</strong> 건설산업기본법에 따른 상하수도설비공업 전문 면허 원본 및 최근 3년간 동등 관경(D300~D800mm) 시공 실적을 조회합니다.</li>
            <li><strong>시방 요구 조항 세팅:</strong> 입찰 현장 설명서에 수압 10kg/cm², 하수 CCTV 100%, 층다짐 95% 이상 시방 준수 의무를 명시합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 5px solid #ea580c;">
        <div class="card-header" style="color: #ea580c;">② 적격 심사 및 외주 심의 단계 (Execution)</div>
        <ul class="bullet-list">
            <li><strong>적격 심사 평가:</strong> 수행 능력, 시공 실적, 재무 상태 및 입찰 가격을 종합 평가하여 적격 점수 85점 이상 업체만 대상자로 선별합니다.</li>
            <li><strong>하도급율 검증:</strong> 실행예산 대비 하도급 비율 82% 이상을 확보하여 덤핑 및 부실 시공 가능성을 사전 차단합니다.</li>
            <li><strong>외주 심의위원회 승인:</strong> 적격 심사 결과표 작성 후 현장소장 및 본사 외주팀의 정식 결재 승인을 획득합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 5px solid #166534;">
        <div class="card-header" style="color: #166534;">③ 하도급 계약 및 발주처 통지 단계 (Sign-off)</div>
        <ul class="bullet-list">
            <li><strong>계약 체결:</strong> 시방서, 안전 관리 수칙, 이설 공정표가 첨부된 정식 하도급 계약서를 체결합니다.</li>
            <li><strong>발주처 하도급 통지:</strong> 계약 체결 후 30일 이내 관련 서류를 첨부하여 발주처(화성시) 및 감리단에 하도급 통지서를 제출합니다.</li>
        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 수행지침 | WBS 2000-1-4 | 지장물이설
    </div>
</div>
</body>
</html>"""

act4_checklist_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 도급자분 이설업체 선정(상_하수) 체크리스트</title>
    <style>
        body { font-family: 'Pretendard', 'Noto Sans KR', sans-serif; margin: 0; padding: 25px; background: #f8fafc; color: #0f172a; line-height: 1.6; }
        .container { max-width: 950px; margin: 0 auto; background: #ffffff; padding: 35px; border-radius: 14px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); }
        .header { border-bottom: 3px solid #0284c7; padding-bottom: 18px; margin-bottom: 25px; }
        .title { font-size: 1.9rem; font-weight: 900; color: #0369a1; margin: 0; }
        .meta-info { font-size: 0.9rem; color: #475569; margin-top: 8px; font-weight: 600; }
        h2 { font-size: 1.35rem; font-weight: 800; color: #0284c7; border-left: 5px solid #38bdf8; padding-left: 12px; margin-top: 30px; margin-bottom: 18px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem; }
        th, td { border: 1px solid #cbd5e1; padding: 12px; vertical-align: middle; }
        th { background: #f1f5f9; color: #1e293b; font-weight: 700; text-align: center; }
        .footer-note { margin-top: 35px; text-align: center; font-size: 0.85rem; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 18px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">도급자분 이설업체 선정(상_하수) 실시간 검측 체크리스트</h1>
        <div class="meta-info">Dongtan Tram WBS 2000-1-4 | 하도급 적격 심사 O/X 검측표</div>
    </div>

    <h2>📋 도급자분 이설업체 선정 9대 핵심 실시간 O/X 검측 항목</h2>

    <table>
        <thead>
            <tr>
                <th style="width: 12%;">구분</th>
                <th style="width: 70%;">상하수도 이설업체 선정 핵심 검측 항목 (정량 규격)</th>
                <th style="width: 18%;">검측 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="text-align: center; font-weight: bold;">면허검증</td>
                <td>1. 상하수도설비공업 전문건설업 면허 보유 원본 및 영업 정지 여부를 확인했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">실적확인</td>
                <td>2. 최근 3년 이내 동등관경(D300~D800mm) 상하수도 관로 이설 시공 실적 증명서를 검속했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">적격점수</td>
                <td>3. 건설산업기본법 하도급 적격 심사 점수가 85점 이상 달성되었음을 확인했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">하도급율</td>
                <td>4. 실행예산 대비 하도급 계약 금액 비율이 82% 이상으로 적정하게 산정되었는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">수압시방</td>
                <td>5. 계약 특기 조항에 상수도 수압시험(10kg/cm² 1시간 유지 Zero 누수) 준수 의무를 명시했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">CCTV시방</td>
                <td>6. 계약 특기 조항에 하수관/오수관 CCTV 내시경 전수 조사(100%) 합격 의무를 명시했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">다짐시방</td>
                <td>7. 토사 되메우기 관 기초 모래(150mm) 및 층다짐도(95% 이상) 시방 조항을 반영했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">외주승인</td>
                <td>8. 적격 심사 종합 평가표를 첨부하여 외주 심의위원회 결재 승인을 완료했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">발주처통지</td>
                <td>9. 하도급 계약 체결 후 30일 이내 발주처(화성시)에 하도급 통지서를 제출 완료했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
        </tbody>
    </table>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 체크리스트 | WBS 2000-1-4 | 지장물이설
    </div>
</div>
</body>
</html>"""


# Apply updates to Act 3 and Act 4 folders (and twin folders)
print("Updating Act 3 and Act 4 HTML documents with tailored engineering specs...")

for root, dirs, files in os.walk(base_dir):
    folder = os.path.basename(root)
    
    # Act 3: 지장물 이설 요청
    if ("3_" in folder and "지장물" in folder) or "지장물 이설 요청" in folder:
        for f in files:
            f_path = os.path.join(root, f)
            if '표준서' in f and f.endswith('.html'):
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(act3_standard_html)
                print(f" ✅ Updated Act 3 Standard: {f}")
            elif '수행지침' in f and f.endswith('.html'):
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(act3_guideline_html)
                print(f" ✅ Updated Act 3 Guideline: {f}")
            elif '체크리스트' in f and f.endswith('.html'):
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(act3_checklist_html)
                print(f" ✅ Updated Act 3 Checklist: {f}")

    # Act 4: 도급자분 이설업체 선정(상_하수)
    elif ("4_" in folder and "이설업체" in folder) or "도급자분 이설업체 선정" in folder:
        for f in files:
            f_path = os.path.join(root, f)
            if '표준서' in f and f.endswith('.html'):
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(act4_standard_html)
                print(f" ✅ Updated Act 4 Standard: {f}")
            elif '수행지침' in f and f.endswith('.html'):
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(act4_guideline_html)
                print(f" ✅ Updated Act 4 Guideline: {f}")
            elif '체크리스트' in f and f.endswith('.html'):
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(act4_checklist_html)
                print(f" ✅ Updated Act 4 Checklist: {f}")

print("\n🎉 Act 3 & Act 4 HTML documents successfully updated with Dongtan Tram Engineering Standards!")
