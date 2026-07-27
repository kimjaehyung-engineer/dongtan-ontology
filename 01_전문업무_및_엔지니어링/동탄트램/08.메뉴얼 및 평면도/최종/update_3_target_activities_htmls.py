import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# ----------------------------------------------------
# 1. Activity 5: 지장물 조사 (위탁기관 합동)
# ----------------------------------------------------
act_joint_survey_std = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 지장물 조사 (위탁기관 합동) 기술 표준서</title>
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
        <div class="breadcrumb">Dongtan Tram WBS 2000-1-5 Standard</div>
        <h1 class="title">지장물 조사 (위탁기관 합동) 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (합동조사)</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 공사팀 / 유관기관 합동조사단</span>
            <span>|</span>
            <span><span class="badge">현장 현치 조사 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>동탄트램 궤도 노선 내 매설된 6대 유틸리티(상하수도, 가스, 난방, 통신, 전력, 광역상수) 관리기관 담당자 현장 동행 입회 하에 지하 매설관 실치 위치 및 심도를 100% 현장 검증</td></tr>
            <tr><th>수행 방법</th><td>GPR 지형 지하 탐지, GRS80 세계측지계 측량 및 인력 줄따기 시굴(폭 1.0m, 깊이 1.2m~1.5m)을 실시하고 현장 실측 조사 보고서 작성</td></tr>
            <tr><th>주요 산출물</th><td>위탁기관 합동 현장 조사 보고서, GPR 탐사 성과표, 매설관 현치 측량 성과표, 현장 조사 사진대지</td></tr>
            <tr><th>관련 법령/기준</th><td>지하안전관리에 관한 특별법 제24조(지하안전평가), KCS 11 20 00 (토공사 탐정 수칙)</td></tr>
        </tbody>
    </table>

    <h2>2. 위탁기관 합동 지장물 현치 조사 4단계 프로세스 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="320" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">위탁기관 합동 현장 실치 조사 및 정밀 측량 절차</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① 합동 조사단 구성</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 6대 위탁기관 동행</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 감리단/시공사 입회</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 사전 도면 대조</text>
            </g>

            <text x="225" y="145" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② GPR & 정밀 측량</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• GPR 오차 ≤ ±10cm</text>
                <text x="15" y="85" font-size="11" fill="#475569">• GRS80 오차 ≤ ±5cm</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 관로 심도 정밀 측정</text>
            </g>

            <text x="450" y="145" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ 인력 시굴 현치</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 폭 1.0m 줄따기 굴착</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 매설관 노출 및 확인</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 궤도 이격 H≥1.5m 검증</text>
            </g>

            <text x="675" y="145" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="170" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ 조사서 서명 승인</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 기관 입회 날인</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 수량 오차 확정</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 최종 조사서 제출</text>
            </g>

            <rect x="30" y="250" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="278" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 기관 동행 입회 없이 줄따기 굴착 단독 진행 시 관로 불시 파손 및 법정 책임 발생 예방</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 위탁기관 합동 조사 업무 해설</h4>
        <p style="margin: 0; line-height: 1.7;">본 조사 업무는 동탄트램 궤도 노선 굴착 전 기존 GIS 지하매설물 도면과 실제 현장의 맨홀, 밸브, 관로 위치 오차를 6대 관리기관 담당자와 현장에서 직접 대조하여 불시 지하 관로 파손 사고를 근본 차단하는 공학적 검증 단계입니다.</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> 6대 위탁기관 동행 입회, GPR 오차 10cm 이내, GRS80 측량 오차 5cm 이내 및 인력 줄따기 시굴을 통해 지하관로 위치를 100% 확정하는 단계입니다!
    </div>

    <h2>3. 정량적 행정/공학 절대 기준 (Technical Specifications)</h2>
    <div style="background: #eff6ff; border: 1px solid #bfdbfe; padding: 20px; border-radius: 10px;">
        <ul style="margin: 0; padding-left: 20px; line-height: 1.9; color: #1e3a8a;">
            <li><strong>1) 합동 입회 기준:</strong> 6대 위탁기관(맑은물사업소, 삼천리, 난방공사, KT, 한전, K-water) 전담 감독관 <strong>100% 현장 동행 입회</strong> 필수</li>
            <li><strong>2) 탐사 및 측량 허용 오차:</strong> GPR 지형 탐지 심도 오차 <strong>$\le \pm 10\text{cm}$ 이내</strong>, GRS80 세계측지계 수평/수직 측량 오차 <strong>$\le \pm 5\text{cm}$ 이내</strong> 준수</li>
            <li><strong>3) 인력 시굴 폭/깊이:</strong> 줄따기 시굴 시 백호 굴착 금지 및 인력 굴착(폭 1.0m, 깊이 1.2m~1.5m) 시행으로 관로 보호</li>
            <li><strong>4) 트램 궤도 최소 이격거리:</strong> 현치 실측관과 트램 궤도 구조물 및 강화노반 간 <strong>최소 이격거리 $H \ge 1.5\text{m}$ 이상</strong> 확보 검증</li>
        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 2000-1-5 | 지장물이설
    </div>
