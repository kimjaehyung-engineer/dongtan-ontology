import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Users\sskjh\antigravity\01_전문업무_및_엔지니어링\동탄트램\08.메뉴얼 및 평면도\최종\매뉴얼BODY(집행단계-첨부폴더)\지장물이설"

# 1. Joint Survey
f_js = os.path.join(base_dir, "5_지장물 조사 (위탁기관 합동)")
# 2. Big Room
f_br = os.path.join(base_dir, "5_착수전 Big Room 회의")
# 3. Malkeunmul
f_mw = os.path.join(base_dir, "6_관리기관(맑은물사업소) 협의")

# Big Room Templates
br_std = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
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

# Malkeunmul Templates
mw_std = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
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
            <li><strong>2) 하수/오수 구배 및 검사:</strong> 하수도 관로 <strong>자연유하 구배 ≥ 1.0% 이상</strong> 확보, 맨홀 인버트(Invert) 유선형 시공 및 <strong>CCTV 내시경 100% 조사</strong> 합격</li>
            <li><strong>3) 궤도 이격 심도:</strong> 신규 상하수도 관로 매설 심도(1.2m 이상) 및 트램 궤도 구조물과 <strong>최소 이격거리 H ≥ 1.5m 이상</strong> 확보</li>
            <li><strong>4) 사업소 협의 문서화:</strong> 관재/관경 변경 내역서 및 수량 비교표에 대한 맑은물사업소 담당자 입회 서명 승인 공문 구비</li>
        </ul>
    </div>

    <div class="footer-note">
        동탄도시철도(트램) 건설공사 엔지니어링 기술 표준서 | WBS 2000-1-6 | 지장물이설
    </div>
</div>
</body>
</html>"""

def safe_write_folder(folder_path, std_content):
    if os.path.exists(folder_path):
        std_dir = os.path.join(folder_path, "표준서")
        if os.path.exists(std_dir):
            for f in os.listdir(std_dir):
                if f.endswith('.html'):
                    with open(os.path.join(std_dir, f), 'w', encoding='utf-8') as out:
                        out.write(std_content)
                    print(f" ✅ Overwritten Standard HTML: {f}")

print("Writing Big Room and Malkeunmul Standards...")
safe_write_folder(f_br, br_std)
safe_write_folder(f_mw, mw_std)

print("🎉 Complete All Overwrites!")
