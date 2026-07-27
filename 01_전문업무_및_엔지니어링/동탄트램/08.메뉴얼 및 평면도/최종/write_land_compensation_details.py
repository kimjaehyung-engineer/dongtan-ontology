import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# Find land compensation folder
target_folder = None
for f in os.listdir(base_dir):
    if "용지보상" in f:
        target_folder = os.path.join(base_dir, f)
        break

print(f"Target Land Compensation Folder: {target_folder}")

if target_folder:
    # 1. Standard HTML
    land_std_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 용지보상 Risk 파악 기술 표준서</title>
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
        <div class="breadcrumb">Dongtan Tram WBS 2000-1-12 Standard</div>
        <h1 class="title">용지보상 Risk 파악 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (용지보상)</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 보상팀 / 화성시 토지정보과</span>
            <span>|</span>
            <span><span class="badge">용지 보상 행정 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>동탄트램 궤도 노선 및 지장물 이설 구간에 저촉되는 사유지·국공유지 토지 보상 리스크를 사전 도출하고 토지보상법에 따라 손실 보상 및 수용 재결을 적기 이행</td></tr>
            <tr><th>수행 방법</th><td>토지/물건조사서 작성, 14일 이상 열람 공고, 3개 감정평가 법인 산정, 손실 보상 협의 및 미협의 시 중앙토지수용위원회(중토위) 수용 재결 신청</td></tr>
            <tr><th>주요 산출물</th><td>토지 및 지장물 물건조사서, 감정평가서, 손실보상 협의서, 중토위 수용재결 신청서</td></tr>
            <tr><th>관련 법령/기준</th><td>공익사업을 위한 토지 등의 취득 및 보상에 관한 법률(토지보상법), 공간정보의 구축 및 관리 등에 관한 법률</td></tr>
        </tbody>
    </table>

    <h2>2. 용지보상 및 토지 수용 정량 행정/기술 시방 수칙</h2>
    <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 22px; border-radius: 12px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 12px 0; color: #1e3a8a; font-size: 1.05rem;">🏞️ 토지보상법 및 지적 재조사 정량 행정 기준</h4>
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
            <thead>
                <tr style="background: #e2e8f0; color: #0f172a;">
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 20%;">보상 절차 항목</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 25%;">관련 법령 및 규정</th>
                    <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: center; width: 55%;">핵심 정량 기술 및 법정 기한 수칙</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-weight: bold; text-align: center;">보상 계획 열람 공고</td>
                    <td style="text-align: center;">토지보상법 제15조</td>
                    <td>• 토지 및 지장물 물건조사서 작성 후 <strong>14일 이상 열람 공고</strong> 시행<br>• 일간신문 및 화성시 시청 홈페이지 공고문 게시</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">감정평가 금액 산정</td>
                    <td style="text-align: center;">토지보상법 제68조</td>
                    <td>• 사업시행자, 시·도지사 및 토지소유자 추천 <strong>3개 감정평가 법인</strong> 선정<br>• 3개 평가 금액의 산술평균가로 최종 손실 보상액 확정</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">손실 보상 협의 기한</td>
                    <td style="text-align: center;">토지보상법 시행령 제8조</td>
                    <td>• 보상액 산정 후 토지 소유자에게 <strong>30일 이상 협의 기간</strong> 부여 통지<br>• 협의 성립 시 계약 체결 및 관할 등기소 소유권 이전</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">중토위 수용 재결</td>
                    <td style="text-align: center;">토지보상법 제28조</td>
                    <td>• 협의 불성립 토지 발생 시 <strong>착공 6개월 전 중토위 수용 재결</strong> 신청<br>• 재결 보상금 법원 공탁 및 직권 소유권 취득으로 공기 확보</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">지적 분할 측량 정밀도</td>
                    <td style="text-align: center;">공간정보관리법 제24조</td>
                    <td>• GRS80 세계측지계 기준 지적 분할 측량 <strong>수평 오차 ≤ ±5cm 이내</strong><br>• 트램 궤도 구조물 부지 수평/수직 이격거리 H ≥ 1.5m 검증</td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top: 15px; background: #eff6ff; padding: 12px 16px; border-radius: 8px; border: 1px solid #bfdbfe; font-size: 0.88rem; color: #1e40af;">
            <strong>📐 동탄트램 용지 확보 절대 수칙:</strong> 본 과업은 토공 착공 지연을 방지하기 위해 <strong>토지보상법 절차(14일 공고, 3개 감정평가, 중토위 수용 재결)</strong>를 엄격히 이행합니다.
        </div>
    </div>

    <h2>3. 용지보상 Risk 파악 핵심 프로세스 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="320" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">용지보상 Risk 파악 및 토지 수용 절차 체계</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① 물건조사서 작성</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">사유지 저촉 14일 공고</text>
            </g>

            <text x="225" y="145" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② 감정평가 산정</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">3개 평가법인 산술평균</text>
            </g>

            <text x="450" y="145" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ 손실 보상 협의</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">30일 이상 협의 통지</text>
            </g>

            <text x="675" y="145" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="170" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ 중토위 수용재결</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 주요 과업:</text>
                <text x="15" y="85" font-size="11" fill="#475569">보상금 공탁 및 직권 취득</text>
            </g>

            <rect x="30" y="250" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="278" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 토지 보상 협의 지연 시 트램 용지 미확보로 인한 토공 착공 불허 및 공기 지연 리스크 전면 차단</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 용지보상 Risk 파악 엔지니어링 시스템 해설</h4>
        <p style="margin: 0; line-height: 1.7;">본 과업은 토지보상법 규정에 의거하여 3개 감정평가 법인 산정 및 협의 불성립 건에 대한 중토위 수용 재결을 추진하여 동탄트램 궤도 용지를 적기에 100% 확보하는 행정적 절차입니다.</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> 14일 열람 공고, 3개 감정평가 산정, 30일 협의 및 중토위 수용 재결로 트램 용지 소유권을 직권 취득하는 핵심 단계입니다!
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 2000-1-12 | 지장물이설
    </div>