</div>
</body>
</html>"""

act_joint_survey_gui = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 지장물 조사 (위탁기관 합동) 수행지침</title>
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
        <h1 class="title">지장물 조사 (위탁기관 합동) 3단계 현장 수행지침</h1>
        <div class="meta-info">Dongtan Tram WBS 2000-1-5 | 6대 위탁기관 현장 합동 실치 조사 가이드</div>
    </div>

    <h2>📌 지장물 합동 조사 3단계 정밀 수행 지침 (Playbook)</h2>

    <div class="card" style="border-left: 5px solid #2563eb;">
        <div class="card-header" style="color: #2563eb;">① 사전 탐사 및 입회 통보 단계 (Preparation)</div>
        <ul class="bullet-list">
            <li><strong>합동 조사단 통보:</strong> 6대 위탁기관에 합동 조사 일시, 구역 및 현장 입회 요청서를 3일 전 공식 발송합니다.</li>
            <li><strong>GPR 사전 탐사:</strong> 현장 투입 전 GPR 탐지기(오차 ≤ ±10cm)를 가동하여 매설관 예상 라인을 노면에 표시(Paint 마킹)합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 5px solid #ea580c;">
        <div class="card-header" style="color: #ea580c;">② 인력 시굴 및 정밀 측량 단계 (Execution)</div>
        <ul class="bullet-list">
            <li><strong>인력 줄따기 굴착:</strong> 관로 마킹 선을 따라 인력 굴착(폭 1.0m, 깊이 1.2m~1.5m)을 시행하여 매설관을 직접 노출시킵니다.</li>
            <li><strong>GRS80 정밀 측량:</strong> 노출된 매설관 상단 및 조인트 위치의 GRS80 세계측지계 좌표(수평/수직 오차 ≤ ±5cm)를 측정합니다.</li>
            <li><strong>궤도 이격거리 검증:</strong> 트램 궤도 구조물과 매설관 간 수평/수직 이격거리(H ≥ 1.5m)를 현장에서 대조합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 5px solid #166534;">
        <div class="card-header" style="color: #166534;">③ 현장 보고서 작성 및 서명 단계 (Sign-off)</div>
        <ul class="bullet-list">
            <li><strong>합동 조사 서명:</strong> 현장에 동행한 6대 위탁기관 감독관의 현장 입회 확인 서명을 조사 보고서에 획득합니다.</li>
            <li><strong>도면 갱신 및 사진대지 구비:</strong> 실측 좌표가 반영된 지장물 현황도 및 구간별 시굴 사진대지를 첨부하여 보고서를 완비합니다.</li>
        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 수행지침 | WBS 2000-1-5 | 지장물이설
    </div>
</div>
</body>
</html>"""

act_joint_survey_chk = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 지장물 조사 (위탁기관 합동) 체크리스트</title>
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
        <h1 class="title">지장물 조사 (위탁기관 합동) 실시간 검측 체크리스트</h1>
        <div class="meta-info">Dongtan Tram WBS 2000-1-5 | 현장 합동 조사 O/X 검측표</div>
    </div>

    <h2>📋 지장물 합동 조사 9대 핵심 실시간 O/X 검측 항목</h2>

    <table>
        <thead>
            <tr>
                <th style="width: 12%;">구분</th>
                <th style="width: 70%;">위탁기관 합동 현치 조사 핵심 검측 항목 (정량 수칙)</th>
                <th style="width: 18%;">검측 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="text-align: center; font-weight: bold;">합동입회</td>
                <td>1. 6대 위탁기관(맑은물, 삼천리, 난방, KT, 한전, K-water) 담당자가 100% 현장 동행 입회했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">GPR탐사</td>
                <td>2. GPR 지하 탐지기의 탐지 심도 오차가 ±10cm 이내임을 확인하고 노면에 Paint 마킹했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">인력시굴</td>
                <td>3. 백호 중장비 사용을 금지하고 인력 굴착(폭 1.0m, 깊이 1.2m~1.5m)으로 안전하게 관로를 노출했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">좌표측량</td>
                <td>4. GRS80 세계측지계 기준 수평/수직 측량 오차(±5cm 이내)로 노출관 좌표를 측정했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">이격거리</td>
                <td>5. 실측 매설관과 트램 궤도 구조물 간 수평/수직 최소 이격거리(H ≥ 1.5m)를 검검했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">관경검증</td>
                <td>6. 실제 노출된 관로의 재질, 관경, 밸브 위치가 기존 GIS 도면과 일치하는지 대조했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">사진대지</td>
                <td>7. 시굴 구간별 매설관 노출 상태 및 측량 표척(Staff) 적용 사진대지를 구비했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">기관서명</td>
                <td>8. 현장 동행 6대 위탁기관 감독관의 현장 입회 확인 서명을 조사 보고서에 수령했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">보고서승인</td>
                <td>9. 실측 조사 보고서를 감리단 및 발주처(화성시)에 제출하여 최종 승인을 완료했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
        </tbody>
    </table>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 체크리스트 | WBS 2000-1-5 | 지장물이설
    </div>
</div>
</body>
</html>"""


# ----------------------------------------------------
# 2. Activity 5: 착수전 Big Room 회의
# ----------------------------------------------------
act_bigroom_std = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 착수전 Big Room 회의 기술 표준서</title>
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
        <div class="breadcrumb">Dongtan Tram WBS 2000-1-8 Standard</div>
        <h1 class="title">착수전 Big Room 회의 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (통합 리딩)</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장소장 / 발주처·감리단·유관기관</span>
            <span>|</span>
            <span><span class="badge">통합 인터페이스 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>동탄트램 착공 전 발주처(화성시), 감리단, 시공사, 6대 위탁기관 및 궤도/노반 전문업체가 한자리에 모여 3D 간섭을 제어하고 릴레이 이설 공정을 최종 조율</td></tr>
            <tr><th>수행 방법</th><td>3D CAD/BIM 지형 모델링 간섭 검토, 이설 우선순위(상하수 ➔ 가스/난방 ➔ 전력/통신) 확정 및 통합 일정 협약 서명</td></tr>
            <tr><th>주요 산출물</th><td>Big Room 합동 회의록, 3D 간섭 검토서, 릴레이 이설 통합 마스터 공정표</td></tr>
            <tr><th>관련 법령/기준</th><td>건설기술 진흥법 시행령 제59조(공정 관리), 동탄도시철도 1·2공구 입찰안내서 인터페이스 지침</td></tr>
        </tbody>
    </table>

    <h2>2. Big Room 합동 인터페이스 조율 4단계 프로세스 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="320" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">Big Room 회의 3D 간섭 제어 및 릴레이 공정 조율 체계</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① 3D 모델링 제출</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 관종별 3D CAD 정합</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 궤도 구조물 연계</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 지하 간섭 지점 추출</text>
            </g>

            <text x="225" y="145" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② 간섭 제어 (0건)</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 3D 간섭 Zero 달성</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 이격거리 H≥1.5m 검증</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 굴착 깊이 재배정</text>
            </g>

            <text x="450" y="145" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ 릴레이 공정 조율</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 1단계: 상하수도 이설</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 2단계: 가스/난방 이설</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 3단계: 전력/통신 이설</text>
            </g>

            <text x="675" y="145" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="170" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ 회의록 결재</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 기관 전원 서명</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 원가절감안 확정</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 마스터 공정 승인</text>
            </g>

            <rect x="30" y="250" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="278" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 Big Room 회의 미시행 시 도로 중복 굴착 및 기관 간 공정 충돌 리스크 전면 차단</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 착수전 Big Room 회의 해설</h4>
        <p style="margin: 0; line-height: 1.7;">Big Room 회의는 지장물 이설과 트램 궤도/강화노반 시공 부서가 3D 모델링 데이터 기반으로 시공 간섭을 일괄 해결하고, 관종별 릴레이 이설 순서를 협의하여 굴착 횟수를 최소화하고 예산을 절감하는 통합 리딩 절정 단계입니다.</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> 3D 간섭 Zero 달성, 상하수 ➔ 가스/난방 ➔ 전력/통신 릴레이 순서 확정 및 기관 합동 결재로 공기 지연을 예방하는 마스터 회의 체계입니다!
    </div>

    <h2>3. 정량적 행정/공학 절대 기준 (Technical Specifications)</h2>
    <div style="background: #eff6ff; border: 1px solid #bfdbfe; padding: 20px; border-radius: 10px;">
        <ul style="margin: 0; padding-left: 20px; line-height: 1.9; color: #1e3a8a;">
            <li><strong>1) 3D 간섭 제어 목표:</strong> 3D CAD/BIM 지형 모델링 대조를 통한 지장물 간 및 궤도 구조물 간 <strong>시공 간섭 0건(Zero)</strong> 확정</li>
            <li><strong>2) 관종별 이설 릴레이 순서:</strong> 1단계 상하수도 ➔ 2단계 도시가스/지역난방 ➔ 3단계 특고압전력/통신관로 순서 엄격 준수</li>
            <li><strong>3) 소요 공기 마스터 공정 반영:</strong> 전력관(255일), 광역상수(160일), 통신관(150일), 난방관(80일), 가스관(62일) 통합 공정표 주간 단위 모니터링</li>
            <li><strong>4) 회의 결재 서명:</strong> 발주처, 감리단, 6대 위탁기관, 시공사 4자 전원 서명이 포함된 회의록 보존</li>
        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 2000-1-8 | 지장물이설
    </div>
</div>
</body>
</html>"""