</div>
</body>
</html>"""

    # 2. Ultra-Detailed Guideline HTML
    land_gui_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 용지보상 Risk 파악 상세 현장 수행지침</title>
    <style>
        :root {
            --bg-primary: #f8fafc;
            --bg-card: #ffffff;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --accent-green: #16a34a;
            --border-color: #cbd5e1;
        }
        body { font-family: 'Pretendard', 'Noto Sans KR', sans-serif; margin: 0; padding: 30px 20px; background: var(--bg-primary); color: var(--text-primary); line-height: 1.7; }
        .container { max-width: 980px; margin: 0 auto; background: var(--bg-card); padding: 40px; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.06); }
        .header { border-bottom: 3px solid var(--accent-green); padding-bottom: 20px; margin-bottom: 30px; }
        .title { font-size: 2.1rem; font-weight: 900; color: #14532d; margin: 0; }
        .meta-info { font-size: 0.95rem; color: var(--text-secondary); margin-top: 10px; font-weight: 600; }
        .badge { background: #dcfce7; color: #15803d; font-weight: 700; padding: 4px 12px; border-radius: 6px; font-size: 0.85rem; }
        h2 { font-size: 1.45rem; font-weight: 800; color: #15803d; border-left: 6px solid #22c55e; padding-left: 14px; margin-top: 35px; margin-bottom: 20px; }
        .card { background: #ffffff; border: 1px solid var(--border-color); border-radius: 12px; padding: 22px; margin-bottom: 22px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03); }
        .card-header { font-weight: 800; font-size: 1.15rem; margin-bottom: 12px; display: flex; align-items: center; gap: 10px; }
        .bullet-list { margin: 0; padding-left: 22px; font-size: 0.94rem; color: #334155; }
        .bullet-list li { margin-bottom: 12px; line-height: 1.75; }
        .bullet-list li strong { color: #0f172a; font-weight: 700; }
        .footer-note { margin-top: 40px; text-align: center; font-size: 0.88rem; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 20px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">용지보상 Risk 파악 정밀 현장 수행지침 (Playbook)</h1>
        <div class="meta-info">Dongtan Tram WBS 2000-1-12 | <span class="badge">용지보상 Ultra-Detailed 실무 가이드</span></div>
    </div>

    <h2>📌 용지보상 Risk 파악 3단계 상세 현장 수행 지침</h2>

    <div class="card" style="border-left: 6px solid #2563eb;">
        <div class="card-header" style="color: #2563eb;">① 사전 준비 및 물건조사서 작성 단계 (Preparation & Survey)</div>
        <ul class="bullet-list">
            <li><strong>지적도 및 등기부 등본 전수 수집:</strong> 동탄트램 궤도 구역 내 사유지 및 국공유지 필지에 대한 토지 대장, 지적도 및 건물 등기부 등본을 100% 수집하여 지적 경계를 분석합니다.</li>
            <li><strong>3D CAD 지적 정합 및 저촉 필지 도출:</strong> 트램 노반 3D CAD 모델과 지적도를 상호 정합하여 수평 최소 이격거리(H ≥ 1.5m) 미달 사유지 필지 및 지장물 목록(Risk Log)을 작성합니다.</li>
            <li><strong>토지 및 지장물 물건조사서 작성:</strong> 현장 실측 조사를 실시하여 수목, 건축물, 분묘, 잔여지 현황을 물건조사서로 작성하고 토지 소유자 및 관계인 서명을 수령합니다.</li>
            <li><strong>보상계획 공고 및 열람 시행:</strong> 토지보상법 제15조에 따라 일간신문 및 화성시 시청 게시판에 보상계획을 공고하고 <strong>14일 이상 주민 열람</strong>을 실시합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 6px solid #ea580c;">
        <div class="card-header" style="color: #ea580c;">② 감정평가, 손실 보상 및 수용 재결 단계 (Execution & Appraisal)</div>
        <ul class="bullet-list">
            <li><strong>3개 감정평가 법인 현장 감정산정:</strong> 사업시행자, 시·도지사 및 토지소유자 추천 3개 감정평가 법인이 현장 조사를 시행하고 산술평균 가액으로 최종 보상액을 확정합니다.</li>
            <li><strong>손실 보상 협의 통지 및 계약 체결:</strong> 보상액 확정 후 토지 소유자에게 손실 보상 협의 서류를 송달하고 <strong>30일 이상 협의 기간</strong>을 부여하여 계약 체결을 추진합니다.</li>
            <li><strong>중앙토지수용위원회(중토위) 수용 재결:</strong> 협의 불성립 및 거부 필지에 대하여 착공 6개월 전 중토위에 수용 재결을 정식 신청하여 수용 재결서를 수령합니다.</li>
            <li><strong>보상금 공탁 및 직권 소유권 이전:</strong> 관할 지방법원에 수용 재결 보상금을 공탁(Deposit) 조치하고 화성시 명의로 토지 직권 소유권 이전 등기를 완료합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 6px solid #166534;">
        <div class="card-header" style="color: #166534;">③ 지적 분할 측량 및 현장 용지 이관 단계 (Handover & Sign-off)</div>
        <ul class="bullet-list">
            <li><strong>GRS80 세계측지계 지적 분할 측량:</strong> LX 한국국토정보공사에 지적 분할 측량을 의뢰하여 수평 오차 ±5cm 이내로 신설 지적 경계 점목을 설치합니다.</li>
            <li><strong>현장 용지 인계인수 및 가설 휀스 설치:</strong> 확보된 용지 경계선에 따라 공사장 가설 휀스를 설치하여 사유지 무단 저촉 분쟁을 근본적으로 방지합니다.</li>
            <li><strong>감리단 결재 및 후행 토공팀 정식 이관:</strong> 토지 소유권 취득 등기 필증 및 용지 확보 리포트를 결재 받아 후행 토공 및 지장물 이설 시공팀에 정식 이관합니다.</li>
        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 수행지침 | WBS 2000-1-12 | 지장물이설
    </div>
</div>
</body>
</html>"""

    # 3. Checklist HTML
    land_chk_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 용지보상 Risk 파악 맞춤형 체크리스트</title>
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
        <h1 class="title">용지보상 Risk 파악 실시간 맞춤 검측 체크리스트</h1>
        <div class="meta-info">Dongtan Tram WBS 2000-1-12 | 용지보상 전용 O/X 품질 검측표</div>
    </div>

    <h2>📋 용지보상 Risk 파악 9대 핵심 실시간 O/X 검측 항목</h2>

    <table>
        <thead>
            <tr>
                <th style="width: 12%;">구분</th>
                <th style="width: 70%;">용지보상 핵심 정량/법률 검측 항목 (토지보상법 수칙)</th>
                <th style="width: 18%;">검측 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="text-align: center; font-weight: bold;">점검1</td>
                <td>토지 대장, 지적도 및 건물 등기부 등본 100% 수집하여 지적 경계를 정합했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">점검2</td>
                <td>토지 및 지장물 물건조사서를 현장 실측 작성하고 소유자 서명을 받았는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">점검3</td>
                <td>토지보상법 제15조에 따라 보상계획을 14일 이상 열람 공고했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">점검4</td>
                <td>3개 감정평가 법인(시행자, 시도지사, 소유자 추천)의 산술평균액으로 보상가를 확정했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">점검5</td>
                <td>토지 소유자에게 30일 이상 손실 보상 협의 기간을 서면 부여했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">점검6</td>
                <td>협의 불성립 필지에 대하여 착공 6개월 전 중토위 수용 재결을 신청했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">점검7</td>
                <td>수용 재결 보상금 법원 공탁 및 직권 소유권 이전 등기를 완료했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">점검8</td>
                <td>GRS80 세계측지계 기준 지적 분할 측량(오차 ±5cm 이내) 경계 점목을 설치했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">점검9</td>
                <td>확보 용지 가설 휀스 시공 및 감리원 입회 서인 후 후행 토공팀에 이관했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
        </tbody>
    </table>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 체크리스트 | WBS 2000-1-12 | 지장물이설
    </div>
</div>
</body>
</html>"""

    # Overwrite in target folder files
    for sub in ["표준서", "수행지침", "체크리스트"]:
        sub_p = os.path.join(target_folder, sub)
        if os.path.exists(sub_p):
            for f in os.listdir(sub_p):
                if f.endswith('.html'):
                    file_path = os.path.join(sub_p, f)
                    if sub == "표준서":
                        with open(file_path, 'w', encoding='utf-8') as out:
                            out.write(land_std_html)
                        print(f"  ✅ Overwritten Land Compensation Standard HTML: {file_path}")
                    elif sub == "수행지침":
                        with open(file_path, 'w', encoding='utf-8') as out:
                            out.write(land_gui_html)
                        print(f"  ✅ Overwritten Land Compensation Guideline HTML: {file_path}")
                    elif sub == "체크리스트":
                        with open(file_path, 'w', encoding='utf-8') as out:
                            out.write(land_chk_html)
                        print(f"  ✅ Overwritten Land Compensation Checklist HTML: {file_path}")

print("🎉 Complete Ultra-Detailed Land Compensation Documents Update!")