act_bigroom_gui = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 착수전 Big Room 회의 수행지침</title>
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
        <h1 class="title">착수전 Big Room 회의 3단계 현장 수행지침</h1>
        <div class="meta-info">Dongtan Tram WBS 2000-1-8 | 유관기관 Big Room 합동 인터페이스 가이드</div>
    </div>

    <h2>📌 Big Room 회의 3단계 정밀 수행 지침 (Playbook)</h2>

    <div class="card" style="border-left: 5px solid #2563eb;">
        <div class="card-header" style="color: #2563eb;">① 3D 모델링 준비 및 안건 배포 단계 (Preparation)</div>
        <ul class="bullet-list">
            <li><strong>3D BIM/CAD 정합:</strong> 지장물 측량 성과표와 트램 궤도/노반 도면을 3D로 정합하여 시공 간섭 위험 구간을 도출합니다.</li>
            <li><strong>회의 안건 통보:</strong> 6대 위탁기관 및 감리단에 Big Room 회의 3D 분석 보고서와 안건을 5일 전 배포합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 5px solid #ea580c;">
        <div class="card-header" style="color: #ea580c;">② Big Room 개최 및 릴레이 조율 단계 (Execution)</div>
        <ul class="bullet-list">
            <li><strong>간섭 제어 검증:</strong> 3D 뷰어를 가동하여 매설관 간 수평/수직 이격거리(H ≥ 1.5m) 및 굴착 사면 안전성을 확인합니다.</li>
            <li><strong>릴레이 공정 확정:</strong> 도로 굴착 횟수를 줄이기 위해 상하수도 ➔ 가스/난방 ➔ 전력/통신 릴레이 이설 순서를 최종 조율합니다.</li>
            <li><strong>원가 절감 도출:</strong> 가설 흙막이 공동 활용 및 되메우기 토사 통합 수급안을 반영합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 5px solid #166534;">
        <div class="card-header" style="color: #166534;">③ 회의록 서명 및 공정표 승인 단계 (Sign-off)</div>
        <ul class="bullet-list">
            <li><strong>합동 회의록 서명:</strong> 발주처, 감리단, 6대 기관, 시공사 참석자 전원의 서명이 완료된 Big Room 회의록을 구비합니다.</li>
            <li><strong>통합 공정표 제출:</strong> 조율된 릴레이 이설 소요 공기가 반영된 마스터 공정표를 감리단에 공식 제출합니다.</li>
        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 수행지침 | WBS 2000-1-8 | 지장물이설
    </div>
</div>
</body>
</html>"""

act_bigroom_chk = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 착수전 Big Room 회의 체크리스트</title>
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
        <h1 class="title">착수전 Big Room 회의 실시간 검측 체크리스트</h1>
        <div class="meta-info">Dongtan Tram WBS 2000-1-8 | Big Room 회의 O/X 검측표</div>
    </div>

    <h2>📋 착수전 Big Room 회의 9대 핵심 실시간 O/X 검측 항목</h2>

    <table>
        <thead>
            <tr>
                <th style="width: 12%;">구분</th>
                <th style="width: 70%;">Big Room 회의 핵심 검측 항목 (정량 수칙)</th>
                <th style="width: 18%;">검측 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="text-align: center; font-weight: bold;">합동참석</td>
                <td>1. 발주처(화성시), 감리단, 시공사, 6대 위탁기관 및 궤도 전문업체 담당자가 전원 참석했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">3D간섭</td>
                <td>2. 3D CAD/BIM 지형 모델링 분석을 실시하여 지하 매설관 시공 간섭 0건(Zero)을 달성했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">이격거리</td>
                <td>3. 3D 검토 결과 매설관과 트램 궤도 구조물 간 수평/수직 최소 이격거리(H ≥ 1.5m)를 확인했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">릴레이순서</td>
                <td>4. 1단계 상하수도 ➔ 2단계 가스/난방 ➔ 3단계 전력/통신 릴레이 이설 순서를 확정했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">전력공기</td>
                <td>5. 한전 특고압 전력관 이설 소요 공기(255일)를 마스터 공정표에 반영했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">광역공기</td>
                <td>6. 수자원공사 광역상수관 이설 소요 공기(160일)를 마스터 공정표에 반영했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">원가절감</td>
                <td>7. 굴착 가시설 공동 활용 및 되메우기 토사 수급안을 통한 원가 절감 방안을 작성했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">회의록서명</td>
                <td>8. 참석 기관 전원의 확인 서명이 포함된 Big Room 합동 회의록을 구비했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">공정승인</td>
                <td>9. 조율된 릴레이 마스터 공정표에 대해 감리단 및 발주처 승인을 완료했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
        </tbody>
    </table>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 체크리스트 | WBS 2000-1-8 | 지장물이설
    </div>
</div>
</body>
</html>"""


# ----------------------------------------------------
# 3. Activity 6: 관리기관(맑은물사업소) 협의
# ----------------------------------------------------
act_malkeunmul_std = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 관리기관(맑은물사업소) 협의 기술 표준서</title>
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
        <div class="breadcrumb">Dongtan Tram WBS 2000-1-6 Standard</div>
        <h1 class="title">관리기관(맑은물사업소) 협의 기술 표준서</h1>
        <div class="meta-info">
            <span><strong>공종/분야:</strong> 사전토공 / 지장물이설 (상하수도 협의)</span>
            <span>|</span>
            <span><strong>주관부서:</strong> 현장 공무팀 / 화성시 맑은물사업소</span>
            <span>|</span>
            <span><span class="badge">상하수도 인허가 표준</span></span>
        </div>
    </div>

    <h2>1. 과업 개요 및 목적 (Overview & Scope)</h2>
    <table>
        <tbody>
            <tr><th style="width: 20%;">과업 목적</th><td>동탄트램 구간 내 도급자 시행 상하수도(상수, 하수, 오수관) 이설 도서에 대해 화성시 맑은물사업소 기술 시방 검토 및 정식 이설 협의 승인 획득</td></tr>
            <tr><th>수행 방법</th><td>이설 계획 도면, 관재 규격서, 수량 산출서 제출 후 수압시험(10kg/cm²), CCTV 검사(100%), 자연유하 구배(≥1.0%) 시방 조건 협의 체결</td></tr>
            <tr><th>주요 산출물</th><td>맑은물사업소 이설 협의 승인서, 상하수도 이설 도서, 관재 및 수량 변경 비교표</td></tr>
            <tr><th>관련 법령/기준</th><td>수도법 제21조, 하수도법 제27조, 화성시 수도정비 기본계획 및 KCS 47 10 00</td></tr>
        </tbody>
    </table>

    <h2>2. 맑은물사업소 상하수도 이설 협의 4단계 프로세스 모식도</h2>
    <div class="svg-container">
        <svg viewBox="0 0 900 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <rect width="900" height="320" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
            <text x="450" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">화성시 맑은물사업소 기술 시방 검토 및 승인 절차</text>

            <g transform="translate(30, 60)">
                <rect width="180" height="170" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="2"/>
                <rect width="180" height="35" rx="8" fill="#dbeafe"/>
                <text x="90" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af">① 이설 도서 제출</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 관재/관경 선정서</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 이설 평·종단면도</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 수량 비교표 구비</text>
            </g>

            <text x="225" y="145" font-size="20" fill="#2563eb">➔</text>

            <g transform="translate(245, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#ffedd5"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#9a3412">② 기술 시방 검토</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 수압 10kg/cm² 조항</text>
                <text x="15" y="85" font-size="11" fill="#475569">• CCTV 100% 조사</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 자연유하 구배 ≥1.0%</text>
            </g>

            <text x="450" y="145" font-size="20" fill="#ea580c">➔</text>

            <g transform="translate(470, 60)">
                <rect width="190" height="170" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2"/>
                <rect width="190" height="35" rx="8" fill="#dcfce7"/>
                <text x="95" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#15803d">③ 보완 반영 & 입회</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 사업소 의견 반영</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 현장 감독관 지정</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 통수 사전 조건 수립</text>
            </g>

            <text x="675" y="145" font-size="20" fill="#059669">➔</text>

            <g transform="translate(695, 60)">
                <rect width="175" height="170" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="2"/>
                <rect width="175" height="35" rx="8" fill="#e0e7ff"/>
                <text x="87" y="23" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e1b4b">④ 정식 승인 통보</text>
                <text x="15" y="65" font-size="11" font-weight="bold" fill="#0f172a">• 협의 승인 공문 획득</text>
                <text x="15" y="85" font-size="11" fill="#475569">• 이설 공사 착수 승인</text>
                <text x="15" y="105" font-size="11" fill="#475569">• 준공 인계 준비</text>
            </g>

            <rect x="30" y="250" width="840" height="45" rx="8" fill="#1e3a8a"/>
            <text x="450" y="278" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">🚨 맑은물사업소 미협의 시 신설 상하수도 관로 인계인수 거부 및 통수 불허 리스크 차단</text>
        </svg>
    </div>

    <div class="diagram-explanation">
        <h4 style="margin: 0 0 8px 0; color: #0f172a;">🔍 맑은물사업소 이설 협의 해설</h4>
        <p style="margin: 0; line-height: 1.7;">본 협의 업무는 동탄트램 궤도 조성으로 이설되는 상수관(덕타일 주철관 DCI), 하수관 및 오수관의 이설 위치와 구조적 안전성을 화성시 맑은물사업소 기술 기준에 맞추어 사전에 공식 검토 승인받는 절차입니다.</p>
    </div>

    <div class="key-takeaway">
        <strong>💡 핵심 요약:</strong> 상수 수압 10kg/cm², 하수 CCTV 100% 및 구배 1.0% 이상을 적용하여 맑은물사업소 정식 협의 승인을 획득하는 핵심 행정 단계입니다!
    </div>

    <h2>3. 정량적 행정/공학 절대 기준 (Technical Specifications)</h2>
    <div style="background: #eff6ff; border: 1px solid #bfdbfe; padding: 20px; border-radius: 10px;">
        <ul style="margin: 0; padding-left: 20px; line-height: 1.9; color: #1e3a8a;">
            <li><strong>1) 상수도 수압/수질 기준:</strong> 상수도 이설 후 <strong>수압시험 10kg/cm² 1시간 유지 Zero 누수</strong> 검증 및 통수 전 수돗물 잔류염소 소독 검사 필증 획득</li>
            <li><strong>2) 하수/오수 구배 및 검사:</strong> 하수도 관로 <strong>자연유하 구배 $\ge 1.0\%$ 이상</strong> 확보, 맨홀 인버트(Invert) 유선형 시공 및 <strong>CCTV 내시경 100% 조사</strong> 합격</li>
            <li><strong>3) 궤도 이격 심도:</strong> 신규 상하수도 관로 매설 심도(1.2m 이상) 및 트램 궤도 구조물과 <strong>최소 이격거리 $H \ge 1.5\text{m}$ 이상</strong> 확보</li>
            <li><strong>4) 사업소 협의 문서화:</strong> 관재/관경 변경 내역서 및 수량 비교표에 대한 맑은물사업소 담당자 입회 서명 승인 공문 구비</li>
        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 2000-1-6 | 지장물이설
    </div>
</div>
</body>
</html>"""

act_malkeunmul_gui = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 관리기관(맑은물사업소) 협의 수행지침</title>
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
        <h1 class="title">관리기관(맑은물사업소) 협의 3단계 현장 수행지침</h1>
        <div class="meta-info">Dongtan Tram WBS 2000-1-6 | 화성시 맑은물사업소 이설 협의 가이드</div>
    </div>

    <h2>📌 맑은물사업소 협의 3단계 정밀 수행 지침 (Playbook)</h2>

    <div class="card" style="border-left: 5px solid #2563eb;">
        <div class="card-header" style="color: #2563eb;">① 이설 도서 작성 및 사전 검토 단계 (Preparation)</div>
        <ul class="bullet-list">
            <li><strong>이설 도서 구비:</strong> 상하수도 이설 평·종단면도, 관재 산출서 및 궤도 최소 이격거리(H ≥ 1.5m) 반영 도면을 작성합니다.</li>
            <li><strong>맑은물사업소 제출:</strong> 화성시 맑은물사업소 정식 접수 및 담당 기술 검토원 배정을 확인합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 5px solid #ea580c;">
        <div class="card-header" style="color: #ea580c;">② 기술 시방 협의 및 현장 검속 단계 (Execution)</div>
        <ul class="bullet-list">
            <li><strong>시방 조건 조율:</strong> 상수도 수압시험(10kg/cm² 1시간) 및 하수도 CCTV 100% 내시경 검사 조건을 협의서에 수록합니다.</li>
            <li><strong>하수 구배 확보:</strong> 하수관 자연유하 구배(≥ 1.0%) 및 맨홀 인버트 시공 정밀도를 사전 검토 승인받습니다.</li>
            <li><strong>사업소 입회관 지정:</strong> 시공 중 이수밀 및 수압 시험 시 현장 동행 입회할 사업소 담당자를 지정합니다.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 5px solid #166534;">
        <div class="card-header" style="color: #166534;">③ 협의 승인 및 문서 관리 단계 (Sign-off)</div>
        <ul class="bullet-list">
            <li><strong>협의 승인서 획득:</strong> 맑은물사업소의 최종 이설 기술 협의 승인 공문 원본을 수령합니다.</li>
            <li><strong>감리단 통보:</strong> 승인 문서 및 맑은물사업소 검토 의견서를 감리단에 보고 후 이설 시공 착수를 승인받습니다.</li>
        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 수행지침 | WBS 2000-1-6 | 지장물이설
    </div>
</div>
</body>
</html>"""

act_malkeunmul_chk = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지장물이설 - 관리기관(맑은물사업소) 협의 체크리스트</title>
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
        <h1 class="title">관리기관(맑은물사업소) 협의 실시간 검측 체크리스트</h1>
        <div class="meta-info">Dongtan Tram WBS 2000-1-6 | 맑은물사업소 협의 O/X 검측표</div>
    </div>

    <h2>📋 맑은물사업소 이설 협의 9대 핵심 실시간 O/X 검측 항목</h2>

    <table>
        <thead>
            <tr>
                <th style="width: 12%;">구분</th>
                <th style="width: 70%;">맑은물사업소 협의 핵심 기술 검측 항목 (정량 수칙)</th>
                <th style="width: 18%;">검측 결과</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="text-align: center; font-weight: bold;">도서제출</td>
                <td>1. 상하수도 이설 평·종단면도, 관재 산출서 및 수량 비교표를 맑은물사업소에 제출했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">수압시방</td>
                <td>2. 상수도 이설 도서에 수압시험(10kg/cm² 1시간 유지 Zero 누수) 조건이 명시되었는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">CCTV조사</td>
                <td>3. 하수관/오수관 이설 도서에 CCTV 내시경 전수 조사(100%) 합격 조건이 명시되었는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">하수구배</td>
                <td>4. 하수도관 이설 노선의 자연유하 구배(≥ 1.0% 이상) 및 맨홀 인버트 시공 정밀도를 검속했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">이격거리</td>
                <td>5. 신설 상하수도 관로와 트램 궤도 구조물 간 수평/수직 최소 이격거리(H ≥ 1.5m)를 확인했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">매설심도</td>
                <td>6. 상하수도 동파 방지 및 궤도 하중 견딤 최소 매설 심도(1.2m 이상)를 준수했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">입회지정</td>
                <td>7. 이설 시공 중 수압시험 및 CCTV 검사 시 현장 동행 입회할 맑은물사업소 담당자를 지정했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">협의승인</td>
                <td>8. 화성시 맑은물사업소의 최종 기술 이설 협의 승인 공문 원본을 획득했는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
            <tr>
                <td style="text-align: center; font-weight: bold;">감리보고</td>
                <td>9. 맑은물사업소 협의 승인서를 감리단에 공식 보고하고 공사 착수를 승인받았는가?</td>
                <td style="text-align: center; font-weight: bold; color: #166534;">[ ☐ 적합  ☐ 부적합 ]</td>
            </tr>
        </tbody>
    </table>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 체크리스트 | WBS 2000-1-6 | 지장물이설
    </div>
</div>
</body>
</html>"""

print("Applying pristine HTML templates to target activity folders...")

# Apply to Activity folders safely
for root, dirs, files in os.walk(base_dir):
    folder = os.path.basename(root)

    # 1. 지장물 조사 (위탁기관 합동)
    if "지장물 조사" in folder or "5_지장물 조사" in folder:
        for f in files:
            f_path = os.path.join(root, f)
            if '표준서' in f and f.endswith('.html'):
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(act_joint_survey_std)
                print(f" ✅ Updated Joint Survey Standard: {f_path}")
            elif '수행지침' in f and f.endswith('.html'):
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(act_joint_survey_gui)
                print(f" ✅ Updated Joint Survey Guideline: {f_path}")
            elif '체크리스트' in f and f.endswith('.html'):
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(act_joint_survey_chk)
                print(f" ✅ Updated Joint Survey Checklist: {f_path}")

    # 2. 착수전 Big Room 회의
    elif "Big Room" in folder or "BigRoom" in folder or "5_착수전 Big" in folder:
        for f in files:
            f_path = os.path.join(root, f)
            if '표준서' in f and f.endswith('.html'):
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(act_bigroom_std)
                print(f" ✅ Updated Big Room Standard: {f_path}")
            elif '수행지침' in f and f.endswith('.html'):
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(act_bigroom_gui)
                print(f" ✅ Updated Big Room Guideline: {f_path}")
            elif '체크리스트' in f and f.endswith('.html'):
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(act_bigroom_chk)
                print(f" ✅ Updated Big Room Checklist: {f_path}")

    # 3. 관리기관(맑은물사업소) 협의
    elif "맑은물사업소" in folder or "6_관리기관" in folder or "13_관리기관" in folder:
        for f in files:
            f_path = os.path.join(root, f)
            if '표준서' in f and f.endswith('.html'):
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(act_malkeunmul_std)
                print(f" ✅ Updated Malkeunmul Standard: {f_path}")
            elif '수행지침' in f and f.endswith('.html'):
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(act_malkeunmul_gui)
                print(f" ✅ Updated Malkeunmul Guideline: {f_path}")
            elif '체크리스트' in f and f.endswith('.html'):
                with open(f_path, 'w', encoding='utf-8') as file:
                    file.write(act_malkeunmul_chk)
                print(f" ✅ Updated Malkeunmul Checklist: {f_path}")

print("\n🎉 All 3 target activities (Joint Survey, Big Room, Malkeunmul) successfully updated!")
